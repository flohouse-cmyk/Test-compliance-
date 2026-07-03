"""Best Finds Under $100 — faceless short-form content engine.

Flask app: admin dashboard + generators + automation + public link hub.
Works fully in demo mode with zero API keys.
"""
import json

from flask import (Flask, abort, flash, redirect, render_template, request,
                   send_from_directory, url_for)

import automation
import db
import generators
import renderer
import seed
from config import (CALENDAR_STATUSES, CATEGORIES, CONTENT_RULES,
                    MONETIZATION_STATUSES, SECRET_KEY, api_status, demo_mode)

app = Flask(__name__)
app.secret_key = SECRET_KEY

seed.seed_if_empty()


# ------------------------------------------------------------ template env

@app.template_filter("fromjson")
def fromjson_filter(text):
    return db.loads(text, [])


@app.context_processor
def inject_globals():
    return {
        "brand_name": db.get_setting("brand_name", "Best Finds Under $100"),
        "demo_mode": demo_mode(),
        "categories": CATEGORIES,
        "monetization_statuses": MONETIZATION_STATUSES,
        "calendar_statuses": CALENDAR_STATUSES,
    }


def get_or_404(table, row_id):
    row = db.query(f"SELECT * FROM {table} WHERE id = ?", (row_id,), one=True)
    if row is None:
        abort(404)
    return row


# --------------------------------------------------------------- dashboard

@app.route("/")
def dashboard():
    stats = {
        "products": db.count("product_ideas"),
        "tiktok_scripts": db.count("tiktok_scripts"),
        "youtube_scripts": db.count("youtube_scripts"),
        "video_prompts": db.count("video_prompts"),
        "calendar_items": db.count("content_calendar"),
    }
    stats["video_ideas"] = stats["tiktok_scripts"] + stats["youtube_scripts"]
    stats["captions"] = stats["tiktok_scripts"] + stats["youtube_scripts"]

    top_categories = db.query(
        "SELECT category, COUNT(*) AS n, ROUND(AVG(overall_score)) AS avg_score "
        "FROM product_ideas GROUP BY category ORDER BY n DESC, avg_score DESC LIMIT 5")
    recent_tiktok = db.query(
        "SELECT t.id, t.title, t.created_at, p.category FROM tiktok_scripts t "
        "JOIN product_ideas p ON p.id = t.product_id ORDER BY t.id DESC LIMIT 5")
    recent_youtube = db.query(
        "SELECT y.id, y.title, y.created_at, p.category FROM youtube_scripts y "
        "JOIN product_ideas p ON p.id = y.product_id ORDER BY y.id DESC LIMIT 5")
    latest_report = db.query("SELECT * FROM reports ORDER BY id DESC LIMIT 1", one=True)
    latest_report_content = db.loads(latest_report["content"], {}) if latest_report else None
    recent_runs = db.query("SELECT * FROM automation_runs ORDER BY id DESC LIMIT 5")

    return render_template(
        "dashboard.html", stats=stats, top_categories=top_categories,
        recent_tiktok=recent_tiktok, recent_youtube=recent_youtube,
        api_status=api_status(), tasks=automation.todays_tasks_status(),
        latest_report=latest_report, latest_report_content=latest_report_content,
        recent_runs=recent_runs)


# ---------------------------------------------------------------- products

@app.route("/products")
def products():
    category = request.args.get("category", "")
    sort = request.args.get("sort", "score")
    order = {"score": "overall_score DESC", "newest": "id DESC",
             "name": "name ASC"}.get(sort, "overall_score DESC")
    if category:
        rows = db.query(f"SELECT * FROM product_ideas WHERE category = ? ORDER BY {order}",
                        (category,))
    else:
        rows = db.query(f"SELECT * FROM product_ideas ORDER BY {order}")
    return render_template("products.html", products=rows,
                           active_category=category, sort=sort)


