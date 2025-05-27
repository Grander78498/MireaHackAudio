import torch
import os
import whisper_timestamped as whisper_ts

from project_settings import ML_Models


"""
Модуль генерации слов для аудио
"""

# model_name = "dvislobokov/whisper-large-v3-turbo-russian"
# model_name = "openai/whisper-tiny" # Если не хватает памяти
# device = "cuda" if torch.cuda.is_available() else "cpu"
# model = whisper_ts.load_model(model_name, device=device)

model = ML_Models().transcription_model


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
    result = whisper_ts.transcribe(model,
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
