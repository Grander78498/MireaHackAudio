import torch
import os
import whisper_timestamped as whisper_ts

from project_settings import ML_Models


"""
Модуль генерации слов для аудио
Если не хватает памяти, заменить # model_whisper_name на 'openai/whisper-tiny'
Если есть возможность использовать на gpu все модели,
заменить device на # device = "cuda" if torch.cuda.is_available() else "cpu"
"""

model_whisper = ML_Models().model_whisper


def get_lyrics(vocals_file):
    """
    Транскрипция песни
    :param vocals_file: Путь до wav файла с вокалом
    :return: Список слов песни в формате: [{
              'word': ..., - слово, str
              'start': ..., - секунда начала, float
              'end': ... - секунда конца, float
          }]
    """
    result = whisper_ts.transcribe(
        model_whisper,
        vocals_file,
        temperature=0.5,
        compression_ratio_threshold=2.4,
        logprob_threshold=-1.0,
        no_speech_threshold=0.6,
        condition_on_previous_text=False,
        language="ru")

    lyrics = []
    for segment in result['segments']:
        for word in segment['words']:
            lyrics.append({
                'word': word['text'],
                'start': float(word['start']),
                'end': float(word['end']),
            })

    return lyrics