@app.route("/products/new", methods=["GET", "POST"])
def product_new():
    if request.method == "POST":
        form = request.form
        name = form.get("name", "").strip()
        if not name:
            flash("Product name is required.", "error")
            return render_template("product_form.html", product=None, form=form)
        scores = generators.score_product(name, form.get("category", CATEGORIES[0]))
        term = form.get("search_term", "").strip() or generators.search_term_for(name, 100)
        product_id = db.insert("product_ideas", {
            "name": name,
            "category": form.get("category", CATEGORIES[0]),
            "price_range": form.get("price_range", "$10-$100").strip() or "$10-$100",
            "search_term": term,
            "why_care": form.get("why_care", "").strip(),
            "target_audience": form.get("target_audience", "").strip(),
            "problem_solved": form.get("problem_solved", "").strip(),
            "video_angle": form.get("video_angle", "").strip(),
            **scores, "source": "manual", "created_at": db.now(),
        })
        db.insert("monetization_links", {
            "product_id": product_id, "search_term": term,
            "placeholder_link": generators.placeholder_link_for(term),
            "monetization_status": "search_link",
            "created_at": db.now(), "updated_at": db.now(),
        })
        flash("Product idea added.", "ok")
        return redirect(url_for("product_detail", product_id=product_id))
    return render_template("product_form.html", product=None, form={})


@app.route("/products/<int:product_id>")
def product_detail(product_id):
    product = get_or_404("product_ideas", product_id)
    links = db.query("SELECT * FROM monetization_links WHERE product_id = ? ORDER BY id DESC",
                     (product_id,))
    tiktoks = db.query("SELECT * FROM tiktok_scripts WHERE product_id = ? ORDER BY id DESC",
                       (product_id,))
    youtubes = db.query("SELECT * FROM youtube_scripts WHERE product_id = ? ORDER BY id DESC",
                        (product_id,))
    prompts = db.query("SELECT * FROM video_prompts WHERE product_id = ? ORDER BY id DESC",
                       (product_id,))
    return render_template("product_detail.html", product=product, links=links,
                           tiktoks=tiktoks, youtubes=youtubes, prompts=prompts,
                           disclosure=generators.disclosure_for(product_id))


@app.route("/products/<int:product_id>/edit", methods=["GET", "POST"])
def product_edit(product_id):
    product = get_or_404("product_ideas", product_id)
    if request.method == "POST":
        form = request.form
        db.update("product_ideas", product_id, {
            "name": form.get("name", product["name"]).strip() or product["name"],
            "category": form.get("category", product["category"]),
            "price_range": form.get("price_range", "").strip() or product["price_range"],
            "search_term": form.get("search_term", "").strip() or product["search_term"],
            "why_care": form.get("why_care", "").strip(),
            "target_audience": form.get("target_audience", "").strip(),
            "problem_solved": form.get("problem_solved", "").strip(),
            "video_angle": form.get("video_angle", "").strip(),
            "featured": 1 if form.get("featured") else 0,
        })
        flash("Product idea updated.", "ok")
        return redirect(url_for("product_detail", product_id=product_id))
    return render_template("product_form.html", product=product, form=product)


@app.route("/products/<int:product_id>/delete", methods=["POST"])
def product_delete(product_id):
    get_or_404("product_ideas", product_id)
    db.execute("DELETE FROM product_ideas WHERE id = ?", (product_id,))
    flash("Product idea deleted (with its links, scripts, and prompts).", "ok")
    return redirect(url_for("products"))


@app.route("/products/<int:product_id>/generate/<content_type>", methods=["POST"])
def product_generate(product_id, content_type):
    product = get_or_404("product_ideas", product_id)
    if content_type == "tiktok":
        script_id = generators.generate_tiktok_script(product)
        flash("TikTok script generated.", "ok")
        return redirect(url_for("tiktok_script_detail", script_id=script_id))
    if content_type == "youtube":
        script_id = generators.generate_youtube_script(product)
        flash("YouTube Shorts script generated.", "ok")
        return redirect(url_for("youtube_script_detail", script_id=script_id))
    if content_type == "prompt":
        prompt_id = generators.generate_video_prompt(product)
        flash("Video prompt generated.", "ok")
        return redirect(url_for("prompt_detail", prompt_id=prompt_id))
    abort(404)


# ------------------------------------------------------------ link manager

@app.route("/links")
def links():
    rows = db.query(
        "SELECT l.*, p.name AS product_name, p.category FROM monetization_links l "
        "JOIN product_ideas p ON p.id = l.product_id ORDER BY l.updated_at DESC")
    counts = {key: db.count("monetization_links", "monetization_status = ?", (key,))
              for key in MONETIZATION_STATUSES}
    return render_template("links.html", links=rows, counts=counts)


