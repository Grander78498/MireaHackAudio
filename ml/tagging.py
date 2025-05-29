import torch
from transformers import pipeline

"""
Модуль генерации тегов для текста песни
Если не хватает памяти, заменить model_bert_name на "cointegrated/rubert-tiny2"
Если есть возможность использовать на gpu все модели,
заменить device на device = "cuda" if torch.cuda.is_available() else "cpu"
"""

model_bert_name = "DeepPavlov/rubert-base-cased"
device = "cpu"

model_bert = pipeline("zero-shot-classification", model=model_bert_name, device=device)

tags = ['Патриотизм', 'Дружба', 'Любовь', 'О Родине', 'Танки', 'Борьба с фашизмом',
        'День победы', 'Свобода', 'Фронт', 'Блокада', 'Сражение', 'Героизм',
        'Гордость', 'Надежда', 'Тоска', 'Память', 'Светлая грусть',
        'Дети войны', 'Ждать с войны', 'Марш', 'Народная', 'Баллада']


def get_tags(text):
    """
    Получение тегов для текста
    :param text: Исходный текст
    :return: список строк - подходящие теги
    """
    result = model_bert(text, candidate_labels=tags)
    labels = result["labels"]
    scores = result["scores"]
    filtered = [label for label, score in zip(labels, scores) if score > 0.5]
    if not filtered:
        filtered = list(labels)[:3]
    return filtered
