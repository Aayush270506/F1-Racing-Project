# F1 Racing Dashboard

Formula 1 Race Intelligence: a Tableau analysis of 17 seasons (2010 to 2026) of race
results, qualifying, lap data and championship standings, served through a small Flask
website.

| Folder | Contents |
| --- | --- |
| `f1-race-intelligence/` | Flask web app that embeds the Tableau Public dashboard and story |
| `dataset/` | The source Excel workbook (5 sheets, 13,748 rows) |

## Run the web app

```bash
cd f1-race-intelligence
python -m venv venv
venv\Scripts\python.exe -m pip install -r requirements.txt
venv\Scripts\python.exe app.py
```

Then open http://127.0.0.1:5000. The Tableau Public links are set in
`f1-race-intelligence/config.py`; see
[f1-race-intelligence/README.md](f1-race-intelligence/README.md) for details.
