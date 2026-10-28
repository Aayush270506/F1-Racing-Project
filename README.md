# Formula 1 Race Intelligence Dashboard (2010–2026)

A Tableau project that analyses Formula 1 race data across 17 seasons: driver performance,
constructors' championship trends, tyre strategy, circuits, DNFs and reliability, and podiums.
The finished dashboard and story are published to Tableau Public and embedded in a Flask website.

It is built for three users:

- **Team Strategist Rajan** compares championship points with Red Bull Racing and Mercedes,
  evaluates tyre strategy and identifies top drivers for recruitment.
- **Broadcast Analyst Divya** needs driver rankings, the countries hosting the most Grands Prix
  and podiums by driver and team.
- **FIA Analyst Arvind** analyses DNFs by driver and failure type and compares reliability across seasons.

## Project links

| | |
| --- | --- |
| **Demo Link** | _To be added_ |
| **GitHub Link** | https://github.com/Aayush270506/F1-Racing-Project |

## Repository structure

```
dataset/                      F1 Racing Project Dataset.xlsx (5 sheets, 13,748 rows)
analysis/                     validate_dataset.py and the validation_report.md it writes
tableau/                      F1_Race_Intelligence.twbx (workbook, extracts and data)
f1-race-intelligence/         Flask web app that embeds the published dashboard and story
```

## Parts 1–7

| Part | What was built | Where |
| --- | --- | --- |
| 1. Data Collection & Extraction | Excel connection to all 5 sheets. `race_results` is related to `circuits` on `circuit_id` and to `lap_intelligence` and `qualifying_results` on `race_id`; `championship_standings` is a separate data source. Both data sources use Tableau extracts. | `dataset/`, `tableau/` |
| 2. Data Preparation | Validation of every sheet, column type and KPI (`analysis/validation_report.md`). `race_date` converted from text to Date. DNF rows kept. Calculated fields: DNF Count, Points Cumulative, Top N Filter, Podium Finish. Top N parameter (default 10). | `analysis/`, `tableau/` |
| 3. Data Visualization | 9 visualizations: KPI cards, map, stacked bar, vertical bar (Top N), horizontal bar, grouped bar, pie, treemap, packed bubbles. A cumulative-points line supports the story. | `tableau/` |
| 4. Dashboard | "F1 Race Intelligence Dashboard": dark F1 theme, title, 4 KPI cards and 3 controls on top, then three rows of charts with legends. | `tableau/` |
| 5. Story | "F1 Race Intelligence Story": 9 scenes. Each scene is a small dashboard with a one-line finding (computed from the data) above its chart. | `tableau/` |
| 6. Performance Testing | Every chart, KPI and filter checked against expected values, plus measured load times: [analysis/performance_testing.md](analysis/performance_testing.md). | `analysis/` |
| 7. Web Integration | Dashboard and story published to Tableau Public and embedded in the Flask app. | `f1-race-intelligence/` |

## Data notes

The full list is in `analysis/validation_report.md`. The ones that affect the charts:

- `race_results` has 42 columns.
- DNF reasons in the data are Engine, Hydraulics, Mechanical, Brake failure, Gearbox and Collision.
  DNF entries score 0 points, so the DNF Reason filter is applied to the reliability chart only.
- Four season-final races are dated in January of the following year, so "Year of Race Date" can
  differ from `season` for those races.
- Carlos Sainz appears for both Ferrari and Williams in every race, so his driver totals combine both entries.
- `circuits` lists 29 circuits; 24 of them host races in `race_results`.

## Re-run the data validation

```bash
pip install -r analysis/requirements.txt
python analysis/validate_dataset.py
```

## Publish the workbook to Tableau Public

1. Open `tableau/F1_Race_Intelligence.twbx` in Tableau Public (or Tableau Desktop).
2. **File > Save to Tableau Public As…**, sign in, and give it a name.
3. When the browser opens the published workbook, copy the dashboard and story links.
4. Paste them into `f1-race-intelligence/config.py`.

## Run the web app

```bash
cd f1-race-intelligence
python -m venv venv
venv\Scripts\python.exe -m pip install -r requirements.txt
venv\Scripts\python.exe app.py
```

Then open http://127.0.0.1:5000. The embedded views load from Tableau Public, so the computer
needs internet access and the workbook must be public (not hidden) on the Tableau Public profile.