@app.route("/links/<int:link_id>/edit", methods=["GET", "POST"])
def link_edit(link_id):
    link = get_or_404("monetization_links", link_id)
    product = get_or_404("product_ideas", link["product_id"])
    if request.method == "POST":
        form = request.form
        status = form.get("monetization_status", link["monetization_status"])
        if status not in MONETIZATION_STATUSES:
            status = "no_link"
        db.update("monetization_links", link_id, {
            "search_term": form.get("search_term", "").strip(),
            "placeholder_link": form.get("placeholder_link", "").strip(),
            "manual_link": form.get("manual_link", "").strip(),
            "affiliate_link": form.get("affiliate_link", "").strip(),
            "sponsored_link": form.get("sponsored_link", "").strip(),
            "digital_product_link": form.get("digital_product_link", "").strip(),
            "platform": form.get("platform", "").strip(),
            "campaign_name": form.get("campaign_name", "").strip(),
            "notes": form.get("notes", "").strip(),
            "monetization_status": status,
            "updated_at": db.now(),
        })
        flash("Link updated.", "ok")
        return redirect(url_for("links"))
    return render_template("link_form.html", link=link, product=product)


# ----------------------------------------------------------------- scripts

@app.route("/scripts/tiktok")
def tiktok_scripts():
    rows = db.query(
        "SELECT t.*, p.name AS product_name, p.category FROM tiktok_scripts t "
        "JOIN product_ideas p ON p.id = t.product_id ORDER BY t.id DESC")
    return render_template("scripts_list.html", scripts=rows, platform="TikTok",
                           detail_endpoint="tiktok_script_detail")


@app.route("/scripts/tiktok/<int:script_id>")
def tiktok_script_detail(script_id):
    script = get_or_404("tiktok_scripts", script_id)
    product = get_or_404("product_ideas", script["product_id"])
    return render_template("script_tiktok_detail.html", script=script, product=product)


@app.route("/scripts/tiktok/<int:script_id>/delete", methods=["POST"])
def tiktok_script_delete(script_id):
    get_or_404("tiktok_scripts", script_id)
    db.execute("DELETE FROM tiktok_scripts WHERE id = ?", (script_id,))
    flash("TikTok script deleted.", "ok")
    return redirect(url_for("tiktok_scripts"))


@app.route("/scripts/youtube")
def youtube_scripts():
    rows = db.query(
        "SELECT y.*, p.name AS product_name, p.category FROM youtube_scripts y "
        "JOIN product_ideas p ON p.id = y.product_id ORDER BY y.id DESC")
    return render_template("scripts_list.html", scripts=rows, platform="YouTube Shorts",
                           detail_endpoint="youtube_script_detail")


@app.route("/scripts/youtube/<int:script_id>")
def youtube_script_detail(script_id):
    script = get_or_404("youtube_scripts", script_id)
    product = get_or_404("product_ideas", script["product_id"])
    return render_template("script_youtube_detail.html", script=script, product=product)


@app.route("/scripts/youtube/<int:script_id>/delete", methods=["POST"])
def youtube_script_delete(script_id):
    get_or_404("youtube_scripts", script_id)
    db.execute("DELETE FROM youtube_scripts WHERE id = ?", (script_id,))
    flash("YouTube Shorts script deleted.", "ok")
    return redirect(url_for("youtube_scripts"))


# ----------------------------------------------------------- video prompts

@app.route("/prompts")
def prompts():
    rows = db.query(
        "SELECT v.*, p.name AS product_name, p.category FROM video_prompts v "
        "JOIN product_ideas p ON p.id = v.product_id ORDER BY v.id DESC")
    return render_template("prompts.html", prompts=rows)


@app.route("/prompts/<int:prompt_id>")
def prompt_detail(prompt_id):
    prompt = get_or_404("video_prompts", prompt_id)
    product = get_or_404("product_ideas", prompt["product_id"])
    return render_template("prompt_detail.html", prompt=prompt, product=product)


# ------------------------------------------------------------ rendered videos

@app.route("/videos")
def videos():
    rows = db.query(
        "SELECT v.*, p.name AS product_name, p.category FROM rendered_videos v "
        "JOIN product_ideas p ON p.id = v.product_id ORDER BY v.id DESC")
    return render_template("videos.html", videos=rows,
                           ffmpeg_ok=renderer.ffmpeg_available())


@app.route("/videos/diagnose")
def video_diagnose():
    return render_template("diagnose.html", checks=renderer.diagnose())


