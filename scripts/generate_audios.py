#!/usr/bin/env python3
"""Batch generate 40-second audios for articles and deploy."""
import json, os, subprocess, sys
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent
JSON_PATH = PROJECT / "articles.json"
MEDIA_AUDIO = PROJECT / "media" / "audio"
SPEAKER_WAV = r"C:\Framers\Anchor\speaker.wav"
WRANGLER = r"C:\Users\Shujan Alee\AppData\Roaming\npm\wrangler.cmd"
TOKEN_FILE = PROJECT / "tokens.txt"

JOBS = [
    {
        "slug": "rising-sea-levels-coastal-crisis",
        "text": (
            "Global sea levels have risen approximately twenty three centimeters "
            "since eighteen eighty. The rate has more than doubled from one point "
            "four millimeters per year to over three point six millimeters per year "
            "today. Nearly nine hundred million people live in low lying coastal "
            "zones. Cities from Miami to Jakarta face increasing flood risk. "
            "The West Antarctic Ice Sheet alone could raise sea levels by three "
            "to five meters if it destabilizes. Reducing emissions now is the most "
            "effective way to slow the rise. This has been The Climate Line."
        ),
        "duration": 40,
    },
    {
        "slug": "heatwaves-climate-crisis",
        "text": (
            "Heatwaves are the deadliest natural disaster most people do not "
            "think about. They kill more people each year than hurricanes, floods "
            "and tornadoes combined. Climate change has made heatwaves longer, "
            "hotter and more frequent worldwide. Thirty seven percent of heat "
            "related deaths between nineteen ninety one and twenty eighteen were "
            "directly linked to human caused warming. Urban heat islands make "
            "cities several degrees hotter than surrounding areas. Reducing "
            "emissions is the only way to prevent extreme heat from becoming "
            "even more severe. This has been The Climate Line."
        ),
        "duration": 40,
    },
]


def win_to_wsl(path):
    path = path.replace("\\", "/")
    if len(path) > 1 and path[1] == ":":
        return f"/mnt/{path[0].lower()}{path[2:]}"
    return path


def run_xtts(text, output_wav):
    MEDIA_AUDIO.mkdir(parents=True, exist_ok=True)
    txt = MEDIA_AUDIO / "_input.txt"
    scr = MEDIA_AUDIO / "_run.py"

    txt.write_text(text, encoding="utf-8")

    tin = win_to_wsl(str(txt))
    tou = win_to_wsl(str(output_wav))
    tspk = win_to_wsl(SPEAKER_WAV)
    scr.write_text(
        'import os,sys\n'
        'from TTS.api import TTS\n'
        f't=open("{tin}").read().strip()\n'
        f'os.makedirs(os.path.dirname("{tou}"),exist_ok=True)\n'
        f'TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2",gpu=False).tts_to_file('
        f'text=t,speaker_wav="{tspk}",language="en",'
        f'file_path="{tou}")\n'
        f'print("OK:"+str(os.path.getsize("{tou}"))+" bytes")',
        encoding="utf-8",
    )

    cmd = [
        "wsl", "-d", "Ubuntu-22.04", "--", "bash", "-c",
        f"cd /home/user/xtts && source xtts-env/bin/activate && "
        f"python3 '{win_to_wsl(str(scr))}'"
    ]

    print(f"  Running XTTS...")
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=1200)
    print(r.stdout)
    if r.returncode != 0:
        for line in r.stderr.strip().split("\n"):
            s = line.strip()
            if s and "warning" not in s.lower():
                print(f"  ERR: {s}")
        raise SystemExit(f"XTTS failed ({r.returncode})")

    for p in [txt, scr]:
        if p.exists():
            p.unlink()


def convert_mp3(wav, mp3):
    r = subprocess.run(
        ["ffmpeg", "-y", "-i", str(wav), "-codec:a", "libmp3lame", "-qscale:a", "2", str(mp3)],
        capture_output=True, text=True, timeout=120
    )
    if r.returncode != 0:
        print(r.stderr)
        raise SystemExit("ffmpeg failed")


def update_json(slug, audio_path, duration):
    data = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    for a in data:
        if a["slug"] == slug:
            a["audio"] = audio_path
            a["duration"] = duration
            print(f"  Updated: {slug}")
            break
    JSON_PATH.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def deploy():
    env = os.environ.copy()
    if TOKEN_FILE.exists():
        token = TOKEN_FILE.read_text(encoding="utf-8").strip().split("\n")[2].strip()
        env["CLOUDFLARE_API_TOKEN"] = token
    r = subprocess.run(
        [WRANGLER, "pages", "deploy", ".", "--project-name", "theclimateline"],
        cwd=str(PROJECT), capture_output=True, text=True, timeout=120, env=env
    )
    print(r.stdout)
    if r.returncode != 0:
        print(r.stderr)
        raise SystemExit("Deploy failed")


def main():
    for job in JOBS:
        slug = job["slug"]
        wav = MEDIA_AUDIO / f"{slug}.wav"
        mp3 = MEDIA_AUDIO / f"{slug}.mp3"
        rel = f"media/audio/{slug}.mp3"

        if mp3.exists():
            print(f"[{slug}] MP3 exists, skipping generation.")
        else:
            print(f"[{slug}] Generating...")
            run_xtts(job["text"], wav)
            if not wav.exists():
                raise SystemExit(f"WAV not generated for {slug}")
            convert_mp3(wav, mp3)
            wav.unlink()

        update_json(slug, rel, job["duration"])

    deploy()


if __name__ == "__main__":
    main()
