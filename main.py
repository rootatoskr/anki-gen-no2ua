#!/usr/bin/env python3
"""
Генератор Anki-карток з відповіді асистента Norwegian Bokmål.

Використання:
    python3 main.py

Вставте список карток у cards.txt і запустіть скрипт.
"""

import sys
import os
import genanki
from config import DECK_ID, DECK_NAME, ERROR_LINES, INPUT_FILE
from parser import split_cards, validate, build_note, word_from_title
from audio import generate, strip_html, sound_tag

INPUT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), INPUT_FILE)


def main():
    if not os.path.isfile(INPUT_PATH):
        open(INPUT_PATH, 'w').close()
        print(f'Створено {INPUT_FILE}. Вставте картки і запустіть знову.')
        sys.exit(0)

    with open(INPUT_PATH, encoding='utf-8') as f:
        text = f.read()

    if not text.strip():
        print(f'{INPUT_FILE} порожній. Вставте картки і запустіть знову.')
        sys.exit(0)

    if text.strip() in ERROR_LINES:
        print(f'Асистент повернув: {text.strip()}')
        sys.exit(0)

    cards = split_cards(text)
    if not cards:
        print('Карток не знайдено. Перевір формат вводу.')
        sys.exit(1)

    valid = []
    failed = 0
    for i, card in enumerate(cards, 1):
        missing = validate(card)
        if missing:
            print(f'Картка {i}: пропущено — {", ".join(missing)}', file=sys.stderr)
            failed += 1
        else:
            valid.append((i, card))

    if not valid:
        print('Жодної валідної картки.')
        sys.exit(1)

    cache_dir = os.path.join(os.path.dirname(INPUT_PATH), 'audio_cache')
    os.makedirs(cache_dir, exist_ok=True)

    texts = set()
    for _, card in valid:
        texts.add(word_from_title(card['title']))
        texts.add(strip_html(card['recognition']))
        texts.add(strip_html(card['example_1']))
    audio_map = generate(texts, cache_dir)

    deck = genanki.Deck(DECK_ID, DECK_NAME)
    ok = 0

    for i, card in valid:
        wt = word_from_title(card['title'])
        rt = strip_html(card['recognition'])
        et = strip_html(card['example_1'])
        w_tag = sound_tag(audio_map[wt])
        r_tag = sound_tag(audio_map[rt])
        e_tag = sound_tag(audio_map[et])
        card_1 = dict(card)
        card_1['example_1'] = card['translation_1']
        card_1['translation_1'] = card['example_1']
        deck.add_note(build_note(card_1, w_tag, e_tag, r_tag))
        card_rev = dict(card)
        card_rev['production'] = card['recognition']
        card_rev['recognition'] = card['production']
        deck.add_note(build_note(card_rev, w_tag, e_tag, r_tag))
        print(f'Картка {i}: OK — {card["title"]}')
        ok += 1

    out_path = os.path.join(os.path.dirname(INPUT_PATH), 'output.apkg')
    pkg = genanki.Package(deck)
    pkg.media_files = list(audio_map.values())
    pkg.write_to_file(out_path)

    print(f'\nСтворено: {ok} | Пропущено: {failed}')
    print(f'Файл: {out_path}')


if __name__ == '__main__':
    main()
