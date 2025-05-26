from scipy.io import wavfile
import demucs.separate
import os
from pathlib import Path
import shutil
import librosa
import subprocess
import numpy as np
import noisereduce as nr
from scipy.signal import butter, lfilter, fftconvolve, medfilt

from ml.transcription import get_lyrics
from ml.tagging import get_tags

"""
Модуль реставрации аудио
"""


def separate(name):
    """
    Разделение аудиофайла на вокал и музыку с помощью модели Demucs.

    :param name: Путь к аудиофайлу
    :return: Кортеж путей к полученным файлам вокала и минуса
    """

    demucs.separate.main(["--mp3", "--two-stems", "vocals", "-n", "mdx_extra", name])
    file_name = os.path.splitext(os.path.basename(name))[0]
    fold_name = 'separated/mdx_extra/' + file_name + '/'
    return fold_name + 'vocals.mp3', fold_name + 'no_vocals.mp3'


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
    :param vocal_path: Путь до mp3 записи вокала
    :return: numpy array - отфильтрованный вокал, int - частота дискретизации
    """
    vocal, sr = librosa.load(vocal_path)
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
    :param music_path: Путь до mp3 записи музыки
    :return: numpy array - отфильтрованная музыка
    """
    music, sr = librosa.load(music_path)
    music = median_filtering(music)
    music = apply_eq(music, sr, lowcut=300.0, highcut=10000.0)
    music = rms_normalize(music, target_db=-16)
    music = limiter(music)
    music = normalize_audio(music)
    return music


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


def process(name, seperate=True):
    """
    Полный цикл обработки аудиофайла: реставрации,
    транскрипции и тегирования
    :param name: Абсолютный путь к исходному аудиофайлу
    :param seperate: Производить ли разделение файла на вокал и музыку при обработке
    :return: строка - путь до обработанного аудио-файла,
    строка - слова песни,
    список строк - теги
    """

    # Обработка аудио
    vocal_path, music_path = name, name
    if seperate:
        vocal_path, music_path = separate(name)
    vocal, sr = vocal_processing(vocal_path)
    music = music_processing(music_path)
    result = mix(music, vocal)

    # Сохранение обработанного файла
    directory = os.path.dirname(name)
    filename = os.path.basename(name)
    new_filename = "cleaned_" + filename
    output_path = os.path.abspath(os.path.join(directory, new_filename))
    wavfile.write('temporary.wav', sr, result)
    subprocess.run(["ffmpeg", "-i", "temporary.wav", output_path])

    # Транскрипция
    clean_vocal_path = 'temporary.wav'
    wavfile.write(clean_vocal_path, sr, vocal)
    lyrics = get_lyrics(Path().absolute().parent.joinpath("temporary.wav"))  # Слова с тайм-кодами
    text = ''.join(token['word'] for token in lyrics)  # Объединение текста без тайм-кодов

    # Тегирование
    tags = get_tags(text)

    # Удаление промежуточных файлов
    shutil.rmtree('separated/mdx_extra/' + os.path.splitext(os.path.basename(name))[0])
    os.remove(clean_vocal_path)

    return output_path, lyrics, tags
