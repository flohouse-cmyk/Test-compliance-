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


def _probe_audio(path):
    """Validate a media file with ffprobe. Returns (ok, error_detail)."""
    try:
        out = subprocess.run(["ffprobe", "-v", "error", "-show_format", path],
                             capture_output=True, text=True, timeout=60)
        return out.returncode == 0, (out.stderr or "").strip()[:200]
    except Exception as exc:  # noqa: BLE001
        return False, f"{exc.__class__.__name__}: {exc}"


def make_voiceover(text, out_path, rng):
    """Free TTS: edge-tts (natural voices) first, gTTS as fallback.
    Each engine's output is validated with ffprobe before being accepted.
    Returns the voice label used. Raises RuntimeError if all fail."""
    errors = []
    voice = rng.choice(EDGE_VOICES)
    engines = [(f"edge-tts {voice}", lambda: _tts_edge(text, out_path, voice)),
               ("gTTS en-us", lambda: _tts_gtts(text, out_path))]
    for label, engine in engines:
        try:
            engine()
            if not os.path.exists(out_path) or os.path.getsize(out_path) < 1000:
                errors.append(f"{label}: empty audio file")
                continue
            ok, detail = _probe_audio(out_path)
            if ok:
                return label
            errors.append(f"{label}: invalid audio ({detail})")
        except Exception as exc:  # noqa: BLE001 — any TTS failure falls through
            errors.append(f"{label}: {exc.__class__.__name__}: {str(exc)[:150]}")
    raise RuntimeError("All free TTS voices failed — " + " | ".join(errors))


def audio_duration(path):
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-print_format", "json", "-show_format", path],
        capture_output=True, text=True)
    if out.returncode != 0:
        raise RuntimeError(f"ffprobe could not read the voiceover: "
                           f"{(out.stderr or '').strip()[:200]}")
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


