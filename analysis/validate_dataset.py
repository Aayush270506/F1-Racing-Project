"""Validate the F1 dataset and write the figures the Tableau workbook should show.

Run from the project root:
    python analysis/validate_dataset.py

Writes analysis/validation_report.md. Every number in the report is computed
from dataset/F1 Racing Project Dataset.xlsx; nothing is typed in by hand.
"""
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
DATASET = ROOT / "dataset" / "F1 Racing Project Dataset.xlsx"
REPORT = ROOT / "analysis" / "validation_report.md"

TABLEAU_TYPES = {"int64": "Number (whole)", "float64": "Number (decimal)", "str": "String", "object": "String"}


def table(df, index=True):
    """Render a small DataFrame as a Markdown table."""
    df = df.reset_index() if index else df
    head = "| " + " | ".join(str(c) for c in df.columns) + " |"
    rule = "| " + " | ".join("---" for _ in df.columns) + " |"
    rows = ["| " + " | ".join(f"{v:,}" if isinstance(v, int) else str(v) for v in row) + " |" for row in df.itertuples(index=False)]
    return "\n".join([head, rule, *rows])


def check(label, ok, detail):
    return f"| {label} | {'PASS' if ok else 'FAIL'} | {detail} |"


def main():
    sheets = pd.read_excel(DATASET, sheet_name=None)
    rr = sheets["race_results"]
    ci = sheets["circuits"]
    cs = sheets["championship_standings"]
    li = sheets["lap_intelligence"]
    qr = sheets["qualifying_results"]
    race_date = pd.to_datetime(rr["race_date"])
    podium = rr["finish_position"] <= 3
    out = ["# Dataset validation report", "", f"Source: `dataset/{DATASET.name}`", ""]

    # Part 1: what was loaded
    inventory = pd.DataFrame(
        [(name, len(df), df.shape[1], int(df.isna().all(axis=1).sum())) for name, df in sheets.items()],
        columns=["Sheet", "Rows", "Columns", "Blank rows"],
    )
    out += ["## 1. Sheets loaded", "", table(inventory, index=False), "",
            f"Total rows across all sheets: **{int(inventory['Rows'].sum()):,}**.", ""]

    # Part 2: data types of race_results
    types = pd.DataFrame({
        "Column": rr.columns,
        "Excel / pandas type": [str(t) for t in rr.dtypes],
        "Tableau type": [TABLEAU_TYPES.get(str(t), str(t)) for t in rr.dtypes],
        "Nulls": [int(n) for n in rr.isna().sum()],
    })
    types.loc[types["Column"] == "race_date", "Tableau type"] = "Date (converted from text)"
    out += ["## 2. race_results columns and data types", "",
            f"`race_results` has **{rr.shape[1]} columns** and {len(rr):,} rows. "
            "`race_date` is stored as text in Excel, so it is converted to a Date in Tableau.", "",
            table(types, index=False), ""]

    # Part 2: cleaning rules
    dnf = rr["dnf"] == 1
    rules = [
        check("Every missing finish_position is a DNF", rr.loc[rr["finish_position"].isna(), "dnf"].eq(1).all(),
              f"{int(rr['finish_position'].isna().sum())} missing, all with dnf = 1 (kept, not deleted)"),
        check("Every DNF has a dnf_reason", rr.loc[dnf, "dnf_reason"].notna().all(),
              f"{int(dnf.sum())} DNFs, {int(rr.loc[dnf, 'dnf_reason'].notna().sum())} with a reason"),
        check("gap_to_leader_s is null only for DNFs", rr.loc[rr["gap_to_leader_s"].isna(), "dnf"].eq(1).all(),
              f"{int(rr['gap_to_leader_s'].isna().sum())} nulls; Tableau's SUM/AVG skip them"),
        check("race_date parses as a date", race_date.notna().all(),
              f"{race_date.min():%Y-%m-%d} to {race_date.max():%Y-%m-%d}"),
        check("Every race_results circuit_id exists in circuits", rr["circuit_id"].isin(ci["circuit_id"]).all(),
              f"{rr['circuit_id'].nunique()} circuits used of {ci['circuit_id'].nunique()} listed"),
        check("Every lap_intelligence race_id exists in race_results", li["race_id"].isin(rr["race_id"]).all(),
              f"{li['race_id'].nunique()} races with lap data"),
        check("Every qualifying_results race_id exists in race_results", qr["race_id"].isin(rr["race_id"]).all(),
              f"{qr['race_id'].nunique()} races with qualifying data"),
    ]
    out += ["## 3. Cleaning and relationship checks", "", "| Check | Result | Detail |", "| --- | --- | --- |", *rules, ""]

    # Part 2: value ranges and categories
    ranges = pd.DataFrame([
        ("points", rr["points"]), ("laps_led", rr["laps_led"]), ("drs_overtakes", rr["drs_overtakes"]),
        ("air_temp_celsius", rr["air_temp_celsius"]), ("lap_time_s (lap_intelligence)", li["lap_time_s"]),
    ], columns=["Measure", "values"])
    # object dtype keeps whole-number measures from being shown as 0.0
    ranges["Min"] = pd.Series([s.min().item() for s in ranges["values"]], dtype=object)
    ranges["Max"] = pd.Series([s.max().item() for s in ranges["values"]], dtype=object)
    ranges["Nulls"] = ranges["values"].map(lambda s: int(s.isna().sum()))
    categories = pd.DataFrame([
        ("driver", rr["driver"]), ("team", rr["team"]), ("country", rr["country"]),
        ("circuit_type", rr["circuit_type"]), ("starting_compound", rr["starting_compound"]),
        ("tyre_compound (lap_intelligence)", li["tyre_compound"]), ("dnf_reason", rr["dnf_reason"].dropna()),
    ], columns=["Dimension", "values"])
    categories["Distinct values"] = categories["values"].map(lambda s: s.nunique())
    categories["Values"] = categories["values"].map(lambda s: ", ".join(sorted(s.unique())) if s.nunique() <= 10 else "(too many to list)")
    out += ["## 4. Measures and dimensions", "", table(ranges.drop(columns="values"), index=False), "",
            table(categories.drop(columns="values"), index=False), ""]

    # Part 4 and 6: KPI cards
    kpis = [
        check("Competing Teams = 10", rr["team"].nunique() == 10, f"COUNTD(team) = {rr['team'].nunique()}"),
        check("Seasons in Play = 17", rr["season"].nunique() == 17,
              f"COUNTD(season) = {rr['season'].nunique()} ({rr['season'].min()} to {rr['season'].max()})"),
        check("Race Outcomes Logged = 6,464", len(rr) == 6464, f"rows in race_results = {len(rr):,}"),
        check("Circuits Showcased = 29", ci["circuit_id"].nunique() == 29, f"COUNTD(circuit_id) in circuits = {ci['circuit_id'].nunique()}"),
    ]
    out += ["## 5. KPI card validation", "", "| KPI | Result | Detail |", "| --- | --- | --- |", *kpis, ""]

    # Part 6: expected values for each chart
    drivers = rr.groupby("driver")["points"].sum().sort_values(ascending=False)
    dnf_reasons = rr["dnf_reason"].value_counts()
    dnf_drivers = rr[dnf].groupby("driver").size().sort_values(ascending=False)
    teams = rr.groupby("team")["points"].sum().sort_values(ascending=False)
    champs = cs[cs["champion"] == 1].set_index("season")[["driver", "team", "points"]]
    champs.index = champs.index.astype(str)
    tyres = li["tyre_compound"].value_counts()
    tyre_share = (tyres / tyres.sum() * 100).round(1)
    countries = rr.groupby("country")["race_id"].nunique().sort_values(ascending=False)
    entries = rr.groupby("country").size().sort_values(ascending=False)
    podiums = rr[podium].groupby(["driver", "team"]).size().sort_values(ascending=False)
    out += [
        "## 6. Expected chart values (for testing the workbook)", "",
        "**Driver Performance Leaderboard: top 10 by points**", "",
        table(drivers.head(10).rename("Points").astype(int).to_frame()), "",
        f"**Driver Reliability Analysis**: {int(dnf.sum())} DNFs by reason", "",
        table(dnf_reasons.rename("DNFs").astype(int).to_frame()), "",
        "Drivers with the most DNFs: " + ", ".join(f"{d} ({n})" for d, n in dnf_drivers.head(5).items()) + ".", "",
        "**Team Performance Ranking** (points from race_results)", "",
        table(teams.rename("Points").astype(int).to_frame()), "",
        "**Team Championship Performance Analysis**: champion by season (championship_standings)", "",
        table(champs.rename(columns=str.title)), "",
        "**Tyre Compound Usage Distribution** (laps in lap_intelligence)", "",
        table(pd.DataFrame({"Laps": tyres.astype(int), "Share %": tyre_share})), "",
        "**Global Driver Distribution / Country-wise Race Participation**", "",
        table(pd.DataFrame({"Grands Prix": countries.astype(int), "Driver entries": entries.reindex(countries.index).astype(int)})), "",
        "**Podium Achievements by Driver and Team**", "",
        table(podiums.rename("Podiums").astype(int).to_frame()), "",
    ]

    # Data notes the workbook and story must respect
    year_mismatch = rr[race_date.dt.year != rr["season"]]
    sainz_teams = sorted(rr.loc[rr["driver"] == "Carlos Sainz", "team"].unique())
    placeholders = sorted((d for d in qr["driver"].unique() if d.startswith("Driver_")), key=lambda d: int(d.split("_")[1]))
    team_diff = (cs.groupby("team")["points"].sum() - teams).loc[lambda s: s != 0]
    out += [
        "## 7. Data notes", "",
        f"- `race_results` has {rr.shape[1]} columns (the brief says 41).",
        f"- DNF reasons in the data are {', '.join(sorted(dnf_reasons.index))}. There is no 'Engine failure' or 'Other' category.",
        f"- {year_mismatch['race_id'].nunique()} season-final races ({len(year_mismatch)} rows) are dated in January of the next year, "
        "so 'Year of Race Date' differs from `season` for them.",
        f"- Carlos Sainz appears for {' and '.join(sainz_teams)} in every race ({int((rr['driver'] == 'Carlos Sainz').sum())} rows), "
        "so his driver totals combine both entries.",
        f"- `circuits` lists {ci['circuit_id'].nunique()} circuits; {rr['circuit_id'].nunique()} host races in `race_results`.",
        f"- `qualifying_results` uses placeholder drivers ({placeholders[0]} to {placeholders[-1]}); it is related on race_id but not charted.",
        "- Team points in `championship_standings` differ from `race_results` for "
        + ", ".join(f"{t} ({d:+,})" for t, d in team_diff.items()) + ".",
        "",
    ]

    REPORT.write_text("\n".join(out), encoding="utf-8")
    print(f"Wrote {REPORT.relative_to(ROOT)}")
    for line in rules + kpis:
        print(line)


if __name__ == "__main__":
    main()
