"""SQLite helpers: connection, schema, and small query utilities."""
import json
import sqlite3
from datetime import datetime

from config import DB_PATH

SCHEMA = """
CREATE TABLE IF NOT EXISTS product_ideas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    price_range TEXT NOT NULL,
    search_term TEXT NOT NULL,
    why_care TEXT NOT NULL,
    target_audience TEXT NOT NULL,
    problem_solved TEXT NOT NULL,
    video_angle TEXT NOT NULL,
    viral_score INTEGER NOT NULL DEFAULT 0,
    visual_score INTEGER NOT NULL DEFAULT 0,
    giftability_score INTEGER NOT NULL DEFAULT 0,
    impulse_score INTEGER NOT NULL DEFAULT 0,
    tiktok_score INTEGER NOT NULL DEFAULT 0,
    youtube_score INTEGER NOT NULL DEFAULT 0,
    overall_score INTEGER NOT NULL DEFAULT 0,
    featured INTEGER NOT NULL DEFAULT 0,
    source TEXT NOT NULL DEFAULT 'generated',
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS monetization_links (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER NOT NULL REFERENCES product_ideas(id) ON DELETE CASCADE,
    search_term TEXT NOT NULL DEFAULT '',
    placeholder_link TEXT NOT NULL DEFAULT '',
    manual_link TEXT NOT NULL DEFAULT '',
    affiliate_link TEXT NOT NULL DEFAULT '',
    sponsored_link TEXT NOT NULL DEFAULT '',
    digital_product_link TEXT NOT NULL DEFAULT '',
    platform TEXT NOT NULL DEFAULT '',
    campaign_name TEXT NOT NULL DEFAULT '',
    notes TEXT NOT NULL DEFAULT '',
    monetization_status TEXT NOT NULL DEFAULT 'no_link',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS tiktok_scripts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER NOT NULL REFERENCES product_ideas(id) ON DELETE CASCADE,
    title TEXT NOT NULL,
    hooks TEXT NOT NULL,             -- JSON list of 5 hook options
    voiceover TEXT NOT NULL,
    on_screen_text TEXT NOT NULL,
    shot_list TEXT NOT NULL,         -- JSON list of scenes
    caption TEXT NOT NULL,
    hashtags TEXT NOT NULL,
    cta TEXT NOT NULL,
    video_length TEXT NOT NULL,
    background_style TEXT NOT NULL,
    ai_prompts TEXT NOT NULL,        -- JSON list of image/video prompts
    disclosure TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS youtube_scripts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER NOT NULL REFERENCES product_ideas(id) ON DELETE CASCADE,
    title TEXT NOT NULL,
    hook TEXT NOT NULL,
    voiceover TEXT NOT NULL,
    on_screen_text TEXT NOT NULL,
    shot_list TEXT NOT NULL,         -- JSON list of scenes
    description TEXT NOT NULL,
    hashtags TEXT NOT NULL,
    pinned_comment TEXT NOT NULL,
    cta TEXT NOT NULL,
    video_length TEXT NOT NULL,
    disclosure TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS video_prompts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER NOT NULL REFERENCES product_ideas(id) ON DELETE CASCADE,
    script_type TEXT NOT NULL DEFAULT '',   -- 'tiktok' | 'youtube' | ''
    script_id INTEGER,
    product_visual_prompt TEXT NOT NULL,
    background_prompt TEXT NOT NULL,
    broll_prompt TEXT NOT NULL,
    thumbnail_prompt TEXT NOT NULL,
    tiktok_cover_text TEXT NOT NULL,
    youtube_cover_text TEXT NOT NULL,
    editing_style TEXT NOT NULL,
    music_mood TEXT NOT NULL,
    pacing TEXT NOT NULL,
    capcut_notes TEXT NOT NULL,
    canva_notes TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS rendered_videos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER NOT NULL REFERENCES product_ideas(id) ON DELETE CASCADE,
    script_type TEXT NOT NULL,       -- 'tiktok' | 'youtube'
    script_id INTEGER NOT NULL,
    filename TEXT NOT NULL DEFAULT '',
    duration_seconds REAL NOT NULL DEFAULT 0,
    voice TEXT NOT NULL DEFAULT '',
    status TEXT NOT NULL DEFAULT 'rendering',  -- rendering | done | failed
    error TEXT NOT NULL DEFAULT '',
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS content_calendar (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER NOT NULL REFERENCES product_ideas(id) ON DELETE CASCADE,
    platform TEXT NOT NULL,          -- 'TikTok' | 'YouTube Shorts' | 'Pinterest'
    hook TEXT NOT NULL DEFAULT '',
    caption TEXT NOT NULL DEFAULT '',
    hashtags TEXT NOT NULL DEFAULT '',
    link_or_term TEXT NOT NULL DEFAULT '',
    scheduled_date TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'idea',
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS automation_runs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    run_type TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'completed',
    details TEXT NOT NULL DEFAULT '{}',   -- JSON summary of what was created
    started_at TEXT NOT NULL,
    finished_at TEXT
);

CREATE TABLE IF NOT EXISTS reports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    report_date TEXT NOT NULL,
    content TEXT NOT NULL,           -- JSON payload rendered on the report page
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS settings (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL
);
"""


def now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = get_db()
    conn.executescript(SCHEMA)
    conn.commit()
    conn.close()


def query(sql, params=(), one=False):
    conn = get_db()
    cur = conn.execute(sql, params)
    rows = cur.fetchall()
    conn.close()
    if one:
        return rows[0] if rows else None
    return rows


def execute(sql, params=()):
    conn = get_db()
    cur = conn.execute(sql, params)
    conn.commit()
    last_id = cur.lastrowid
    conn.close()
    return last_id


def insert(table, data):
    keys = ", ".join(data.keys())
    marks = ", ".join(["?"] * len(data))
    return execute(f"INSERT INTO {table} ({keys}) VALUES ({marks})", tuple(data.values()))


def update(table, row_id, data):
    sets = ", ".join(f"{k} = ?" for k in data)
    execute(f"UPDATE {table} SET {sets} WHERE id = ?", (*data.values(), row_id))


def count(table, where="", params=()):
    sql = f"SELECT COUNT(*) AS c FROM {table}"
    if where:
        sql += f" WHERE {where}"
    return query(sql, params, one=True)["c"]


def get_setting(key, default=""):
    row = query("SELECT value FROM settings WHERE key = ?", (key,), one=True)
    return row["value"] if row else default


def set_setting(key, value):
    execute(
        "INSERT INTO settings (key, value) VALUES (?, ?) "
        "ON CONFLICT(key) DO UPDATE SET value = excluded.value",
        (key, value),
    )


def loads(text, default=None):
    try:
        return json.loads(text)
    except (TypeError, ValueError):
        return default if default is not None else []
