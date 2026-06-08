import genanki
from config import KEY_RE, START_KEY, EXPECTED_SET
from model import MODEL


def split_cards(text):
    cards = []
    current = {}
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        m = KEY_RE.match(line)
        if not m:
            continue
        key, value = m.group(1), m.group(2).strip()
        if key == START_KEY and current:
            cards.append(current)
            current = {}
        current[key] = value
    if current:
        cards.append(current)
    return cards


def validate(card):
    return sorted(EXPECTED_SET - card.keys())


def word_from_title(title):
    return title.split('—')[0].strip()


def build_note(card, audio_word_tag='', audio_1_tag='', audio_tag=''):
    title = card['title']
    fields = [
        word_from_title(title),
        card['production'],
        card['recognition'],
        title,
        card['example_1'],
        card['translation_1'],
        audio_tag,
        audio_word_tag,
        audio_1_tag,
    ]
    return genanki.Note(model=MODEL, fields=fields)
