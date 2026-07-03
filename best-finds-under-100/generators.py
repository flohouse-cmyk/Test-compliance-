"""Content generators.

Every generator works in demo mode (no API keys) using original template
pools from content_data.py. If OPENAI_API_KEY is set, voiceovers are
enhanced with AI; any AI failure silently falls back to templates so the
app never breaks because a key is missing or invalid.
"""
import hashlib
import json
import random
from urllib.parse import quote_plus

import content_data as data
import db
from config import (AFFILIATE_DISCLOSURE, API_KEYS, DEFAULT_DISCLOSURE)


# ---------------------------------------------------------------- utilities

def _seeded(name):
    """Deterministic RNG per product name so scores are stable across runs."""
    seed = int(hashlib.md5(name.encode()).hexdigest(), 16) % (2 ** 32)
    return random.Random(seed)


def search_term_for(name, hi):
    return f"{name.lower()} under {hi}"


def placeholder_link_for(term):
    label, template = data.PLACEHOLDER_LINK_TEMPLATES[0]
    return template.format(q=quote_plus(term))


def amazon_search_link(term):
    """Plain Amazon search link; appends the associate tag only if configured."""
    url = f"https://www.amazon.com/s?k={quote_plus(term)}"
    tag = API_KEYS["AMAZON_ASSOCIATE_TAG"]
    if tag:
        url += f"&tag={quote_plus(tag)}"
    return url


def disclosure_for(product_id):
    """Affiliate disclosure only when an affiliate link actually exists."""
    row = db.query(
        "SELECT 1 FROM monetization_links WHERE product_id = ? "
        "AND monetization_status IN ('affiliate_link', 'sponsored_link') "
        "AND (affiliate_link != '' OR sponsored_link != '') LIMIT 1",
        (product_id,), one=True)
    if row:
        return db.get_setting("affiliate_disclosure", AFFILIATE_DISCLOSURE)
    return db.get_setting("default_disclosure", DEFAULT_DISCLOSURE)


def best_link_or_term(product):
    """The most monetized link available, else the search term."""
    link = db.query(
        "SELECT * FROM monetization_links WHERE product_id = ? ORDER BY id DESC LIMIT 1",
        (product["id"],), one=True)
    if link:
        for field in ("sponsored_link", "affiliate_link", "manual_link", "placeholder_link"):
            if link[field]:
                return link[field]
    return product["search_term"]


# ------------------------------------------------------------ product ideas

def score_product(name, category):
    rng = _seeded(name + category)
    scores = {
        "viral_score": rng.randint(55, 95),
        "visual_score": rng.randint(55, 95),
        "giftability_score": rng.randint(45, 95),
        "impulse_score": rng.randint(50, 95),
        "tiktok_score": rng.randint(55, 95),
        "youtube_score": rng.randint(50, 95),
    }
    weights = {"viral_score": 2, "visual_score": 1.5, "giftability_score": 1,
               "impulse_score": 1.5, "tiktok_score": 2, "youtube_score": 2}
    total = sum(scores[k] * w for k, w in weights.items())
    scores["overall_score"] = round(total / sum(weights.values()))
    return scores


def video_angle_for(category, rng):
    template = rng.choice(data.VIDEO_ANGLES)
    return template.format(category=category, category_lower=category.lower(),
                           space=data.CATEGORY_SPACE[category])


def generate_product_ideas(count=10, category=None, source="generated"):
    """Create new product ideas from the concept pool, skipping names already saved."""
    existing = {r["name"] for r in db.query("SELECT name FROM product_ideas")}
    candidates = []
    for cat, concepts in data.PRODUCT_POOL.items():
        if category and cat != category:
            continue
        for concept in concepts:
            if concept[0] not in existing:
                candidates.append((cat, concept))
    random.shuffle(candidates)

    created = []
    for cat, (name, lo, hi, why, problem, audience) in candidates[:count]:
        rng = _seeded(name)
        scores = score_product(name, cat)
        term = search_term_for(name, hi)
        product_id = db.insert("product_ideas", {
            "name": name, "category": cat, "price_range": f"${lo}-${hi}",
            "search_term": term, "why_care": why, "target_audience": audience,
            "problem_solved": problem, "video_angle": video_angle_for(cat, rng),
            **scores, "source": source, "created_at": db.now(),
        })
        db.insert("monetization_links", {
            "product_id": product_id, "search_term": term,
            "placeholder_link": placeholder_link_for(term),
            "monetization_status": "search_link",
            "notes": "Auto-created placeholder search link. Replace with a real product or affiliate link later.",
            "created_at": db.now(), "updated_at": db.now(),
        })
        created.append(product_id)
    return created


def rescore_all_products():
    products = db.query("SELECT id, name, category FROM product_ideas")
    for p in products:
        db.update("product_ideas", p["id"], score_product(p["name"], p["category"]))
    return len(products)


