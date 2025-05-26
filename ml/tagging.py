import torch
from transformers import pipeline

"""
Модуль генерации тегов для текста песни
"""

model = "DeepPavlov/rubert-base-cased"
# model = "cointegrated/rubert-tiny2" # Если не хватает памяти
device = "cuda" if torch.cuda.is_available() else "cpu"

classifier = pipeline("zero-shot-classification", model=model, device=device)

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
    result = classifier(text, candidate_labels=tags)
    labels = result["labels"]
    scores = result["scores"]
    filtered = [label for label, score in zip(labels, scores) if score > 0.5]
    if not filtered:
        filtered = list(labels)[:3]
    return filtered
