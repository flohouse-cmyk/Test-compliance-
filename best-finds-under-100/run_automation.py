"""Headless daily automation for Replit Scheduled Deployments (or cron).

Usage:  python run_automation.py

Runs the full daily pipeline: generates product ideas, scores them, picks
the top 5, generates TikTok + YouTube Shorts scripts, video prompts,
captions/hashtags, a 7-day calendar, and the daily report.
"""
import json

import automation
import seed


def main():
    seed.seed_if_empty()
    summary = automation.run_daily_automation()
    print("Daily automation complete:")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
