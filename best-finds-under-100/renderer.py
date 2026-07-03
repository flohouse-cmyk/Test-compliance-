"""Autonomous faceless video renderer — zero API keys required.

Turns a generated script into a finished vertical MP4 (1080x1920):
  1. Voiceover from free TTS (edge-tts first, gTTS fallback).
  2. Branded text-card scenes drawn with Pillow (hook → problem → product
     → search term → CTA), with a per-product color palette.
  3. Assembled with ffmpeg, scene timing matched to the voiceover length.

Videos land in renders/ and are listed on the Videos page for download.
If ffmpeg or TTS is unavailable, the render fails gracefully with a
recorded error — nothing else in the app is affected.
"""
import hashlib
import json
import os
import random
import shutil
import subprocess
import tempfile
import textwrap

from PIL import Image, ImageDraw, ImageFont

import db
from config import API_KEYS

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RENDER_DIR = os.path.join(BASE_DIR, "renders")
FONT_BOLD = os.path.join(BASE_DIR, "static", "fonts", "DejaVuSans-Bold.ttf")
FONT_REG = os.path.join(BASE_DIR, "static", "fonts", "DejaVuSans.ttf")

W, H = 1080, 1920

EDGE_VOICES = ["en-US-ChristopherNeural", "en-US-JennyNeural", "en-US-GuyNeural",
               "en-US-AriaNeural", "en-US-EricNeural", "en-US-MichelleNeural"]

# (background top, background bottom, accent, text) — dark, high-contrast palettes
PALETTES = [
    ((16, 24, 32), (30, 41, 59), (45, 212, 191), (245, 245, 244)),
    ((24, 16, 32), (49, 30, 59), (192, 132, 252), (245, 245, 244)),
    ((32, 22, 14), (68, 44, 24), (251, 191, 36), (250, 247, 240)),
    ((14, 28, 22), (22, 52, 40), (74, 222, 128), (240, 253, 244)),
    ((28, 14, 18), (60, 26, 34), (251, 113, 133), (253, 244, 246)),
]


def ffmpeg_available():
    return shutil.which("ffmpeg") is not None and shutil.which("ffprobe") is not None


def _seeded(key):
    return random.Random(int(hashlib.md5(key.encode()).hexdigest(), 16) % (2 ** 32))


# ------------------------------------------------------------------- TTS

def _tts_edge(text, out_path, voice):
    import asyncio
    import edge_tts

    async def _run():
        await edge_tts.Communicate(text, voice).save(out_path)

    asyncio.run(_run())


def _tts_gtts(text, out_path):
    from gtts import gTTS
    gTTS(text, lang="en", tld="us").save(out_path)


def make_voiceover(text, out_path, rng):
    """Free TTS: edge-tts (natural voices) first, gTTS as fallback.
    Returns the voice label used. Raises RuntimeError if both fail."""
    errors = []
    voice = rng.choice(EDGE_VOICES)
    try:
        _tts_edge(text, out_path, voice)
        if os.path.getsize(out_path) > 1000:
            return f"edge-tts {voice}"
        errors.append("edge-tts produced empty audio")
    except Exception as exc:  # noqa: BLE001 — any TTS failure falls through
        errors.append(f"edge-tts: {exc.__class__.__name__}")
    try:
        _tts_gtts(text, out_path)
        if os.path.getsize(out_path) > 1000:
            return "gTTS en-us"
        errors.append("gTTS produced empty audio")
    except Exception as exc:  # noqa: BLE001
        errors.append(f"gTTS: {exc.__class__.__name__}")
    raise RuntimeError("All free TTS voices failed (" + "; ".join(errors) +
                       "). Check the host's internet access.")


def audio_duration(path):
    out = subprocess.run(
        ["ffprobe", "-v", "quiet", "-print_format", "json", "-show_format", path],
        capture_output=True, text=True, check=True)
    return float(json.loads(out.stdout)["format"]["duration"])


# ----------------------------------------------- stock visuals (Pexels)

