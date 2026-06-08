import asyncio
import hashlib
import os
import re
import subprocess
import edge_tts
from config import TTS_VOICE, TTS_RATE


def strip_html(text):
    return re.sub(r'<[^>]+>', '', text).strip()


def sound_tag(path):
    return f'[sound:{os.path.basename(path)}]'


def _fname(text):
    h = hashlib.md5(text.encode()).hexdigest()[:16]
    return f'langdeck_{h}.mp3'


def _trim_silence(path):
    tmp = path + '.tmp.mp3'
    subprocess.run(
        [
            'ffmpeg', '-y', '-i', path,
            '-af', 'silenceremove=start_periods=1:start_silence=0.01:start_threshold=-50dB,areverse,silenceremove=start_periods=1:start_silence=0.01:start_threshold=-50dB,areverse',
            tmp,
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=True,
    )
    os.replace(tmp, path)


async def _synthesize(text, path):
    communicate = edge_tts.Communicate(text, TTS_VOICE, rate=TTS_RATE)
    await communicate.save(path)
    _trim_silence(path)


async def _run_all(tasks):
    await asyncio.gather(*[_synthesize(t, p) for t, p in tasks])


def generate(texts, out_dir):
    unique = {t: os.path.join(out_dir, _fname(t)) for t in texts}
    to_gen = [(t, p) for t, p in unique.items() if not os.path.exists(p)]
    if to_gen:
        asyncio.run(_run_all(to_gen))
    return unique
