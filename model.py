import os
import genanki
from config import MODEL_ID, MODEL_NAME, FIELDS

_DIR = os.path.join(os.path.dirname(__file__), 'templates')


def _read(name):
    with open(os.path.join(_DIR, name), encoding='utf-8') as f:
        return f.read()


MODEL = genanki.Model(
    MODEL_ID,
    MODEL_NAME,
    fields=[{'name': f} for f in FIELDS],
    templates=[
        {
            'name': 'Production',
            'qfmt': _read('production_front.html'),
            'afmt': _read('production_back.html'),
        },
    ],
    css=_read('card.css'),
)