def pick_top_products(limit=5):
    db.execute("UPDATE product_ideas SET featured = 0")
    top = db.query("SELECT id FROM product_ideas ORDER BY overall_score DESC LIMIT ?", (limit,))
    for row in top:
        db.update("product_ideas", row["id"], {"featured": 1})
    return [row["id"] for row in top]


# ---------------------------------------------------------------- AI helper

def _try_ai_voiceover(product, platform):
    """Optional OpenAI enhancement. Returns None on any problem (demo fallback)."""
    if not API_KEYS["OPENAI_API_KEY"]:
        return None
    try:
        from openai import OpenAI
        client = OpenAI(api_key=API_KEYS["OPENAI_API_KEY"])
        prompt = (
            f"Write a faceless {platform} voiceover script (60-90 words) about a product "
            f"concept: '{product['name']}' ({product['category']}, {product['price_range']}). "
            f"Why people care: {product['why_care']}. Problem it solves: {product['problem_solved']}. "
            "Rules: original copy, no fake testing claims, no guaranteed results, no medical/financial/"
            "safety claims, punchy and useful, product-discovery tone, end with a soft follow CTA."
        )
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300, timeout=20,
        )
        text = resp.choices[0].message.content.strip()
        return text or None
    except Exception:
        return None


# ------------------------------------------------------------------- hooks

def make_hooks(product, n=5):
    rng = _seeded(product["name"] + "hooks")
    lo, hi = _price_bounds(product["price_range"])
    slots = {
        "name_lower": product["name"].lower(),
        "cat_lower": product["category"].lower(),
        "cat_space": data.CATEGORY_SPACE.get(product["category"], "space"),
        "problem_lower": product["problem_solved"].lower().rstrip("."),
        "lo": lo, "hi": hi,
    }
    templates = rng.sample(data.HOOK_TEMPLATES, min(n, len(data.HOOK_TEMPLATES)))
    return [t.format(**slots) for t in templates]


def _price_bounds(price_range):
    nums = [int(s) for s in price_range.replace("$", "").split("-") if s.strip().isdigit()]
    if len(nums) == 2:
        return nums[0], nums[1]
    return 10, 100


def make_hashtags(product, extra_platform_tag=None):
    tags = list(data.CATEGORY_HASHTAGS.get(product["category"], []))
    tags += data.GENERIC_HASHTAGS
    if extra_platform_tag:
        tags.append(extra_platform_tag)
    return " ".join(tags[:8])


def make_caption(product, hook):
    return (f"{hook} 🔎 Search: “{product['search_term']}”. "
            "Prices and availability may change.")


def _voiceover_template(product):
    space = data.CATEGORY_SPACE.get(product["category"], "space")
    return (
        f"If {product['problem_solved'].lower().rstrip('.')} sounds familiar, this one's for you. "
        f"This is the {product['name'].lower()} — {product['why_care'].lower().rstrip('.')}. "
        f"It usually runs {product['price_range']}, which makes it one of the easiest upgrades "
        f"for your {space} right now. It's made for {product['target_audience'].lower().rstrip('.')}, "
        f"and it's exactly the kind of find most people scroll right past. "
        "Prices change fast, so save this one. And follow for a new under-$100 find every day."
    )


def _shot_list(product):
    return [
        "Scene 1 (0-2s): Bold hook text over a quick reveal of the product concept.",
        f"Scene 2 (2-5s): Show the problem — {product['problem_solved'].lower().rstrip('.')}.",
        f"Scene 3 (5-9s): Product in use, close-up on the key feature.",
        "Scene 4 (9-13s): Second angle or before/after moment for the payoff.",
        f"Scene 5 (13-17s): Price text on screen: “usually {product['price_range']}”.",
        "Scene 6 (17-20s): End card with CTA text and the search term on screen.",
    ]


# ---------------------------------------------------------- TikTok scripts