def fetch_stock_photos(product, outdir, rng, limit=5):
    """Download free-to-use portrait photos from Pexels as scene backgrounds.

    Pexels photos are free for commercial use (pexels.com/license) — unlike
    reusing other creators' posts, this keeps videos monetization-safe.
    Requires the free PEXELS_API_KEY; returns [] without it (text-card
    fallback) and on any network failure.
    """
    key = API_KEYS.get("PEXELS_API_KEY", "")
    if not key:
        return []
    try:
        import requests
    except ImportError:
        return []
    paths = []
    for query in (product["name"], product["category"]):
        try:
            resp = requests.get(
                "https://api.pexels.com/v1/search",
                params={"query": query, "orientation": "portrait", "per_page": 15},
                headers={"Authorization": key}, timeout=15)
            resp.raise_for_status()
            photos = resp.json().get("photos", [])
            rng.shuffle(photos)
            for photo in photos:
                if len(paths) >= limit:
                    break
                url = photo.get("src", {}).get("large2x") or photo.get("src", {}).get("portrait")
                if not url:
                    continue
                img = requests.get(url, timeout=20)
                img.raise_for_status()
                path = os.path.join(outdir, f"stock{len(paths)}.jpg")
                with open(path, "wb") as f:
                    f.write(img.content)
                paths.append(path)
        except Exception:  # noqa: BLE001 — stock photos are best-effort
            continue
        if len(paths) >= limit:
            break
    return paths


def _cover_crop(img, w, h):
    ratio = max(w / img.width, h / img.height)
    img = img.resize((int(img.width * ratio) + 1, int(img.height * ratio) + 1))
    left, top = (img.width - w) // 2, (img.height - h) // 2
    return img.crop((left, top, left + w, top + h))


# ----------------------------------------------------------- scene cards

def _font(path, size):
    return ImageFont.truetype(path, size)


def _wrap(draw, text, font, max_width):
    """Wrap text to fit max_width pixels."""
    lines = []
    for chunk in text.split("\n"):
        words, line = chunk.split(), ""
        for word in words:
            trial = f"{line} {word}".strip()
            if draw.textlength(trial, font=font) <= max_width:
                line = trial
            else:
                if line:
                    lines.append(line)
                line = word
        lines.append(line)
    return lines


def _card(palette, kicker, title, body, footer, brand, bg_photo=None):
    """Draw one 1080x1920 scene card, over a stock photo when available."""
    top, bottom, accent, ink = palette
    if bg_photo:
        try:
            img = _cover_crop(Image.open(bg_photo).convert("RGB"), W, H)
            # Darken for text legibility: base shade, heavier near the bottom.
            mask = Image.new("L", (1, H))
            for y in range(H):
                t = y / H
                mask.putpixel((0, y), 150 if t < 0.62 else int(150 + (t - 0.62) / 0.38 * 60))
            img = Image.composite(Image.new("RGB", (W, H), (8, 10, 14)), img,
                                  mask.resize((W, H)))
        except Exception:  # noqa: BLE001 — bad download falls back to gradient
            bg_photo = None
    if not bg_photo:
        img = Image.new("RGB", (W, H))
        draw = ImageDraw.Draw(img)
        for y in range(H):  # vertical gradient
            t = y / H
            draw.line([(0, y), (W, y)], fill=tuple(
                int(top[i] + (bottom[i] - top[i]) * t) for i in range(3)))
    draw = ImageDraw.Draw(img)

    margin, max_w = 90, W - 180
    y = 300

    if kicker:
        kfont = _font(FONT_BOLD, 44)
        draw.rounded_rectangle(
            [margin, y - 18, margin + draw.textlength(kicker, font=kfont) + 60, y + 66],
            radius=42, fill=accent)
        draw.text((margin + 30, y - 4), kicker, font=kfont, fill=top)
        y += 150

    tfont = _font(FONT_BOLD, 92)
    for line in _wrap(draw, title, tfont, max_w)[:7]:
        draw.text((margin, y), line, font=tfont, fill=ink)
        y += 112
    y += 40

    if body:
        draw.rounded_rectangle([margin, y, margin + 160, y + 12], radius=6, fill=accent)
        y += 60
        bfont = _font(FONT_REG, 56)
        for line in _wrap(draw, body, bfont, max_w)[:8]:
            draw.text((margin, y), line, font=bfont, fill=ink)
            y += 76

    if footer:
        ffont = _font(FONT_BOLD, 52)
        fy = H - 420
        for line in _wrap(draw, footer, ffont, max_w)[:3]:
            draw.text((margin, fy), line, font=ffont, fill=accent)
            fy += 68

    bfont = _font(FONT_BOLD, 40)
    bw = draw.textlength(brand, font=bfont)
    draw.text(((W - bw) / 2, H - 160), brand, font=bfont, fill=ink)
    return img


