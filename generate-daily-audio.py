#!/usr/bin/env python3
"""
Daily climate audio generator:
  pytrends -> keyword filter -> Ollama title+script -> XTTS -> MP3 ->
  update articles.json -> wrangler deploy
"""

import json, os, re, subprocess, sys, tempfile, time
from datetime import datetime
from pathlib import Path

import requests
from pytrends.request import TrendReq

# ─── Config ───────────────────────────────────────────────
PROJECT_DIR = Path(r"C:\TheClimateLine")
JSON_PATH = PROJECT_DIR / "articles.json"
MEDIA_AUDIO = PROJECT_DIR / "media" / "audio"
WRANGLER = r"C:\Users\Shujan Alee\AppData\Roaming\npm\wrangler.cmd"
TOKEN_FILE = PROJECT_DIR / "tokens.txt"

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama3.2:latest"

XTTS_WSL_CMD = [
    "wsl", "-d", "Ubuntu", "--",
    "bash", "-c",
    "cd ~/xtts && source xtts-env/bin/activate && python3 -c \""
    "import sys; sys.path.insert(0, '.'); "
    "from modules.contentaudio import run_xtts; "
    "run_xtts(text=sys.argv[1], speaker_wav=sys.argv[2], output_path=sys.argv[3])\""
]

SPEAKER_WAV = r"C:\Framers\Anchor\speaker.wav"

CLIMATE_KEYWORDS = [
    "climate", "global warming", "renewable", "emission", "carbon",
    "fossil fuel", "green energy", "solar", "wind power",
    "temperature", "sea level", "ice melt", "deforestation",
    "biodiversity", "pollution", "sustainable", "net zero",
    "paris agreement", "cop", "ipcc", "extreme weather",
    "heatwave", "wildfire", "flood", "drought", "hurricane",
    "ocean acidification", "greenhouse gas", "methane",
    "electric vehicle", "clean energy", "energy transition"
]


def load_json():
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(data):
    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def get_trending_topics():
    """Fetch top trending searches from Google Trends (US)."""
    pytrends = TrendReq(hl="en-US", tz=300)
    trending = pytrends.trending_searches(pn="united_states")
    return trending[0].tolist() if not trending.empty else []


def filter_climate(topics):
    """Return the first topic matching a climate keyword."""
    for topic in topics:
        t = topic.lower()
        if any(kw in t for kw in CLIMATE_KEYWORDS):
            return topic
    return None


def ollama_generate(prompt):
    """Call Ollama with a prompt, return the response text."""
    resp = requests.post(OLLAMA_URL, json={
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.7, "max_tokens": 600}
    })
    resp.raise_for_status()
    return resp.json()["response"].strip()


def make_script(trending_topic):
    """Use Ollama to create a 260-word educational script about the topic."""
    prompt = (
        f"You are a climate educator. Write a ~260-word educational audio script "
        f"about: '{trending_topic}'. The script should be conversational, "
        f"informative, and suitable for spoken delivery (~2 minutes). "
        f"Keep it engaging but factual. Do NOT use markdown or special formatting."
    )
    script = ollama_generate(prompt)
    return script


def make_title(trending_topic):
    """Use Ollama to generate a short, educational title."""
    prompt = (
        f"Generate a short, educational title (max 8 words) for an audio "
        f"briefing about: '{trending_topic}'. Return ONLY the title, no quotes."
    )
    title = ollama_generate(prompt)
    return title.strip('"\'')


def generate_slug(title):
    slug = title.lower()
    slug = re.sub(r"[^a-z0-9\s-]", "", slug)
    slug = re.sub(r"\s+", "-", slug.strip())
    slug = re.sub(r"-+", "-", slug)
    return slug[:80]


def run_xtts(text, output_path):
    """Run XTTS via WSL subprocess."""
    cmd = [
        "wsl", "-d", "Ubuntu", "--",
        "bash", "-c",
        f"cd ~/xtts && source xtts-env/bin/activate && "
        f"python3 -c \"import sys; sys.path.insert(0, '.'); "
        f"from modules.contentaudio import run_xtts; "
        f"run_xtts(text='''{text}''', speaker_wav='{SPEAKER_WAV}', output_path='{output_path}')\""
    ]
    subprocess.run(cmd, check=True, timeout=600)


def generate_audio(articles, script, title, date_str):
    """Generate MP3 via XTTS, save to media/audio/, return audio path and duration."""
    slug = generate_slug(title)
    MEDIA_AUDIO.mkdir(parents=True, exist_ok=True)

    mp3_name = f"{date_str}.mp3"
    mp3_path = MEDIA_AUDIO / mp3_name
    rel_path = f"media/audio/{mp3_name}"

    if mp3_path.exists():
        print(f"Audio already exists for {date_str}, skipping generation.")
        return rel_path, 120

    print(f"Generating audio: {mp3_path}")

    # Clean script for XTTS
    clean = script.replace("\n", " ").replace("'", "").strip()
    run_xtts(clean, str(mp3_path))

    # Estimate duration: ~2 min for 260 words
    word_count = len(clean.split())
    duration_sec = max(60, round(word_count / 130 * 60))
    return rel_path, duration_sec


def deploy():
    """Run wrangler pages deploy."""
    env = os.environ.copy()
    if TOKEN_FILE.exists():
        with open(TOKEN_FILE) as f:
            token = f.read().strip()
        env["CLOUDFLARE_API_TOKEN"] = token

    result = subprocess.run(
        [WRANGLER, "pages", "deploy", ".", "--project-name", "theclimateline"],
        cwd=str(PROJECT_DIR),
        capture_output=True, text=True, timeout=120, env=env
    )
    print(result.stdout)
    if result.returncode != 0:
        print("Deploy stderr:", result.stderr)
        raise SystemExit("Deploy failed")


def main():
    print("=== Daily Climate Audio Generator ===")
    date_str = datetime.now().strftime("%Y-%m-%d")

    articles = load_json()

    # Skip if already generated today
    if any(a.get("audio") and date_str in a.get("audio", "") for a in articles):
        print(f"Audio already exists for {date_str}, skipping.")
        return

    print("Fetching Google Trends...")
    topics = get_trending_topics()
    if not topics:
        print("No trending topics found, using fallback topic.")
        topic = "climate change impacts"
    else:
        topic = filter_climate(topics)
        if not topic:
            print(f"No climate topics in trends ({topics[0:5]}), using first trend.")
            topic = topics[0]

    print(f"Trending topic: {topic}")

    print("Generating title via Ollama...")
    title = make_title(topic)
    print(f"Title: {title}")

    print("Generating script via Ollama...")
    script = make_script(topic)
    print(f"Script length: {len(script.split())} words")

    print("Generating audio via XTTS...")
    audio_path, duration = generate_audio(articles, script, title, date_str)

    slug = generate_slug(title)

    new_article = {
        "slug": slug,
        "title": title,
        "summary": f"Today's climate briefing on {topic}.",
        "date": datetime.now().strftime("%B %d, %Y"),
        "audio": audio_path,
        "duration": duration
    }

    articles.insert(0, new_article)
    save_json(articles)

    print(f"Article added: {title} ({audio_path})")

    print("Deploying to Cloudflare Pages...")
    deploy()

    print("=== Done ===")


if __name__ == "__main__":
    main()
