"""App configuration. Loads environment variables; everything is optional (demo mode)."""
import os

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.environ.get("DATABASE_PATH", os.path.join(BASE_DIR, "bestfinds.db"))

BRAND_NAME = "Best Finds Under $100"

# Optional API keys — the app works fully in demo mode without any of these.
API_KEYS = {
    "OPENAI_API_KEY": os.environ.get("OPENAI_API_KEY", ""),
    "AMAZON_ASSOCIATE_TAG": os.environ.get("AMAZON_ASSOCIATE_TAG", ""),
    "TIKTOK_ACCESS_TOKEN": os.environ.get("TIKTOK_ACCESS_TOKEN", ""),
    "YOUTUBE_API_KEY": os.environ.get("YOUTUBE_API_KEY", ""),
    "YOUTUBE_CLIENT_ID": os.environ.get("YOUTUBE_CLIENT_ID", ""),
    "YOUTUBE_CLIENT_SECRET": os.environ.get("YOUTUBE_CLIENT_SECRET", ""),
    "PINTEREST_ACCESS_TOKEN": os.environ.get("PINTEREST_ACCESS_TOKEN", ""),
    "PEXELS_API_KEY": os.environ.get("PEXELS_API_KEY", ""),
}

SECRET_KEY = os.environ.get("SECRET_KEY", "bestfinds-dev-secret")


def api_status():
    """Which integrations are configured. Missing keys never block features."""
    return {
        "OpenAI (AI-enhanced writing)": bool(API_KEYS["OPENAI_API_KEY"]),
        "Amazon Associates tag": bool(API_KEYS["AMAZON_ASSOCIATE_TAG"]),
        "TikTok access token": bool(API_KEYS["TIKTOK_ACCESS_TOKEN"]),
        "YouTube API key": bool(API_KEYS["YOUTUBE_API_KEY"]),
        "YouTube OAuth client": bool(API_KEYS["YOUTUBE_CLIENT_ID"] and API_KEYS["YOUTUBE_CLIENT_SECRET"]),
        "Pinterest access token": bool(API_KEYS["PINTEREST_ACCESS_TOKEN"]),
        "Pexels (free stock visuals in videos)": bool(API_KEYS["PEXELS_API_KEY"]),
    }


def missing_keys():
    return [name for name, ok in api_status().items() if not ok]


def demo_mode():
    """Demo mode = no OpenAI key. Template-based generation is used instead."""
    return not API_KEYS["OPENAI_API_KEY"]


# Compliance / disclosure copy (also editable in Settings)
DEFAULT_DISCLOSURE = "Product ideas are for discovery and inspiration. Prices and availability may change."
AFFILIATE_DISCLOSURE = "As an affiliate, we may earn from qualifying purchases. Prices and availability may change."

CONTENT_RULES = [
    "Do not claim guaranteed earnings or guaranteed results.",
    "Do not fabricate reviews or say “I tested this” unless it was actually tested.",
    "Do not copy Amazon or retailer product descriptions — write original copy.",
    "Do not scrape restricted websites.",
    "Do not use copyrighted characters, celebrity likenesses, or brand logos without permission.",
    "Do not make medical, financial, or safety claims about products.",
    "Do not generate misleading product claims.",
    "Always note that prices and availability may change.",
    "Use the affiliate disclosure only when affiliate links are actually used.",
    "Create original content that adds value.",
]

CATEGORIES = [
    "Home finds",
    "Apartment upgrades",
    "Tech accessories",
    "Car gadgets",
    "Pet products",
    "Travel essentials",
    "Gift ideas",
    "Desk setup",
    "Kitchen gadgets",
    "Fitness accessories",
]

MONETIZATION_STATUSES = {
    "no_link": "No link yet",
    "search_link": "Search link only",
    "manual_link": "Manual product link added",
    "affiliate_link": "Affiliate link added",
    "sponsored_link": "Sponsored link added",
}

CALENDAR_STATUSES = {
    "idea": "Idea",
    "script_ready": "Script ready",
    "prompt_ready": "Video prompt ready",
    "ready_to_create": "Ready to create",
    "ready_to_post": "Ready to post",
    "posted": "Posted",
    "needs_review": "Needs review",
}
