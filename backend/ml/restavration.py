from scipy.io import wavfile
import demucs.separate
import os
from pathlib import Path
import shutil
import librosa
import numpy as np
import noisereduce as nr
from scipy.signal import butter, lfilter, fftconvolve, medfilt
from pydub import AudioSegment
import time

from ml.transcription import get_lyrics
from ml.tagging import get_tags

"""
Модуль реставрации аудио
Модель для сепарации музыки и вокала, demucs, загружается в память последней.
Если whisper и bert из модулей генерации слов и генерации тегов загружены на gpu,
но памяти для demucs на gpu не хватает, он загрузится в cpu.
"""


def convert_mp3_to_wav(mp3_file, output_dir):
    """
    Перевод mp3 файла в формат wav
    :param mp3_file: Путь до исходного файла
    :param output_dir: Директория, куда нужно сохранить wav
    :return: Путь до сохранённого wav
    """

    audio = AudioSegment.from_mp3(mp3_file)
    wav_file = os.path.join(output_dir, os.path.splitext(os.path.basename(mp3_file))[0] + '.wav')
    audio.export(wav_file, format="wav")
    return wav_file


def separate(name):
    """
    Разделение аудиофайла на вокал и музыку с помощью модели Demucs.

    :param name: Путь к аудиофайлу
    :return: Кортеж путей к полученным файлам вокала и минуса
    """
    demucs.separate.main(["--two-stems", "vocals", "-n", "mdx_extra", name])
    file_name = os.path.splitext(os.path.basename(name))[0]
    fold_name = 'separated/mdx_extra/' + file_name + '/'
    return fold_name + 'vocals.wav', fold_name + 'no_vocals.wav'


def apply_eq(y, sr, lowcut=100.0, highcut=8000.0, order=5):
    """
    Применяет полосовой эквалайзер к аудиосигналу.
    :param y: Аудиосигнал
    :param sr: Частота дискретизации
    :param lowcut: Нижняя граница пропускаемых частот
    :param highcut: Верхняя граница пропускаемых частот
    :param order: Порядок фильтра
    :return: Отфильтрованный аудиосигнал
    """
    nyq = 0.5 * sr
    b, a = butter(order, [lowcut / nyq, highcut / nyq], btype='band')
    return lfilter(b, a, y)


def normalize_audio(audio):
    """Нормализация сигнала до диапазона [-1, 1]"""
    return audio / np.max(np.abs(audio) + 1e-8)


def soft_compressor(audio, threshold=0.2, ratio=4.0):
    """
    Мягкий компрессор для уменьшения динамического диапазона
    """
    abs_audio = np.abs(audio)
    gain = np.where(abs_audio < threshold, 1.0, (threshold + (abs_audio - threshold) / ratio) / abs_audio)
    return audio * gain


def rms_normalize(audio, target_db=-14):
    """RMS-нормализация сигнала под заданный уровень громкости"""
    rms = np.sqrt(np.mean(audio ** 2))
    scalar = 10 ** (target_db / 20) / (rms + 1e-8)
    return audio * scalar


def limiter(audio, limit=0.98):
    """Ограничение амплитуды сигнала"""
    return np.clip(audio, -limit, limit)


def apply_reverb(audio, sr, reverb_gain=0.3, decay=0.4):
    """
    Реверберация через импульсную свёртку
    """
    impulse = np.zeros(int(sr * 0.4))
    impulse[0] = 1.0
    for i in range(1, len(impulse)):
        impulse[i] = decay ** i
    reverb = fftconvolve(audio, impulse)[:len(audio)]
    return normalize_audio(audio + reverb_gain * reverb)


def median_filtering(audio, kernel_size=5):
    """
    Медианный фильтр для удаления щелчков и импульсных шумов
    """
    if kernel_size % 2 == 0:
        raise ValueError("kernel_size должен быть нечетным числом")
    return medfilt(audio, kernel_size=kernel_size)


def vocal_processing(vocal_path):
    """
    Обработка вокала
    :param vocal_path: Путь до wav записи вокала
    :return: numpy array - отфильтрованный вокал, int - частота дискретизации
    """
    vocal, sr = librosa.load(vocal_path, sr=None)
    vocal = median_filtering(vocal)
    vocal = nr.reduce_noise(y=vocal, sr=sr)
    vocal = apply_eq(vocal, sr)
    vocal = soft_compressor(vocal)
    vocal = apply_reverb(vocal, sr)
    vocal = rms_normalize(vocal)
    vocal = limiter(vocal)
    vocal = normalize_audio(vocal)
    return vocal, sr


def music_processing(music_path):
    """
    Обработка музыки
    :param music_path: Путь до wav записи музыки
    :return: numpy array - отфильтрованная музыка
    """
    music, sr = librosa.load(music_path, sr=None)
    music = median_filtering(music)
    music = apply_eq(music, sr, lowcut=300.0, highcut=10000.0)
    music = rms_normalize(music, target_db=-16)
    music = limiter(music)
    music = normalize_audio(music)
    return music, sr


def mix(music, vocal):
    """
    Сведение музыки и вокала
    :param music: numpy array - отфильтрованная музыка
    :param vocal: numpy array - отфильтрованный вокал
    :return: numpy array - песня
    """
    min_len = min(len(vocal), len(music))
    mix = vocal[:min_len] + music[:min_len]
    mix = rms_normalize(mix)
    mix = limiter(mix)
    mix = normalize_audio(mix)
    return mix


def process(name, separate_vocals=True):
    """
    Полный цикл обработки аудиофайла: реставрации,
    транскрипции и тегирования
    :param name: Абсолютный путь к исходному аудиофайлу
    :param separate_vocals: Производить ли разделение файла на вокал и музыку при обработке
    :return: строка - путь до обработанного аудио-файла,
    список словарей - слова песни,
    список строк - теги
    """
    if not os.path.exists(name):
        print(f'Файл {name} не найден.')
        return name, '', []

    if os.path.splitext(os.path.basename(name))[1] == '.mp3':
        new_name = convert_mp3_to_wav(name, '')
        os.remove(name)
        name = new_name

    # Обработка аудио
    vocal_path, music_path = name, name
    if separate_vocals:
        start = time.time()
        vocal_path, music_path = separate(name)
        end = time.time()
        print(f'Сепарация заняла {end - start:.2f} секунд')
    start = time.time()
    music, sr = music_processing(music_path)
    if separate_vocals:
      vocal, sr = vocal_processing(vocal_path)
      result = mix(music, vocal)
    else:
      result = music
    end = time.time()
    print(f'Обработка вокала и музыки заняла {end - start:.2f} секунд')

    # Сохранение обработанного файла
    directory = os.path.dirname(name)
    filename = os.path.basename(name)
    new_filename = "cleaned_" + filename
    output_path = os.path.abspath(os.path.join(directory, new_filename))
    scaled = np.int16(result * 32767)
    wavfile.write(output_path, sr, scaled)

    # Транскрипция
    start = time.time()
    lyrics = get_lyrics(vocal_path)  # Слова с тайм-кодами
    text = ''.join(token['word'] for token in lyrics)  # Объединение текста без тайм-кодов
    end = time.time()
    print(f'Транскрипция заняла {end - start:.2f} секунд')

    # Тегирование
    start = time.time()
    tags = get_tags(text)
    end = time.time()
    print(f'Тегирование заняло {end - start:.2f} секунд')

    # Удаление промежуточных файлов
    if separate_vocals:
        shutil.rmtree('separated/mdx_extra/' + os.path.splitext(os.path.basename(name))[0])

    return new_filename, lyrics, tags