def generate_tiktok_script(product):
    rng = _seeded(product["name"] + "tiktok" + db.now())
    hooks = make_hooks(product)
    hook = hooks[0]
    voiceover = _try_ai_voiceover(product, "TikTok") or _voiceover_template(product)
    cta = rng.choice(data.CTA_OPTIONS).format(
        space=data.CATEGORY_SPACE.get(product["category"], "space"))
    ai_prompts = [
        f"Photorealistic product shot of a {product['name'].lower()}, on a clean neutral surface, "
        "soft natural light, shallow depth of field, vertical 9:16, no logos, no people's faces",
        f"Lifestyle b-roll of a {product['name'].lower()} being used in a modern "
        f"{data.CATEGORY_SPACE.get(product['category'], 'room')}, hands only, cozy lighting, 9:16",
        f"Minimal aesthetic flat-lay themed around {product['category'].lower()}, "
        "neutral palette, top-down, 9:16, original generic products only",
    ]
    script_id = db.insert("tiktok_scripts", {
        "product_id": product["id"],
        "title": f"{product['name']} — {product['video_angle']}",
        "hooks": json.dumps(hooks),
        "voiceover": voiceover,
        "on_screen_text": (f"{hook}\n{product['price_range']} • save this\n"
                           f"Search: {product['search_term']}"),
        "shot_list": json.dumps(_shot_list(product)),
        "caption": make_caption(product, hook),
        "hashtags": make_hashtags(product, "#tiktokfinds"),
        "cta": cta,
        "video_length": rng.choice(["15-20 seconds", "20-25 seconds", "25-30 seconds"]),
        "background_style": rng.choice(data.BACKGROUND_STYLES),
        "ai_prompts": json.dumps(ai_prompts),
        "disclosure": disclosure_for(product["id"]),
        "created_at": db.now(),
    })
    return script_id


# --------------------------------------------------------- YouTube scripts

def generate_youtube_script(product):
    rng = _seeded(product["name"] + "youtube" + db.now())
    hooks = make_hooks(product)
    hook = hooks[1] if len(hooks) > 1 else hooks[0]
    voiceover = _try_ai_voiceover(product, "YouTube Shorts") or _voiceover_template(product)
    title = f"{product['name']} — the {product['category'].lower()} find under ${_price_bounds(product['price_range'])[1]}"
    description = (
        f"{product['video_angle']}. {product['why_care']}. "
        f"Typical price: {product['price_range']}. "
        f"Search term: “{product['search_term']}”. "
        f"{disclosure_for(product['id'])}"
    )
    script_id = db.insert("youtube_scripts", {
        "product_id": product["id"],
        "title": title[:100],
        "hook": hook,
        "voiceover": voiceover,
        "on_screen_text": (f"{hook}\nTypically {product['price_range']}\n"
                           f"Search: {product['search_term']}"),
        "shot_list": json.dumps(_shot_list(product)),
        "description": description,
        "hashtags": make_hashtags(product, "#shorts"),
        "pinned_comment": (f"🔎 Find it by searching: “{product['search_term']}”. "
                           "Which category should we cover next? "
                           "Prices and availability may change."),
        "cta": "Subscribe for a new under-$100 find every day.",
        "video_length": rng.choice(["30-40 seconds", "40-50 seconds", "50-58 seconds"]),
        "disclosure": disclosure_for(product["id"]),
        "created_at": db.now(),
    })
    return script_id


# ----------------------------------------------------------- video prompts

def generate_video_prompt(product, script_type="", script_id=None):
    rng = _seeded(product["name"] + "prompt" + db.now())
    name_l = product["name"].lower()
    space = data.CATEGORY_SPACE.get(product["category"], "room")
    lo, hi = _price_bounds(product["price_range"])
    prompt_id = db.insert("video_prompts", {
        "product_id": product["id"],
        "script_type": script_type,
        "script_id": script_id,
        "product_visual_prompt": (
            f"Photorealistic {name_l} on a clean minimal surface, soft diffused daylight, "
            "shallow depth of field, premium product-photography look, vertical 9:16, "
            "generic unbranded design, no logos, no text, no faces"),
        "background_prompt": (
            f"A bright modern {space} scene with neutral tones and soft shadows, "
            "slightly blurred for product overlay, vertical 9:16, no people, no brands"),
        "broll_prompt": (
            f"Close-up hands-only footage of someone using a {name_l} in a cozy {space}, "
            "natural movement, warm lighting, smooth slow push-in, 9:16, no faces, no logos"),
        "thumbnail_prompt": (
            f"Eye-catching vertical thumbnail: {name_l} centered with bold negative space "
            f"for text overlay, high contrast, clean background, no brands, no faces"),
        "tiktok_cover_text": f"Under ${hi} {product['category'].lower()} find 👀",
        "youtube_cover_text": f"The ${lo}-${hi} {product['category'].lower()} upgrade",
        "editing_style": rng.choice(data.EDITING_STYLES),
        "music_mood": rng.choice(data.MUSIC_MOODS),
        "pacing": rng.choice(data.PACING_OPTIONS),
        "capcut_notes": (
            "Auto-captions ON with keyword highlights; punch-in zoom at each scene change; "
            "add a subtle shake on the price reveal; keep total cuts under 10; "
            "export 1080x1920 at 30fps."),
        "canva_notes": (
            "Use a 1080x1920 template; bold sans-serif headline at top third; "
            "product image centered with soft drop shadow; price badge bottom-left; "
            "keep to 2 fonts max and one accent color."),
        "created_at": db.now(),
    })
    return prompt_id