@app.route("/render/<script_type>/<int:script_id>", methods=["POST"])
def render_video(script_type, script_id):
    if script_type not in ("tiktok", "youtube"):
        abort(404)
    video_id = renderer.render_script(script_type, script_id)
    video = db.query("SELECT * FROM rendered_videos WHERE id = ?", (video_id,), one=True)
    if video["status"] == "done":
        flash(f"Video rendered ({video['duration_seconds']}s, voice: {video['voice']}). "
              "Download it from the Videos page.", "ok")
    else:
        flash(f"Render failed: {video['error']}", "error")
    return redirect(url_for("videos"))


@app.route("/videos/render-today", methods=["POST"])
def render_today():
    ids = renderer.render_todays_scripts(limit=6)
    done = db.count("rendered_videos", "status = 'done' AND id IN ({})".format(
        ",".join("?" * len(ids))), tuple(ids)) if ids else 0
    if not ids:
        flash("No unrendered scripts from today — generate scripts first "
              "(Run Daily Automation).", "error")
    elif done == len(ids):
        flash(f"Rendered {done} video(s). Download them below.", "ok")
    else:
        flash(f"Rendered {done} of {len(ids)} — check failed rows below for details.",
              "error")
    return redirect(url_for("videos"))


@app.route("/videos/<int:video_id>/download")
def video_download(video_id):
    video = get_or_404("rendered_videos", video_id)
    if video["status"] != "done" or not video["filename"]:
        abort(404)
    return send_from_directory(renderer.RENDER_DIR, video["filename"], as_attachment=True)


@app.route("/videos/<int:video_id>/watch")
def video_watch(video_id):
    video = get_or_404("rendered_videos", video_id)
    if video["status"] != "done" or not video["filename"]:
        abort(404)
    return send_from_directory(renderer.RENDER_DIR, video["filename"])


@app.route("/videos/<int:video_id>/delete", methods=["POST"])
def video_delete(video_id):
    video = get_or_404("rendered_videos", video_id)
    if video["filename"]:
        try:
            import os
            os.unlink(os.path.join(renderer.RENDER_DIR, video["filename"]))
        except OSError:
            pass
    db.execute("DELETE FROM rendered_videos WHERE id = ?", (video_id,))
    flash("Video deleted.", "ok")
    return redirect(url_for("videos"))


# ---------------------------------------------------------------- calendar

@app.route("/calendar")
def calendar():
    rows = db.query(
        "SELECT c.*, p.name AS product_name, p.category FROM content_calendar c "
        "JOIN product_ideas p ON p.id = c.product_id "
        "ORDER BY c.scheduled_date ASC, c.id ASC")
    grouped = {}
    for row in rows:
        grouped.setdefault(row["scheduled_date"], []).append(row)
    return render_template("calendar.html", grouped=grouped)


@app.route("/calendar/<int:item_id>/status", methods=["POST"])
def calendar_status(item_id):
    get_or_404("content_calendar", item_id)
    status = request.form.get("status", "idea")
    if status in CALENDAR_STATUSES:
        db.update("content_calendar", item_id, {"status": status})
        flash("Calendar item updated.", "ok")
    return redirect(url_for("calendar"))


@app.route("/calendar/<int:item_id>/delete", methods=["POST"])
def calendar_delete(item_id):
    get_or_404("content_calendar", item_id)
    db.execute("DELETE FROM content_calendar WHERE id = ?", (item_id,))
    flash("Calendar item removed.", "ok")
    return redirect(url_for("calendar"))


# ----------------------------------------------------------------- reports

@app.route("/reports")
def reports():
    rows = db.query("SELECT * FROM reports ORDER BY id DESC")
    return render_template("reports.html", reports=rows)


@app.route("/reports/<int:report_id>")
def report_detail(report_id):
    report = get_or_404("reports", report_id)
    return render_template("report_detail.html", report=report,
                           content=db.loads(report["content"], {}))


# -------------------------------------------------------------- automation

AUTOMATION_ACTIONS = {
    "daily": ("Daily automation", automation.run_daily_automation),
    "ideas": ("Product idea generation", lambda: {"new_product_ideas": len(generators.generate_product_ideas(10))}),
    "tiktok": ("TikTok script generation", None),   # handled below
    "youtube": ("YouTube script generation", None),
    "prompts": ("Video prompt generation", None),
    "calendar7": ("7-day calendar", lambda: {"calendar_items": len(automation.generate_calendar(7))}),
    "calendar30": ("30-day calendar", lambda: {"calendar_items": len(automation.generate_calendar(30))}),
    "report": ("Daily report", lambda: {"report_id": automation.generate_daily_report()}),
}


