# Полезные ссылки

Ссылка на макет в Figma: https://www.figma.com/design/kGTdJpYMYU7nCqiy4DfXra/Untitled?node-id=0-1&t=8BUu2e9I1vyGz3XU-1

Презентация лежит в корне проекта: _ЗаписиВоенныхЛетУрокеры\_ред.pdf_

Решение, представленное до Митапа №2, лежит в ветке [pre-meetup2](https://github.com/Grander78498/MireaHackAudio/tree/pre-meetup2)

# Установка
## Backend
Для запуска серверной части нужен пакетный менеджер [uv](https://github.com/astral-sh/uv)

Перед запуском нужно в директории backend создать _.env_ файл следующего формата:
```bash
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
BUCKET=...

FQDN_HOST=...
MONGO_USER=...
MONGO_PASSWORD=...

SEARCH_HOST=...
DASHBOARD_HOST=...
SEARCH_USER=...
SEARCH_PASSWORD=...
```

Установка зависимостей:
```bash
uv sync
```

Запуск проекта:
```bash
cd backend
uv run fastapi dev main.py
```

## Frontend
Установка зависимостей:
```bash
npm install
```

Запуск проекта:
```bash
npm run dev
```