def make_scene_images(product, script_fields, outdir, rng):
    palette = PALETTES[_seeded(product["name"]).randrange(len(PALETTES))]
    brand = db.get_setting("brand_name", "Best Finds Under $100")
    hook = script_fields["hook"]
    cta = script_fields["cta"]
    scenes = [
        ("", hook, "", "Wait for it…", brand),
        ("THE PROBLEM", product["problem_solved"], "Sound familiar? There's a cheap fix.", "", brand),
        ("THE FIND", product["name"], product["why_care"], f"Typically {product['price_range']}", brand),
        ("HOW TO FIND IT", "Search this:", f"“{product['search_term']}”",
         "Prices and availability may change", brand),
        ("", cta, script_fields.get("disclosure", ""), "New find every day", brand),
    ]
    photos = fetch_stock_photos(product, outdir, rng)
    paths = []
    for i, (kicker, title, body, footer, brand_line) in enumerate(scenes):
        path = os.path.join(outdir, f"scene{i}.png")
        bg = photos[i % len(photos)] if photos else None
        _card(palette, kicker, title, body, footer, brand_line, bg_photo=bg).save(path)
        paths.append(path)
    return paths


# ---------------------------------------------------------------- ffmpeg

def assemble(image_paths, audio_path, out_path, total_duration):
    per = max(total_duration / len(image_paths), 1.5)
    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False) as f:
        for path in image_paths:
            f.write(f"file '{path}'\nduration {per:.3f}\n")
        f.write(f"file '{image_paths[-1]}'\n")  # concat demuxer needs last frame repeated
        concat_file = f.name
    try:
        subprocess.run(
            ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", concat_file,
             "-i", audio_path,
             "-vf", "fps=30,format=yuv420p,scale=1080:1920",
             "-c:v", "libx264", "-preset", "veryfast", "-crf", "23",
             "-c:a", "aac", "-b:a", "160k", "-shortest", "-movflags", "+faststart",
             out_path],
            capture_output=True, text=True, check=True, timeout=300)
    except subprocess.CalledProcessError as exc:
        raise RuntimeError("ffmpeg failed: " + (exc.stderr or "")[-400:]) from exc
    finally:
        os.unlink(concat_file)


# ------------------------------------------------------------ main entry

def render_script(script_type, script_id):
    """Render one script to MP4. Returns the rendered_videos row id."""
    table = "tiktok_scripts" if script_type == "tiktok" else "youtube_scripts"
    script = db.query(f"SELECT * FROM {table} WHERE id = ?", (script_id,), one=True)
    if script is None:
        raise ValueError("Script not found")
    product = db.query("SELECT * FROM product_ideas WHERE id = ?",
                       (script["product_id"],), one=True)

    video_id = db.insert("rendered_videos", {
        "product_id": product["id"], "script_type": script_type,
        "script_id": script_id, "filename": "", "duration_seconds": 0,
        "voice": "", "status": "rendering", "error": "", "created_at": db.now(),
    })

    try:
        if not ffmpeg_available():
            raise RuntimeError(
                "ffmpeg not found. On Replit add 'ffmpeg' under [nix] packages in "
                ".replit (already configured in this repo) and restart the Repl; "
                "elsewhere install ffmpeg on the host.")
        os.makedirs(RENDER_DIR, exist_ok=True)
        rng = _seeded(f"{script_type}-{script_id}-{product['name']}")

        hooks = db.loads(script["hooks"], []) if "hooks" in script.keys() else []
        hook = hooks[0] if hooks else (script["hook"] if "hook" in script.keys() else product["video_angle"])
        fields = {"hook": hook, "cta": script["cta"], "disclosure": script["disclosure"]}

        with tempfile.TemporaryDirectory() as tmp:
            audio_path = os.path.join(tmp, "voice.mp3")
            voice = make_voiceover(script["voiceover"], audio_path, rng)
            duration = audio_duration(audio_path)
            images = make_scene_images(product, fields, tmp, rng)
            filename = f"{script_type}_{script_id}_{video_id}.mp4"
            assemble(images, audio_path, os.path.join(RENDER_DIR, filename), duration)

        db.update("rendered_videos", video_id, {
            "filename": filename, "duration_seconds": round(duration, 1),
            "voice": voice, "status": "done",
        })
    except Exception as exc:  # noqa: BLE001 — record failure, never crash the app
        db.update("rendered_videos", video_id, {"status": "failed", "error": str(exc)[:500]})
    return video_id


def render_todays_scripts(limit=6):
    """Render today's scripts that don't have a finished video yet."""
    from datetime import date
    today = date.today().isoformat()
    rendered = {(r["script_type"], r["script_id"]) for r in db.query(
        "SELECT script_type, script_id FROM rendered_videos WHERE status = 'done'")}
    video_ids = []
    for script_type, table in (("tiktok", "tiktok_scripts"), ("youtube", "youtube_scripts")):
        for row in db.query(
                f"SELECT id FROM {table} WHERE created_at LIKE ? ORDER BY id DESC",
                (f"{today}%",)):
            if (script_type, row["id"]) not in rendered and len(video_ids) < limit:
                video_ids.append(render_script(script_type, row["id"]))
    return video_ids
