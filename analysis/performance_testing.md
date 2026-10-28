# Performance testing (Part 6)

Workbook tested: `tableau/F1_Race_Intelligence.twbx`, opened in Tableau Public 2026.3 on Windows 11.
Every expected value below comes from `analysis/validate_dataset.py` or a pandas query on the same
Excel file; every observed value is what Tableau showed in its status bar (marks and totals).

## Data volume and extract mode

| Item | Value |
| --- | --- |
| Rows loaded | 13,748 across 5 sheets (`race_results` 6,464 × 42 columns) |
| Data sources | F1 Race Data (4 related tables), F1 Championship Standings (1 table) |
| Connection mode | Extract (Hyper) for both data sources |
| Extract size | F1 Race Data 1.0 MB, Championship Standings 64 KB (uncompressed) |
| Packaged workbook | 2.3 MB `.twbx` (workbook, both extracts and the Excel file) |

## Rendering: all visualizations against expected values

| Visualization | Expected | Observed in Tableau | Result |
| --- | --- | --- | --- |
| KPI cards | 10 teams, 17 seasons, 6,464 outcomes, 29 circuits | 10, 17, 6,464, 29 | Pass |
| Global Driver Distribution | 21 countries, 6,464 entries | 21 marks, SUM(CNT(race_id)) 6,464 | Pass |
| Driver Reliability Analysis | 19 drivers, 396 DNFs | 19 rows, SUM(DNF Count) 396 | Pass |
| Driver Performance Leaderboard (Top N = 10) | 10 drivers, 28,403 points | 10 marks, SUM(points) 28,403 | Pass |
| Team Performance Ranking | 10 teams, 31,906 points | 10 marks, SUM(points) 31,906 | Pass |
| Team Championship Performance Analysis | 17 seasons × 4 teams, 26,456 points | 68 marks, SUM(points) 26,456 | Pass |
| Tyre Compound Usage Distribution | 4 compounds, 3,814 laps | 4 marks, 3,814 laps (100%) | Pass |
| Country-wise Race Participation | 21 countries, 334 Grands Prix | 21 marks, SUM(CNTD(race_id)) 334 | Pass |
| Podium Achievements by Driver and Team | 20 driver-team pairs, 940 podiums | 20 marks, SUM(Podium Finish) 940 | Pass |
| Driver Points Progression (story) | 5 drivers × 17 seasons | 85 marks | Pass |

## Filters and parameter

| Test | Setting | Expected | Observed | Result |
| --- | --- | --- | --- | --- |
| T1b | Year of Race Date = 2024, leaderboard | 10 drivers, 1,955 points | 10 marks, SUM(points) 1,955 | Pass |
| T2 | DNF Reason = Engine, reliability chart | 16 drivers, 73 DNFs | 16 rows, SUM(DNF Count) 73 | Pass |
| T1 | Year of Race Date = 2024, team ranking | 10 teams, 2,102 points | Not captured | Pending |
| T3 | Top N = 5, leaderboard | 5 drivers, 19,039 points | Not run yet | Pending |
| T4 | Year 2024 + DNF Reason Engine | 2 DNFs, 2 drivers | Not run yet | Pending |

No filter produced duplicated rows or inflated totals: every observed total equals the pandas total.

## Loading speed

Measured from Tableau's own log for one run that opened the workbook on the reliability chart:

| Step | Time |
| --- | --- |
| Open workbook | 1.22 s |
| Connect to both extracts | 0.30 s |
| Reliability chart query | 0.055 s |
| Slowest chart render (visual model update) | 0.10 s |

This is a single measurement on one laptop; it is not an average.

## Calculated fields

Only four calculated fields and one parameter are used; everything else comes straight from the data.

| Field | Formula | Used in |
| --- | --- | --- |
| DNF Count | `IF [dnf] = 1 THEN 1 ELSE 0 END` | Driver Reliability Analysis |
| Points Cumulative | `RUNNING_SUM(SUM([points]))` | Driver Points Progression |
| Top N Filter | `RANK(SUM([points])) <= [Top N]` | Driver Performance Leaderboard |
| Podium Finish | `IF [finish_position] <= 3 THEN 1 ELSE 0 END` | Podium Achievements |
| Top N (parameter) | integer 1–19, default 10 | Leaderboard filter |

## Problems found and fixed during testing

- `race_date` is text in Excel, so "Year of Race Date" failed; the field is now a Date.
- Tableau Public refused the workbook until both data sources were extracts.
- KPI numbers showed `###` when their tiles shrank; the tiles now have fixed widths.
- The pie chart overflowed its tile; mark sizing was reset.
- Coloured charts had no legends; legends were added to the dashboard and to the story scenes.
- The grouped bar chart repeated a team label under every bar; the labels were hidden (the legend names the teams).

## Known log message

When the Top N table-calculation filter runs, Tableau logs "Skipping the logical query cache". It only
means that query is not cached; the leaderboard totals above match the expected values.
