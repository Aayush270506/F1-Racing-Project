"""Flask front end for the Formula 1 Race Intelligence Tableau dashboard and story."""
import re

from flask import Flask, render_template

import config

app = Flask(__name__)

# Headline figures, matching the KPI cards on the Tableau dashboard.
KPIS = [
    {"value": "10", "label": "Competing Teams"},
    {"value": "17", "label": "Seasons in Play"},
    {"value": "6,464", "label": "Race Outcomes Logged"},
    {"value": "29", "label": "Circuits Showcased"},
]

VISUALS = [
    {"title": "KPI Summary Cards", "chart": "KPI cards",
     "text": "Competing teams, seasons, race outcomes and circuits at a glance."},
    {"title": "Global Driver Distribution Across Grand Prix Nations", "chart": "Geographic map",
     "text": "Where the races are held and how driver entries spread across host countries."},
    {"title": "Driver Reliability Analysis", "chart": "Stacked bar",
     "text": "Retirements per driver, split by DNF reason."},
    {"title": "Driver Performance Leaderboard", "chart": "Vertical bar · Top N",
     "text": "Points by driver, trimmed to the number set by the Top N parameter."},
    {"title": "Team Performance Ranking", "chart": "Horizontal bar",
     "text": "Constructors ranked by total points across the selected seasons."},
    {"title": "Team Championship Performance Analysis", "chart": "Grouped bar",
     "text": "Season-by-season championship results, team against team."},
    {"title": "Tyre Compound Usage Distribution", "chart": "Pie chart",
     "text": "Share of soft, medium, hard and intermediate tyres."},
    {"title": "Country-wise Race Participation", "chart": "Treemap / highlight table",
     "text": "Race entries by host country, sized and shaded by volume."},
    {"title": "Podium Achievements by Driver and Team", "chart": "Packed bubbles",
     "text": "Podium finishes per driver, bubbles sized by count and coloured by team."},
]

SHEETS = [
    {"name": "race_results", "rows": "6,464", "cols": 42,
     "text": "One row per driver per race: grid, finish, points, DNFs, pit stops, tyre strategy, weather."},
    {"name": "lap_intelligence", "rows": "3,814", "cols": 14,
     "text": "Lap times, sector splits, tyre compound and age, DRS and pit laps."},
    {"name": "qualifying_results", "rows": "3,130", "cols": 16,
     "text": "Q1 to Q3 lap times, gap to pole, sector splits and top speed."},
    {"name": "championship_standings", "rows": "311", "cols": 10,
     "text": "Final driver standings per season: points, wins, podiums, poles, titles."},
    {"name": "circuits", "rows": "29", "cols": 9,
     "text": "Country, city, laps, lap length, layout type, altitude and direction."},
]

FILTERS = [
    {"name": "DNF Reason", "kind": "Dropdown filter",
     "text": "Narrows the reliability chart and race results to one cause of retirement."},
    {"name": "Year of Race Date", "kind": "Season filter",
     "text": "Isolates a single season or compares a range, from 2010 to 2026, across every chart."},
    {"name": "Top N", "kind": "Parameter · default 10",
     "text": "Sets how many drivers the performance leaderboard shows."},
]

STORY_SCENES = [
    "The global scale of the grid",
    "Where drivers race",
    "Driver reliability and DNFs",
    "Driver performance leaderboard",
    "Team performance ranking",
    "Season-by-season championships",
    "Tyre strategy patterns",
    "Country-level participation",
    "Podium achievements",
]


def embed_src(link):
    """Return the /views/ URL the <tableau-viz> tag needs, from any Tableau Public share link."""
    link = link.strip()
    shared = re.search(r"/shared/([^/?#]+)", link)
    if shared:
        return f"https://public.tableau.com/shared/{shared.group(1)}"
    found = re.search(r"/(?:viz|views)/([^/?#]+)/([^/?#]+)", link)
    if not found:
        return link
    return f"https://public.tableau.com/views/{found.group(1)}/{found.group(2)}"


@app.route("/")
def home():
    return render_template("index.html", kpis=KPIS, visuals=VISUALS, sheets=SHEETS, filters=FILTERS)


@app.route("/dashboard")
def dashboard():
    return render_template(
        "viz.html",
        kicker="Interactive dashboard",
        heading="Race Intelligence Dashboard",
        intro="Nine views of the 2010 to 2026 seasons on one page. Use the DNF Reason, Year and "
              "Top N controls at the top of the dashboard, or click any mark to filter the rest.",
        src=embed_src(config.TABLEAU_DASHBOARD_URL),
        setting="TABLEAU_DASHBOARD_URL",
    )


@app.route("/story")
def story():
    return render_template(
        "viz.html",
        kicker="Data story",
        heading="The Race Intelligence Story",
        intro="Nine scenes, from the scale of the grid to who reaches the podium. Step through them "
              "with the arrows at the top of the story.",
        src=embed_src(config.TABLEAU_STORY_URL),
        setting="TABLEAU_STORY_URL",
        scenes=STORY_SCENES,
    )


@app.errorhandler(404)
def not_found(error):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(debug=True)
