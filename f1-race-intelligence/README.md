# Formula 1 Race Intelligence: Flask web app

A small Flask site that embeds the Tableau Public dashboard and story for the
F1 Race Intelligence project (2010 to 2026).

| Page | Route | What it shows |
| --- | --- | --- |
| Home | `/` | KPIs, the nine visualizations, the three filters and the five data sheets |
| Dashboard | `/dashboard` | The published Tableau dashboard, fully interactive |
| Story | `/story` | The published nine-scene Tableau story |

## 1. Add your Tableau Public links

Open `config.py` and paste your links between the quotes:

```python
TABLEAU_DASHBOARD_URL = os.environ.get("TABLEAU_DASHBOARD_URL", "https://public.tableau.com/views/YourWorkbook/Dashboard1")
TABLEAU_STORY_URL = os.environ.get("TABLEAU_STORY_URL", "https://public.tableau.com/views/YourWorkbook/Story1")
```

Use the link from **Share > Copy Link** on Tableau Public. Both the
`/views/...` form and the `/app/profile/<you>/viz/...` form work; the app
turns either one into the embed URL. The workbook must be visible (not
hidden) on your profile, or the embed shows a sign-in screen.

## 2. Run it

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

On macOS or Linux, activate with `source venv/bin/activate` instead.

Then open http://127.0.0.1:5000.

## How the embed works

`templates/viz.html` loads Tableau's Embedding API and places a
`<tableau-viz>` tag with your link as its `src`. The view keeps everything
from the published workbook: the DNF Reason and Year filters, the Top N
parameter, cross-filtering on click, and the story navigation.

The embed takes its size from the workbook, so set the dashboard and story
to a **Fixed** size in Tableau (Dashboard > Size) before publishing. The page
centres it, and on a narrow screen it scrolls sideways inside its frame.

## Project layout

```
app.py              routes and page content
config.py           Tableau Public links
templates/
  base.html         header, nav and footer shared by every page
  index.html        home page
  viz.html          dashboard and story pages
  404.html          page not found
static/css/style.css
requirements.txt
```