def _top_products(limit=5):
    return db.query("SELECT * FROM product_ideas ORDER BY overall_score DESC LIMIT ?", (limit,))


@app.route("/automation/<action>", methods=["POST"])
def run_automation(action):
    if action not in AUTOMATION_ACTIONS:
        abort(404)
    label, fn = AUTOMATION_ACTIONS[action]
    if action == "tiktok":
        ids = [generators.generate_tiktok_script(p) for p in _top_products()]
        summary = {"tiktok_scripts": len(ids)}
    elif action == "youtube":
        ids = [generators.generate_youtube_script(p) for p in _top_products()]
        summary = {"youtube_scripts": len(ids)}
    elif action == "prompts":
        ids = [generators.generate_video_prompt(p) for p in _top_products()]
        summary = {"video_prompts": len(ids)}
    else:
        summary = fn()
    if action != "daily":  # daily logs itself
        db.insert("automation_runs", {
            "run_type": action, "status": "completed",
            "details": json.dumps(summary),
            "started_at": db.now(), "finished_at": db.now(),
        })
    parts = ", ".join(f"{k.replace('_', ' ')}: {v}" for k, v in summary.items())
    flash(f"{label} finished — {parts}.", "ok")
    if action == "report" or action == "daily":
        return redirect(url_for("reports"))
    return redirect(request.referrer or url_for("dashboard"))


# ---------------------------------------------------------------- settings

SETTING_FIELDS = ["brand_name", "tagline", "tiktok_handle", "youtube_handle",
                  "pinterest_handle", "posting_time",
                  "default_disclosure", "affiliate_disclosure"]


@app.route("/settings", methods=["GET", "POST"])
def settings():
    if request.method == "POST":
        for field in SETTING_FIELDS:
            if field in request.form:
                db.set_setting(field, request.form[field].strip())
        db.set_setting("pinterest_enabled", "1" if request.form.get("pinterest_enabled") else "0")
        flash("Settings saved.", "ok")
        return redirect(url_for("settings"))
    values = {field: db.get_setting(field, "") for field in SETTING_FIELDS}
    values["pinterest_enabled"] = db.get_setting("pinterest_enabled", "0")
    return render_template("settings.html", values=values,
                           api_status=api_status(), content_rules=CONTENT_RULES)


# ------------------------------------------------------------- public hub

def _hub_context():
    return {
        "tagline": db.get_setting("tagline", ""),
        "tiktok_handle": db.get_setting("tiktok_handle", ""),
        "youtube_handle": db.get_setting("youtube_handle", ""),
        "pinterest_handle": db.get_setting("pinterest_handle", ""),
        "pinterest_enabled": db.get_setting("pinterest_enabled", "0") == "1",
        "has_affiliate": db.count(
            "monetization_links",
            "monetization_status IN ('affiliate_link', 'sponsored_link')") > 0,
    }


def _hub_link(product):
    return generators.best_link_or_term(product)


@app.route("/hub")
def hub_home():
    featured = db.query(
        "SELECT * FROM product_ideas WHERE featured = 1 ORDER BY overall_score DESC LIMIT 6")
    if not featured:
        featured = db.query("SELECT * FROM product_ideas ORDER BY overall_score DESC LIMIT 6")
    cat_counts = db.query(
        "SELECT category, COUNT(*) AS n FROM product_ideas GROUP BY category ORDER BY n DESC")
    featured_links = [(p, _hub_link(p)) for p in featured]
    return render_template("hub/home.html", featured=featured_links,
                           cat_counts=cat_counts, **_hub_context())


@app.route("/hub/category/<category>")
def hub_category(category):
    if category not in CATEGORIES:
        abort(404)
    products = db.query(
        "SELECT * FROM product_ideas WHERE category = ? ORDER BY overall_score DESC",
        (category,))
    product_links = [(p, _hub_link(p)) for p in products]
    return render_template("hub/category.html", category=category,
                           products=product_links, **_hub_context())


@app.route("/hub/disclosure")
def hub_disclosure():
    ctx = _hub_context()
    disclosure = (db.get_setting("affiliate_disclosure") if ctx["has_affiliate"]
                  else db.get_setting("default_disclosure"))
    return render_template("hub/disclosure.html", disclosure=disclosure, **ctx)


@app.errorhandler(404)
def not_found(_error):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
