# Dataset validation report

Source: `dataset/F1 Racing Project Dataset.xlsx`

## 1. Sheets loaded

| Sheet | Rows | Columns | Blank rows |
| --- | --- | --- | --- |
| circuits | 29 | 9 | 0 |
| championship_standings | 311 | 10 | 0 |
| lap_intelligence | 3,814 | 14 | 0 |
| qualifying_results | 3,130 | 16 | 0 |
| race_results | 6,464 | 42 | 0 |

Total rows across all sheets: **13,748**.

## 2. race_results columns and data types

`race_results` has **42 columns** and 6,464 rows. `race_date` is stored as text in Excel, so it is converted to a Date in Tableau.

| Column | Excel / pandas type | Tableau type | Nulls |
| --- | --- | --- | --- |
| race_id | str | String | 0 |
| season | int64 | Number (whole) | 0 |
| round | int64 | Number (whole) | 0 |
| circuit_id | str | String | 0 |
| circuit_name | str | String | 0 |
| country | str | String | 0 |
| city | str | String | 0 |
| race_date | str | Date (converted from text) | 0 |
| circuit_type | str | String | 0 |
| circuit_laps | int64 | Number (whole) | 0 |
| circuit_length_km | float64 | Number (decimal) | 0 |
| total_distance_km | float64 | Number (decimal) | 0 |
| altitude_m | int64 | Number (whole) | 0 |
| direction | str | String | 0 |
| weather | str | String | 0 |
| is_wet_race | int64 | Number (whole) | 0 |
| air_temp_celsius | float64 | Number (decimal) | 0 |
| humidity_pct | float64 | Number (decimal) | 0 |
| wind_speed_kmh | float64 | Number (decimal) | 0 |
| safety_car_laps | int64 | Number (whole) | 0 |
| vsc_laps | int64 | Number (whole) | 0 |
| red_flag | int64 | Number (whole) | 0 |
| finish_position | float64 | Number (decimal) | 396 |
| grid_position | int64 | Number (whole) | 0 |
| positions_gained | float64 | Number (decimal) | 396 |
| driver | str | String | 0 |
| team | str | String | 0 |
| points | int64 | Number (whole) | 0 |
| dnf | int64 | Number (whole) | 0 |
| dnf_reason | str | String | 6,068 |
| fastest_lap | int64 | Number (whole) | 0 |
| gap_to_leader_s | float64 | Number (decimal) | 396 |
| total_race_time_s | float64 | Number (decimal) | 6,130 |
| pit_stops | int64 | Number (whole) | 0 |
| pit_stop_times_s | str | String | 0 |
| avg_pit_stop_time_s | float64 | Number (decimal) | 0 |
| tyre_strategy | str | String | 0 |
| starting_compound | str | String | 0 |
| undercut_attempt | int64 | Number (whole) | 0 |
| overcut_attempt | int64 | Number (whole) | 0 |
| drs_overtakes | int64 | Number (whole) | 0 |
| laps_led | int64 | Number (whole) | 0 |

## 3. Cleaning and relationship checks

| Check | Result | Detail |
| --- | --- | --- |
| Every missing finish_position is a DNF | PASS | 396 missing, all with dnf = 1 (kept, not deleted) |
| Every DNF has a dnf_reason | PASS | 396 DNFs, 396 with a reason |
| gap_to_leader_s is null only for DNFs | PASS | 396 nulls; Tableau's SUM/AVG skip them |
| race_date parses as a date | PASS | 2010-03-01 to 2026-08-02 |
| Every race_results circuit_id exists in circuits | PASS | 24 circuits used of 29 listed |
| Every lap_intelligence race_id exists in race_results | PASS | 300 races with lap data |
| Every qualifying_results race_id exists in race_results | PASS | 313 races with qualifying data |

## 4. Measures and dimensions

| Measure | Min | Max | Nulls |
| --- | --- | --- | --- |
| points | 0 | 26 | 0 |
| laps_led | 0 | 61 | 0 |
| drs_overtakes | 0 | 8 | 0 |
| air_temp_celsius | 10.2 | 34.9 | 0 |
| lap_time_s (lap_intelligence) | 66.587 | 95.984 | 0 |

| Dimension | Distinct values | Values |
| --- | --- | --- |
| driver | 19 | (too many to list) |
| team | 10 | Alpine, Aston Martin, Ferrari, Haas, Kick Sauber, McLaren, Mercedes, RB (AlphaTauri), Red Bull Racing, Williams |
| country | 21 | (too many to list) |
| circuit_type | 3 | Permanent, Street, Street/Park |
| starting_compound | 4 | Hard, Intermediate, Medium, Soft |
| tyre_compound (lap_intelligence) | 4 | Hard, Intermediate, Medium, Soft |
| dnf_reason | 6 | Brake failure, Collision, Engine, Gearbox, Hydraulics, Mechanical |

## 5. KPI card validation

| KPI | Result | Detail |
| --- | --- | --- |
| Competing Teams = 10 | PASS | COUNTD(team) = 10 |
| Seasons in Play = 17 | PASS | COUNTD(season) = 17 (2010 to 2026) |
| Race Outcomes Logged = 6,464 | PASS | rows in race_results = 6,464 |
| Circuits Showcased = 29 | PASS | COUNTD(circuit_id) in circuits = 29 |

## 6. Expected chart values (for testing the workbook)

**Driver Performance Leaderboard: top 10 by points**

