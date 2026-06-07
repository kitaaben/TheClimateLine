#!/usr/bin/env python3
"""
Generate 40-second audio for "Rising Temperatures" article.
Standalone: text embedded here, runs XTTS via WSL, converts to MP3,
updates articles.json, deploys.
"""

import json, os, subprocess, sys, tempfile
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent
JSON_PATH = PROJECT / "articles.json"
MEDIA_AUDIO = PROJECT / "media" / "audio"
SPEAKER_WAV = r"C:\Framers\Anchor\speaker.wav"
WRANGLER = r"C:\Users\Shujan Alee\AppData\Roaming\npm\wrangler.cmd"
TOKEN_FILE = PROJECT / "tokens.txt"

SCRIPT_TEXT = (
    "Earth average temperature has risen one point two degrees Celsius "
    "since the late eighteen hundreds. Carbon dioxide levels now exceed "
    "four hundred and twenty parts per million, the highest in four "
    "million years. The Arctic is warming nearly four times faster "
    "than the rest of the planet. Extreme heat events have tripled "
    "since the nineteen eighties. Every fraction of a degree we prevent "
    "reduces suffering for millions. We must cut emissions by switching "
    "to renewable energy and protecting our forests. The future depends "
    "on the choices we make today. This has been The Climate Line."
)


def win_to_wsl(path):
    path = path.replace("\\", "/")
    if len(path) > 1 and path[1] == ":":
        drive = path[0].lower()
        path = f"/mnt/{drive}{path[2:]}"
    return path


def run_xtts(text, output_wav):
    MEDIA_AUDIO.mkdir(parents=True, exist_ok=True)

    # Write text to a temp file
    txt_file = PROJECT / "media" / "audio" / "_input.txt"
    txt_file.write_text(text, encoding="utf-8")
    txt_wsl = win_to_wsl(str(txt_file))
    out_wsl = win_to_wsl(str(output_wav))
    spk_wsl = win_to_wsl(SPEAKER_WAV)

    # Build a standalone XTTS Python script to run in WSL
    xwsl = f"""#!/usr/bin/env python3
import os
from TTS.api import TTS

txt_file = "{txt_wsl}"
out_file = "{out_wsl}"
spk_file = "{spk_wsl}"

with open(txt_file, "r", encoding="utf-8") as f:
    text = f.read().strip()

tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2", gpu=False)
os.makedirs(os.path.dirname(out_file), exist_ok=True)
tts.tts_to_file(text=text, speaker_wav=spk_file, language="en", file_path=out_file)
size = os.path.getsize(out_file)
print(f"OK: {{size:,}} bytes")
"""

    script_file = PROJECT / "media" / "audio" / "_xtts_run.py"
    script_file.write_text(xwsl, encoding="utf-8")
    sc_wsl = win_to_wsl(str(script_file))

    cmd = ["wsl", "-d", "Ubuntu-22.04", "--", "bash", "-lc",
           f"cd ~/xtts && source xtts-env/bin/activate && python3 '{sc_wsl}'"]

    print("Running XTTS via WSL (may take a few minutes)...")
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
    print(r.stdout)
    if r.stderr:
        for line in r.stderr.strip().split("\n"):
            stripped = line.strip()
            if stripped and "warning" not in stripped.lower():
                print(f"  STDERR: {stripped}")

    # Cleanup temp files
    for p in [txt_file, script_file]:
        if p.exists():
            p.unlink()

    if r.returncode != 0:
        raise SystemExit(f"XTTS failed (exit {r.returncode})")

    if not output_wav.exists() or output_wav.stat().st_size == 0:
        raise SystemExit("Output WAV is empty or missing")


def convert_to_mp3(wav_path, mp3_path):
    print(f"Converting to MP3: {mp3_path.name}")
    r = subprocess.run(
        ["ffmpeg", "-y", "-i", str(wav_path),
         "-codec:a", "libmp3lame", "-qscale:a", "2",
         str(mp3_path)],
        capture_output=True, text=True, timeout=120
    )
    if r.returncode != 0:
        print(r.stderr)
        raise SystemExit("ffmpeg conversion failed")
    print(f"MP3: {mp3_path.stat().st_size:,} bytes")


def update_articles(slug, audio_path, duration):
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        articles = json.load(f)

    found = False
    for a in articles:
        if a["slug"] == slug:
            a["audio"] = audio_path
            a["duration"] = duration
            found = True
            break

    if not found:
        raise SystemExit(f"Article '{slug}' not found in articles.json")

    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(articles, f, indent=2, ensure_ascii=False)
    print(f"Updated articles.json: {slug}")


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
    print("Deployed!")


def main():
    slug = "rising-temperatures-global-warming"
    wav_path = MEDIA_AUDIO / f"{slug}.wav"
    mp3_path = MEDIA_AUDIO / f"{slug}.mp3"
    rel_path = f"media/audio/{slug}.mp3"
    duration = 40

    if mp3_path.exists():
        print(f"MP3 already exists ({mp3_path}), skipping generation.")
    else:
        run_xtts(SCRIPT_TEXT, wav_path)
        convert_to_mp3(wav_path, mp3_path)

    update_articles(slug, rel_path, duration)
    deploy()


if __name__ == "__main__":
    main()