def fetch_stock_videos(product, outdir, rng, limit=4):
    """Download free-to-use motion b-roll clips from Pexels Videos.

    Same free PEXELS_API_KEY and license as photos. Returns [] without the
    key or on failure; the renderer then tries photos, then gradient cards.
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
                "https://api.pexels.com/videos/search",
                params={"query": query, "orientation": "portrait", "per_page": 12},
                headers={"Authorization": key}, timeout=15)
            resp.raise_for_status()
            videos = resp.json().get("videos", [])
            rng.shuffle(videos)
            for video in videos:
                if len(paths) >= limit:
                    break
                # Smallest portrait file that's still HD-ish keeps downloads fast.
                files = sorted(
                    (f for f in video.get("video_files", [])
                     if f.get("link") and (f.get("height") or 0) >= 960),
                    key=lambda f: f.get("height") or 9999)
                if not files:
                    continue
                clip = requests.get(files[0]["link"], timeout=60)
                clip.raise_for_status()
                path = os.path.join(outdir, f"clip{len(paths)}.mp4")
                with open(path, "wb") as f:
                    f.write(clip.content)
                paths.append(path)
        except Exception:  # noqa: BLE001 — stock clips are best-effort
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


def _card(palette, kicker, title, body, footer, brand, bg_photo=None, transparent=False):
    """Draw one 1080x1920 scene card. transparent=True returns an RGBA overlay
    (dark scrim + text) for compositing onto motion video with ffmpeg."""
    top, bottom, accent, ink = palette
    if transparent:
        img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        for y in range(H):  # dark scrim so text reads over any footage
            t = y / H
            alpha = 140 if t < 0.62 else int(140 + (t - 0.62) / 0.38 * 65)
            draw.line([(0, y), (W, y)], fill=(8, 10, 14, alpha))
        bg_photo = "skip"
    elif bg_photo:
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


def _scenes(product, script_fields):
    brand = db.get_setting("brand_name", "Best Finds Under $100")
    return [
        ("", script_fields["hook"], "", "Wait for it…", brand),
        ("THE PROBLEM", product["problem_solved"], "Sound familiar? There's a cheap fix.", "", brand),
        ("THE FIND", product["name"], product["why_care"], f"Typically {product['price_range']}", brand),
        ("HOW TO FIND IT", "Search this:", f"“{product['search_term']}”",
         "Prices and availability may change", brand),
        ("", script_fields["cta"], script_fields.get("disclosure", ""), "New find every day", brand),
    ]


def _palette_for(product):
    return PALETTES[_seeded(product["name"]).randrange(len(PALETTES))]


def make_scene_images(product, script_fields, outdir, rng):
    """Full-frame scene stills: stock-photo backgrounds when available."""
    palette = _palette_for(product)
    photos = fetch_stock_photos(product, outdir, rng)
    paths = []
    for i, scene in enumerate(_scenes(product, script_fields)):
        path = os.path.join(outdir, f"scene{i}.png")
        bg = photos[i % len(photos)] if photos else None
        _card(palette, *scene, bg_photo=bg).save(path)
        paths.append(path)
    return paths, ("stock photos" if photos else "branded cards")


def make_scene_overlays(product, script_fields, outdir, rng):
    """Transparent text overlays for compositing onto motion b-roll."""
    palette = _palette_for(product)
    paths = []
    for i, scene in enumerate(_scenes(product, script_fields)):
        path = os.path.join(outdir, f"overlay{i}.png")
        _card(palette, *scene, transparent=True).save(path)
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


def assemble_motion(clips, overlays, audio_path, out_path, total_duration, workdir):
    """Composite text overlays onto looping stock clips, concat, add voiceover."""
    per = max(total_duration / len(overlays), 1.5)
    scene_files = []
    for i, overlay in enumerate(overlays):
        clip = clips[i % len(clips)]
        scene_out = os.path.join(workdir, f"scenevid{i}.mp4")
        try:
            subprocess.run(
                ["ffmpeg", "-y", "-stream_loop", "-1", "-t", f"{per:.3f}", "-i", clip,
                 "-i", overlay,
                 "-filter_complex",
                 "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,"
                 "crop=1080:1920,fps=30[bg];[bg][1:v]overlay=0:0,format=yuv420p",
                 "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "23",
                 scene_out],
                capture_output=True, text=True, check=True, timeout=300)
        except subprocess.CalledProcessError as exc:
            raise RuntimeError("ffmpeg scene failed: " + (exc.stderr or "")[-300:]) from exc
        scene_files.append(scene_out)

    concat_file = os.path.join(workdir, "scenes.txt")
    with open(concat_file, "w") as f:
        for path in scene_files:
            f.write(f"file '{path}'\n")
    try:
        subprocess.run(
            ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", concat_file,
             "-i", audio_path,
             "-c:v", "libx264", "-preset", "veryfast", "-crf", "23",
             "-c:a", "aac", "-b:a", "160k", "-shortest", "-movflags", "+faststart",
             out_path],
            capture_output=True, text=True, check=True, timeout=300)
    except subprocess.CalledProcessError as exc:
        raise RuntimeError("ffmpeg concat failed: " + (exc.stderr or "")[-300:]) from exc


def diagnose():
    """Test every piece of the render pipeline. Returns [(name, ok, detail)]."""
    checks = [
        ("ffmpeg installed", bool(shutil.which("ffmpeg")), shutil.which("ffmpeg") or "not found — restart the Repl so [nix] packages install"),
        ("ffprobe installed", bool(shutil.which("ffprobe")), shutil.which("ffprobe") or "not found"),
    ]
    with tempfile.TemporaryDirectory() as tmp:
        for label, fn in (("edge-tts voice (primary)",
                           lambda p: _tts_edge("Testing the voice, one two three.", p, "en-US-JennyNeural")),
                          ("gTTS voice (fallback)",
                           lambda p: _tts_gtts("Testing the voice, one two three.", p))):
            path = os.path.join(tmp, label[:4] + ".mp3")
            try:
                fn(path)
                ok, detail = _probe_audio(path)
                checks.append((label, ok, detail if not ok else f"OK ({os.path.getsize(path)} bytes)"))
            except Exception as exc:  # noqa: BLE001
                checks.append((label, False, f"{exc.__class__.__name__}: {str(exc)[:250]}"))

        key = API_KEYS.get("PEXELS_API_KEY", "")
        if not key:
            checks.append(("Pexels API (visuals)", False,
                           "PEXELS_API_KEY not set — videos fall back to branded cards"))
        else:
            try:
                import requests
                resp = requests.get("https://api.pexels.com/v1/search",
                                    params={"query": "kitchen", "per_page": 1},
                                    headers={"Authorization": key}, timeout=15)
                checks.append(("Pexels API (visuals)", resp.status_code == 200,
                               f"HTTP {resp.status_code}"
                               + ("" if resp.status_code == 200 else " — check the key value")))
            except Exception as exc:  # noqa: BLE001
                checks.append(("Pexels API (visuals)", False,
                               f"{exc.__class__.__name__}: {str(exc)[:250]}"))

        try:
            img_path = os.path.join(tmp, "test.png")
            Image.new("RGB", (1080, 1920), (20, 24, 32)).save(img_path)
            out = subprocess.run(
                ["ffmpeg", "-y", "-loop", "1", "-t", "1", "-i", img_path,
                 "-c:v", "libx264", "-preset", "veryfast", "-pix_fmt", "yuv420p",
                 os.path.join(tmp, "test.mp4")],
                capture_output=True, text=True, timeout=120)
            checks.append(("ffmpeg test encode", out.returncode == 0,
                           "OK" if out.returncode == 0 else (out.stderr or "")[-250:]))
        except Exception as exc:  # noqa: BLE001
            checks.append(("ffmpeg test encode", False,
                           f"{exc.__class__.__name__}: {str(exc)[:250]}"))
    return checks


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
            filename = f"{script_type}_{script_id}_{video_id}.mp4"
            out_path = os.path.join(RENDER_DIR, filename)

            # Best visuals first: motion b-roll → stock photos → branded cards.
            clips = fetch_stock_videos(product, tmp, rng)
            if clips:
                overlays = make_scene_overlays(product, fields, tmp, rng)
                assemble_motion(clips, overlays, audio_path, out_path, duration, tmp)
                visuals = "motion b-roll"
            else:
                images, visuals = make_scene_images(product, fields, tmp, rng)
                assemble(images, audio_path, out_path, duration)

        db.update("rendered_videos", video_id, {
            "filename": filename, "duration_seconds": round(duration, 1),
            "voice": f"{voice} · {visuals}", "status": "done",
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
