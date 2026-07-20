import re

INPUT_FILE = "cards.txt"

TTS_VOICE = "nb-NO-FinnNeural"
TTS_RATE = "-30%"

MODEL_ID = 5207392320
DECK_ID = 5029400111
MODEL_NAME = "Norwegian Bokmål to Ukrainian"
DECK_NAME = "Norwegian Bokmål to Ukrainian"

FIELDS = [
    "word",
    "production",
    "recognition",
    "title",
    "example_1",
    "translation_1",
    "audio",
    "audio_word",
    "audio_1",
    "note",
]

EXPECTED_KEYS = [
    "production",
    "recognition",
    "title",
    "example_1",
    "translation_1",
]
EXPECTED_SET = set(EXPECTED_KEYS)
START_KEY = "production"

ERROR_LINES = {
    "Невідомий вхід.",
    "Граматична функція, картка не потрібна.",
}

KEY_RE = re.compile(r"^(" + "|".join(EXPECTED_KEYS) + r")\s*:\s*(.*)$")
