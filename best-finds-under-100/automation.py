"""Automation engine: calendar generation, daily automation, and reports.

Every task can be run manually from the dashboard, or headlessly via
`python run_automation.py` (for Replit Scheduled Deployments / cron).
"""
import json
from datetime import date, datetime, timedelta

import db
import generators
from config import CALENDAR_STATUSES, MONETIZATION_STATUSES, api_status, demo_mode, missing_keys


def _log_run(run_type, details):
    db.insert("automation_runs", {
        "run_type": run_type, "status": "completed",
        "details": json.dumps(details),
        "started_at": db.now(), "finished_at": db.now(),
    })


# ------------------------------------------------------------- calendar

def generate_calendar(days=7, include_pinterest=None):
    """Build a posting plan: one TikTok + one YouTube Short per day, from
    the highest-scoring products that aren't already scheduled."""
    if include_pinterest is None:
        include_pinterest = db.get_setting("pinterest_enabled", "0") == "1"

    scheduled_ids = {r["product_id"] for r in db.query(
        "SELECT DISTINCT product_id FROM content_calendar WHERE scheduled_date >= ?",
        (date.today().isoformat(),))}
    products = [p for p in db.query(
        "SELECT * FROM product_ideas ORDER BY overall_score DESC")
        if p["id"] not in scheduled_ids]
    if not products:
        products = db.query("SELECT * FROM product_ideas ORDER BY overall_score DESC")
    if not products:
        return []

    created = []
    per_day = 2 + (1 if include_pinterest else 0)
    needed = days * per_day
    # Cycle products if the pool is smaller than the plan.
    pool = (products * ((needed // len(products)) + 1))[:needed]

    idx = 0
    for day_offset in range(days):
        post_date = (date.today() + timedelta(days=day_offset + 1)).isoformat()
        platforms = ["TikTok", "YouTube Shorts"] + (["Pinterest"] if include_pinterest else [])
        for platform in platforms:
            product = pool[idx]
            idx += 1
            hooks = generators.make_hooks(product)
            hook = hooks[0]
            tag = {"TikTok": "#tiktokfinds", "YouTube Shorts": "#shorts",
                   "Pinterest": "#pinterestfinds"}[platform]
            item_id = db.insert("content_calendar", {
                "product_id": product["id"],
                "platform": platform,
                "hook": hook,
                "caption": generators.make_caption(product, hook),
                "hashtags": generators.make_hashtags(product, tag),
                "link_or_term": generators.best_link_or_term(product),
                "scheduled_date": post_date,
                "status": "idea",
                "created_at": db.now(),
            })
            created.append(item_id)
    _log_run(f"generate_{days}_day_calendar", {"items_created": len(created)})
    return created


# --------------------------------------------------------------- reports

def build_report_content():
    today = date.today().isoformat()
    top_products = db.query(
        "SELECT name, category, price_range, overall_score FROM product_ideas "
        "ORDER BY overall_score DESC LIMIT 5")
    top_categories = db.query(
        "SELECT category, COUNT(*) AS n, AVG(overall_score) AS avg_score "
        "FROM product_ideas GROUP BY category ORDER BY avg_score DESC LIMIT 5")
    ready = db.count("content_calendar", "status IN ('ready_to_post', 'ready_to_create')")
    link_counts = {label: db.count("monetization_links", "monetization_status = ?", (key,))
                   for key, label in MONETIZATION_STATUSES.items()}
    affiliate_ready = (link_counts.get("Affiliate link added", 0)
                       + link_counts.get("Sponsored link added", 0))

    recommendations = []
    if db.count("product_ideas") < 25:
        recommendations.append("Generate more product ideas — a deeper pool improves calendar quality.")
    if db.count("tiktok_scripts") < db.count("product_ideas"):
        recommendations.append("Several products have no TikTok script yet — run the TikTok generator.")
    if ready == 0:
        recommendations.append("Nothing is marked ready to post — move today's calendar items forward.")
    if affiliate_ready == 0:
        recommendations.append("No affiliate links yet (expected for now) — keep growing the audience; "
                               "apply to Amazon Associates and TikTok Shop once eligible.")
    if demo_mode():
        recommendations.append("Running in demo mode — add OPENAI_API_KEY later for AI-enhanced voiceovers.")
    recommendations.append("Post consistently: 1 TikTok + 1 Short per day beats bursts.")

    return {
        "date": today,
        "new_ideas_today": db.count("product_ideas", "created_at LIKE ?", (f"{today}%",)),
        "tiktok_scripts_today": db.count("tiktok_scripts", "created_at LIKE ?", (f"{today}%",)),
        "youtube_scripts_today": db.count("youtube_scripts", "created_at LIKE ?", (f"{today}%",)),
        "video_prompts_today": db.count("video_prompts", "created_at LIKE ?", (f"{today}%",)),
        "totals": {
            "product_ideas": db.count("product_ideas"),
            "tiktok_scripts": db.count("tiktok_scripts"),
            "youtube_scripts": db.count("youtube_scripts"),
            "video_prompts": db.count("video_prompts"),
            "calendar_items": db.count("content_calendar"),
        },
        "top_products": [dict(r) for r in top_products],
        "top_categories": [
            {"category": r["category"], "count": r["n"], "avg_score": round(r["avg_score"])}
            for r in top_categories],
        "ready_to_post": ready,
        "missing_keys": missing_keys(),
        "monetization": {
            "link_counts": link_counts,
            "readiness": ("Monetization-ready: affiliate links are plugged in."
                          if affiliate_ready else
                          "Audience-building phase: no affiliate links yet. The system is ready "
                          "to accept them the moment your accounts are approved."),
        },
        "recommendations": recommendations,
    }


def generate_daily_report():
    content = build_report_content()
    report_id = db.insert("reports", {
        "report_date": content["date"],
        "content": json.dumps(content),
        "created_at": db.now(),
    })
    _log_run("generate_daily_report", {"report_id": report_id})
    return report_id


# ------------------------------------------------------- daily automation

DAILY_TASKS = [
    "Generate 10 new product ideas",
    "Score all product ideas",
    "Pick top 5 products to promote",
    "Generate 5 TikTok scripts",
    "Generate 5 YouTube Shorts scripts",
    "Generate video prompts for each script",
    "Generate captions and hashtags",
    "Generate 7-day content calendar",
    "Generate daily report",
]


def run_daily_automation():
    """The full daily pipeline. Safe to run repeatedly."""
    summary = {}

    ideas = generators.generate_product_ideas(10)
    summary["new_product_ideas"] = len(ideas)

    summary["products_rescored"] = generators.rescore_all_products()
    top_ids = generators.pick_top_products(5)
    summary["top_products_picked"] = len(top_ids)

    top_products = [db.query("SELECT * FROM product_ideas WHERE id = ?", (pid,), one=True)
                    for pid in top_ids]
    tiktok_ids, youtube_ids, prompt_ids = [], [], []
    for product in top_products:
        if product is None:
            continue
        t_id = generators.generate_tiktok_script(product)
        y_id = generators.generate_youtube_script(product)
        tiktok_ids.append(t_id)
        youtube_ids.append(y_id)
        prompt_ids.append(generators.generate_video_prompt(product, "tiktok", t_id))
        prompt_ids.append(generators.generate_video_prompt(product, "youtube", y_id))
    summary["tiktok_scripts"] = len(tiktok_ids)
    summary["youtube_scripts"] = len(youtube_ids)
    summary["video_prompts"] = len(prompt_ids)
    summary["captions_and_hashtags"] = len(tiktok_ids) + len(youtube_ids)

    summary["calendar_items"] = len(generate_calendar(7))
    summary["report_id"] = generate_daily_report()

    _log_run("run_daily_automation", summary)
    return summary


def todays_tasks_status():
    """Which daily tasks have run today (for the dashboard checklist)."""
    today = date.today().isoformat()
    ran_daily = db.count("automation_runs",
                         "run_type = 'run_daily_automation' AND started_at LIKE ?",
                         (f"{today}%",)) > 0
    checks = {
        "Generate 10 new product ideas": ran_daily or db.count(
            "product_ideas", "created_at LIKE ? AND source = 'generated'", (f"{today}%",)) >= 1,
        "Score all product ideas": ran_daily,
        "Pick top 5 products to promote": ran_daily or db.count("product_ideas", "featured = 1") > 0,
        "Generate 5 TikTok scripts": db.count("tiktok_scripts", "created_at LIKE ?", (f"{today}%",)) >= 5,
        "Generate 5 YouTube Shorts scripts": db.count("youtube_scripts", "created_at LIKE ?", (f"{today}%",)) >= 5,
        "Generate video prompts for each script": db.count("video_prompts", "created_at LIKE ?", (f"{today}%",)) >= 1,
        "Generate captions and hashtags": db.count("tiktok_scripts", "created_at LIKE ?", (f"{today}%",)) >= 1,
        "Generate 7-day content calendar": db.count("content_calendar", "created_at LIKE ?", (f"{today}%",)) >= 1,
        "Generate daily report": db.count("reports", "created_at LIKE ?", (f"{today}%",)) >= 1,
    }
    return [(task, checks.get(task, False)) for task in DAILY_TASKS]
