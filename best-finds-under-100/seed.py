"""Demo-mode seeding. Runs automatically on first launch when the DB is empty.

Seeds: 25 product ideas (with placeholder search links), 10 TikTok scripts,
10 YouTube Shorts scripts, 10 video prompts, a 7-day content calendar,
1 daily report, and default settings.
"""
import db
import generators
import automation
from config import AFFILIATE_DISCLOSURE, DEFAULT_DISCLOSURE


DEFAULT_SETTINGS = {
    "brand_name": "Best Finds Under $100",
    "tagline": "Daily affordable finds for your home, desk, car, pets, and more.",
    "tiktok_handle": "@bestfindsunder100",
    "youtube_handle": "@bestfindsunder100",
    "pinterest_handle": "",
    "pinterest_enabled": "0",
    "default_disclosure": DEFAULT_DISCLOSURE,
    "affiliate_disclosure": AFFILIATE_DISCLOSURE,
    "posting_time": "18:00",
}


def seed_if_empty():
    db.init_db()

    for key, value in DEFAULT_SETTINGS.items():
        if db.get_setting(key, None) is None:
            db.set_setting(key, value)

    if db.count("product_ideas") > 0:
        return False

    # 25 sample product ideas across all categories (placeholder links included)
    generators.generate_product_ideas(25, source="demo")
    generators.rescore_all_products()
    generators.pick_top_products(5)

    # 10 sample TikTok scripts, 10 YouTube Shorts scripts, 10 video prompts
    products = db.query("SELECT * FROM product_ideas ORDER BY overall_score DESC LIMIT 10")
    for i, product in enumerate(products):
        t_id = generators.generate_tiktok_script(product)
        generators.generate_youtube_script(product)
        generators.generate_video_prompt(product, "tiktok", t_id)

    # 7-day content calendar + 1 sample daily report
    automation.generate_calendar(7)
    automation.generate_daily_report()
    return True
