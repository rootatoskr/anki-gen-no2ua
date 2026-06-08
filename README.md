# anki-langdeck

Генератор Anki-колод для вивчення норвезької мови (Bokmål – українська).

## Як це працює

1. Береш слова з колоди [6000 Most Frequent Norwegian Words](https://ankiweb.net/shared/info/1011073314) як базу для вивчення
2. Задаєш слово AI-асистенту, використовуючи промпт із `docs/prompt_anki_no2ua_generator.txt`
3. (Опційно) перевіряєш відповідь через `docs/prompt_anki_no2ua_verifier.txt`
4. Копіюєш картки у `cards.txt`
5. Запускаєш скрипт – аудіо генерується автоматично через `edge_tts` + `ffmpeg`, отримуєш `output.apkg` для імпорту в Anki

## Структура проєкту

```
main.py – точка входу
config.py – константи (ID моделі, поля, ключі)
model.py – збирає genanki.Model з шаблонів
parser.py – парсинг тексту, побудова нотаток
audio.py – генерація TTS-аудіо через edge_tts + ffmpeg
templates/ – HTML-шаблони карток і CSS
docs/ – промпти для AI-асистента
cards.txt – вхідний файл із картками
audio_cache/ – кеш згенерованих mp3
```

## Встановлення

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Також потрібен `ffmpeg` у PATH.

## Використання

```bash
python3 main.py
```

Вхідні картки беруться з `cards.txt`. Результат: `output.apkg` у директорії проєкту.

## Формат вхідного файлу

Кожна картка – блок пар `ключ: значення`:

```
production: я хочу піти
recognition: jeg vil gå
title: å ville — хотіти
example_1: Jeg vil gå hjem.
translation_1: Я хочу піти додому.
```

Нова картка починається з поля `production:`. Порожні рядки ігноруються. Усі п'ять полів обов'язкові.

На кожну картку генерується дві нотатки: впізнавання (recognition) і продукування (production).