| driver | Points |
| --- | --- |
| Max Verstappen | 4,640 |
| Lewis Hamilton | 4,491 |
| Sergio Perez | 3,366 |
| George Russell | 3,299 |
| Charles Leclerc | 3,243 |
| Carlos Sainz | 3,147 |
| Lando Norris | 2,454 |
| Oscar Piastri | 1,816 |
| Esteban Ocon | 1,136 |
| Pierre Gasly | 811 |

**Driver Reliability Analysis**: 396 DNFs by reason

| dnf_reason | DNFs |
| --- | --- |
| Engine | 73 |
| Hydraulics | 70 |
| Mechanical | 67 |
| Brake failure | 64 |
| Gearbox | 62 |
| Collision | 60 |

Drivers with the most DNFs: Carlos Sainz (34), Sergio Perez (29), Charles Leclerc (28), Fernando Alonso (25), Oscar Piastri (24).

**Team Performance Ranking** (points from race_results)

| team | Points |
| --- | --- |
| Red Bull Racing | 8,006 |
| Mercedes | 7,790 |
| Ferrari | 5,778 |
| McLaren | 4,270 |
| Alpine | 1,947 |
| Aston Martin | 1,181 |
| Williams | 1,057 |
| RB (AlphaTauri) | 923 |
| Haas | 591 |
| Kick Sauber | 363 |

**Team Championship Performance Analysis**: champion by season (championship_standings)

| season | Driver | Team | Points |
| --- | --- | --- | --- |
| 2010 | Max Verstappen | Red Bull Racing | 306 |
| 2011 | Max Verstappen | Red Bull Racing | 407 |
| 2012 | Lando Norris | McLaren | 285 |
| 2013 | Max Verstappen | Red Bull Racing | 401 |
| 2014 | Lewis Hamilton | Mercedes | 409 |
| 2015 | Lewis Hamilton | Mercedes | 404 |
| 2016 | Lewis Hamilton | Mercedes | 430 |
| 2017 | Lewis Hamilton | Mercedes | 322 |
| 2018 | Lewis Hamilton | Mercedes | 456 |
| 2019 | Lewis Hamilton | Mercedes | 465 |
| 2020 | Lewis Hamilton | Mercedes | 463 |
| 2021 | Max Verstappen | Red Bull Racing | 364 |
| 2022 | Max Verstappen | Red Bull Racing | 366 |
| 2023 | Max Verstappen | Red Bull Racing | 407 |
| 2024 | Lando Norris | McLaren | 328 |
| 2025 | Max Verstappen | Red Bull Racing | 348 |
| 2026 | Lando Norris | McLaren | 168 |

**Tyre Compound Usage Distribution** (laps in lap_intelligence)

| tyre_compound | Laps | Share % |
| --- | --- | --- |
| Soft | 1,202 | 31.5 |
| Medium | 1,174 | 30.8 |
| Hard | 1,158 | 30.4 |
| Intermediate | 280 | 7.3 |

**Global Driver Distribution / Country-wise Race Participation**

| country | Grands Prix | Driver entries |
| --- | --- | --- |
| Bahrain | 115 | 2,168 |
| USA | 20 | 400 |
| Monaco | 17 | 328 |
| Hungary | 17 | 328 |
| Spain | 17 | 328 |
| Canada | 16 | 308 |
| UAE | 16 | 308 |
| Brazil | 16 | 308 |
| Singapore | 15 | 288 |
| Italy | 11 | 220 |
| Austria | 9 | 180 |
| Mexico | 8 | 160 |
| Australia | 7 | 140 |
| Netherlands | 7 | 140 |
| Azerbaijan | 7 | 140 |
| Saudi Arabia | 7 | 140 |
| Japan | 7 | 140 |
| UK | 7 | 140 |
| Qatar | 7 | 140 |
| Belgium | 6 | 120 |
| China | 2 | 40 |

**Podium Achievements by Driver and Team**

| driver | team | Podiums |
| --- | --- | --- |
| Max Verstappen | Red Bull Racing | 187 |
| Lewis Hamilton | Mercedes | 174 |
| George Russell | Mercedes | 115 |
| Charles Leclerc | Ferrari | 113 |
| Sergio Perez | Red Bull Racing | 97 |
| Lando Norris | McLaren | 85 |
| Carlos Sainz | Ferrari | 44 |
| Oscar Piastri | McLaren | 35 |
| Esteban Ocon | Alpine | 25 |
| Carlos Sainz | Williams | 19 |
| Yuki Tsunoda | RB (AlphaTauri) | 10 |
| Fernando Alonso | Aston Martin | 10 |
| Pierre Gasly | Alpine | 7 |
| Nico Hülkenberg | Haas | 6 |
| Liam Lawson | RB (AlphaTauri) | 6 |
| Lance Stroll | Aston Martin | 3 |
| Alex Albon | Williams | 2 |
| Valtteri Bottas | Kick Sauber | 2 |

## 7. Data notes

- `race_results` has 42 columns (the brief says 41).
- DNF reasons in the data are Brake failure, Collision, Engine, Gearbox, Hydraulics, Mechanical. There is no 'Engine failure' or 'Other' category.
- 4 season-final races (80 rows) are dated in January of the next year, so 'Year of Race Date' differs from `season` for them.
- Carlos Sainz appears for Ferrari and Williams in every race (668 rows), so his driver totals combine both entries.
- `circuits` lists 29 circuits; 24 host races in `race_results`.
- `qualifying_results` uses placeholder drivers (Driver_2 to Driver_10); it is related on race_id but not charted.
- Team points in `championship_standings` differ from `race_results` for Ferrari (+612), Williams (-612).
