#!/usr/bin/env python3
"""Extract Tables IV, V, VIII and the analysis tables (A-G and text tables)
of the 1906 European census of Tunisia (Gallica ark bd6t53563851).

Gallica's OCR is too incomplete on these pages to parse automatically (many
cells are dropped), so the values below were transcribed from the page images
(data-raw/bnf_gallica/pages/bd6t53563851/fNNNN.jpg) and are checked here
against every printed row and column total. Printed totals are kept only for
validation, not as data rows (see SPEC.md). '»' in the source is written 0.

Run:  python3 data-raw/colonial_census/extract_eur1906_t4_t8_analysis.py
Writes data-raw/colonial_census/csv/eur1906_*.csv and prints a validation report.
"""
import csv
from pathlib import Path

OUT = Path(__file__).resolve().parent / "csv"
CENSUS = "eur1906"

NAT = ["french", "italian", "maltese", "spanish", "greek", "other_european"]
NAT_FR = ["Français", "Italiens", "Maltais", "Espagnols", "Grecs", "Autres"]

REPORT = []   # (table, checks, passed, notes)
CHECKS = {}


def check(table, label, got, expected):
    c = CHECKS.setdefault(table, [0, 0, []])
    c[0] += 1
    if got == expected:
        c[1] += 1
    elif isinstance(got, bool):
        c[2].append(f"{label}: differs from printed value")
    else:
        c[2].append(f"{label}: computed {got} != printed {expected}")


def grid(text):
    """Parse whitespace-separated integer rows (blank lines ignored)."""
    return [[int(x) for x in ln.split()] for ln in text.strip().splitlines() if ln.strip()]


def write(name, header, rows):
    OUT.mkdir(parents=True, exist_ok=True)
    with open(OUT / f"{name}.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)
    return len(rows)


# --------------------------------------------------------------------------
# Table I (p.5, view 9): nationality x circonscription. Extracted by another
# worker; used here only as the source of row totals for Table IV.
# Columns: french italian maltese spanish greek other total
TABLE_I = {
    "Béja": [773, 1883, 41, 9, 2, 19, 2727],
    "Medjez-el-Bab": [476, 404, 26, 13, 3, 4, 926],
    "Bizerte": [4611, 9169, 507, 92, 29, 79, 14487],
    "Gabès": [335, 365, 196, 10, 1, 2, 909],
    "Djerba": [187, 86, 345, 0, 41, 28, 687],
    "Gafsa": [661, 1213, 49, 21, 8, 3, 1955],
    "Tozeur": [74, 16, 0, 2, 0, 1, 93],
    "Grombalia": [1031, 2020, 167, 28, 14, 33, 3293],
    "Kairouan": [432, 689, 34, 18, 25, 49, 1247],
    "Le Kef": [781, 1969, 55, 22, 4, 26, 2857],
    "Téboursouk": [431, 419, 14, 3, 2, 34, 903],
    "Mactar": [75, 16, 2, 3, 0, 1, 97],
    "Sfax": [1801, 3267, 1310, 15, 234, 84, 6711],
    "Souk-el-Arba": [1004, 1497, 43, 13, 6, 15, 2578],
    "Tabarca": [849, 1107, 27, 30, 0, 1, 2014],
    "Sousse": [2194, 4561, 1277, 24, 13, 62, 8131],
    "Thala": [136, 279, 4, 0, 0, 0, 419],
    "Tunis": [18626, 52076, 6174, 289, 293, 1061, 78519],
    "Territoires du Sud": [133, 120, 59, 8, 8, 14, 342],
}
TABLE_I_TOTAL = [34610, 81156, 10330, 600, 683, 1516, 128895]

# --------------------------------------------------------------------------
# Table IV (pp.18-21, views 22-25): length of stay in Tunisia.
DUR = ["passing_through", "lt_1y", "1_2y", "2_3y", "3_4y", "4_5y", "5_6y",
       "6_7y", "7_8y", "8_9y", "9_10y", "gt_10y"]
DUR_FR = ["de passage en Tunisie", "de moins d'un an", "compris entre 1 et 2 ans",
          "compris entre 2 et 3 ans", "compris entre 3 et 4 ans", "compris entre 4 et 5 ans",
          "compris entre 5 et 6 ans", "compris entre 6 et 7 ans", "compris entre 7 et 8 ans",
          "compris entre 8 et 9 ans", "compris entre 9 et 10 ans", "de plus de 10 ans"]

# Each block: 6 nationality rows then the printed "Totaux" row.
# On pp.18 and 20 the last column ("de plus de 10 ans") is lost in the binding:
# those blocks have 11 values per row and the 12th is derived below.
T4 = {
    # page 18, view 22 (gt_10y lost in the gutter)
    ("Béja", 18, 22): """
        0 72 73 70 45 72 58 44 26 53 23
        3 165 165 161 134 155 134 123 81 56 80
        0 2 0 1 1 2 1 3 0 2 1
        0 0 1 0 0 5 0 0 0 1 0
        0 0 0 0 0 0 1 0 0 0 0
        0 2 6 2 0 1 0 0 2 0 1
        3 241 245 234 180 235 194 170 109 112 105""",
    ("Medjez-el-Bab", 18, 22): """
        5 41 91 44 37 36 40 29 32 10 16
        0 37 61 34 32 32 21 10 30 22 27
        1 2 1 1 0 1 1 0 0 1 1
        0 0 0 0 1 7 0 0 0 0 0
        0 0 0 0 0 0 1 0 0 0 1
        0 2 2 0 0 0 0 0 0 0 0
        6 82 155 79 70 76 63 39 62 33 45""",
    ("Bizerte", 18, 22): """
        74 560 370 336 367 328 340 317 189 207 155
        2 543 477 563 694 774 967 857 604 453 262
        0 16 23 14 12 25 17 16 21 16 8
        1 11 6 8 9 2 7 6 3 2 1
        0 3 1 1 5 3 2 0 0 1 3
        0 10 13 5 5 7 6 6 1 2 2
        77 1143 890 927 1092 1139 1339 1202 818 681 431""",
    ("Gabès", 18, 22): """
        7 28 25 22 26 14 14 22 11 8 16
        0 11 8 11 21 13 14 13 17 12 10
        0 12 1 5 5 5 8 4 5 8 6
        0 0 1 0 0 0 0 1 0 0 1
        0 0 0 0 0 0 0 0 0 0 0
        0 0 0 0 0 0 0 0 0 0 0
        7 51 35 38 52 32 36 40 33 28 33""",
    ("Djerba", 18, 22): """
        3 15 6 6 16 18 16 7 2 5 7
        0 6 4 4 3 1 3 5 5 1 0
        0 12 13 9 15 7 8 8 11 7 10
        0 0 0 0 0 0 0 0 0 0 0
        0 8 5 7 0 0 1 0 5 1 2
        0 4 3 3 0 1 8 0 4 1 0
        3 45 31 29 34 27 36 20 27 15 19""",
    # page 19, view 23
    ("Gafsa", 19, 23): """
        2 95 67 63 44 33 55 26 36 31 20 189
        0 186 109 110 107 78 79 63 53 55 48 325
        0 4 3 2 0 1 1 1 3 0 2 32
        0 7 4 5 0 3 0 0 0 0 1 1
        0 0 0 2 1 0 0 0 1 0 0 4
        0 0 0 1 1 0 0 0 0 0 0 1
        2 292 183 183 153 115 135 90 93 86 71 552""",
    ("Tozeur", 19, 23): """
        5 4 2 6 2 6 6 5 1 1 3 33
        0 1 1 0 0 1 0 0 0 2 1 10
        0 0 0 0 0 0 0 0 0 0 0 0
        0 1 0 0 0 0 0 0 0 0 0 1
        0 0 0 0 0 0 0 0 0 0 0 0
        0 0 0 0 0 0 0 0 0 0 0 1
        5 6 3 6 2 7 6 5 1 3 4 45""",
    ("Grombalia", 19, 23): """
        86 82 84 74 65 36 66 49 53 44 43 349
        1 83 156 128 156 82 136 113 103 115 103 844
        0 5 2 7 9 6 3 5 7 5 1 117
        0 0 1 4 1 1 1 0 0 0 0 20
        0 1 2 2 0 0 0 0 0 0 0 9
        1 1 2 2 1 2 3 3 1 2 0 15
        88 172 247 217 232 127 209 170 164 166 147 1354""",
    ("Kairouan", 19, 23): """
        10 31 53 27 24 21 23 27 9 18 19 170
        0 65 74 55 33 38 35 35 29 20 19 286
        0 0 0 1 1 0 1 0 0 1 0 30
        0 0 3 1 1 0 0 0 1 1 1 10
        0 1 0 0 0 2 0 1 0 0 1 20
        3 1 13 7 3 4 1 5 0 0 3 9
        13 98 143 91 62 65 60 68 39 40 43 525""",
    ("Le Kef", 19, 23): """
        3 138 74 74 48 33 48 44 42 19 13 245
        0 380 175 168 120 108 101 100 77 59 21 660
        0 3 2 3 6 13 1 3 2 1 0 21
        0 5 9 0 0 0 4 0 0 0 0 4
        0 1 0 0 0 0 0 1 0 0 0 2
        0 5 4 4 1 1 1 1 1 0 0 8
        3 532 264 249 175 155 155 149 122 79 34 940""",
    # page 20, view 24 (gt_10y lost in the gutter)
    ("Téboursouk", 20, 24): """
        10 72 52 32 43 25 24 28 19 13 13
        1 39 30 25 37 28 20 20 14 14 29
        0 0 0 0 0 1 0 0 0 1 0
        0 0 0 1 0 0 0 0 1 0 0
        0 0 0 0 0 0 0 0 0 0 0
        0 4 2 5 2 4 2 4 0 2 0
        11 115 84 63 82 58 46 52 34 30 42""",
    ("Mactar", 20, 24): """
        0 4 3 2 4 9 2 3 3 2 2
        0 0 0 0 0 0 0 1 1 1 1
        0 0 0 0 0 0 0 0 0 0 0
        0 1 0 0 0 0 0 0 0 0 0
        0 0 0 0 0 0 0 0 0 0 0
        0 0 1 0 0 0 0 0 0 0 0
        0 5 4 2 4 9 2 4 4 3 3""",
    ("Sfax", 20, 24): """
        30 140 125 120 138 107 104 104 106 94 95
        4 254 163 221 205 177 179 142 156 200 165
        9 42 67 60 49 48 46 57 9 67 60
        0 0 1 5 1 1 1 3 0 1 0
        3 19 30 25 18 13 9 21 9 5 4
        2 7 9 7 4 4 3 2 5 4 1
        48 462 395 438 415 350 342 329 285 371 325""",
    ("Souk-el-Arba", 20, 24): """
        20 133 73 90 81 54 57 62 46 28 33
        48 129 97 116 85 79 79 99 77 42 34
        0 3 2 0 1 2 1 0 0 2 1
        0 2 0 0 3 1 1 0 0 0 1
        0 0 1 0 0 0 1 1 0 0 0
        1 0 2 0 0 0 2 0 1 0 0
        69 267 175 206 170 136 141 162 124 72 69""",
    ("Tabarca", 20, 24): """
        7 83 96 75 42 47 54 36 40 39 43
        228 79 93 54 41 42 61 42 37 39 41
        2 6 7 1 1 1 1 0 0 1 0
        0 1 0 5 1 5 0 0 1 0 0
        0 0 0 0 0 0 0 0 0 0 0
        0 1 0 0 0 0 0 0 0 0 0
        237 170 196 135 85 95 116 78 78 79 84""",
    # page 21, view 25
    ("Sousse", 21, 25): """
        20 204 135 123 136 101 93 103 84 109 69 1017
        2 226 176 227 233 163 195 203 230 285 138 2483
        0 33 18 34 33 31 38 33 33 38 27 959
        0 1 1 0 0 1 0 0 0 1 2 18
        0 0 2 0 0 0 1 0 1 1 0 8
        5 8 10 3 4 1 0 1 0 0 1 29
        27 472 342 387 406 297 327 340 348 434 237 4514""",
    ("Thala", 21, 25): """
        2 9 4 11 8 7 9 9 9 8 6 54
        0 20 54 16 18 15 21 16 16 16 7 80
        0 0 0 0 0 0 0 0 0 0 0 4
        0 0 0 0 0 0 0 0 0 0 0 0
        0 0 0 0 0 0 0 0 0 0 0 0
        0 0 0 0 0 0 0 0 0 0 0 0
        2 29 58 27 26 22 30 25 25 24 13 138""",
    ("Tunis", 21, 25): """
        407 1698 1286 1281 1112 1040 971 1137 834 877 711 7272
        96 2557 2436 3100 3105 3151 3263 3256 2764 2525 1609 24214
        13 180 165 155 154 180 189 128 156 160 196 4498
        4 31 12 23 22 28 6 10 4 7 12 130
        5 15 4 14 9 12 9 14 12 10 4 185
        79 113 99 82 64 45 53 31 35 37 30 393
        604 4594 4002 4655 4466 4456 4491 4576 3805 3616 2562 36692""",
    ("Territoires du Sud", 21, 25): """
        3 20 18 13 9 6 12 5 5 5 1 36
        0 6 3 7 3 6 3 15 3 5 5 64
        0 8 3 6 1 1 1 0 2 1 0 36
        0 0 0 0 0 0 0 0 1 2 0 5
        0 0 0 0 0 0 0 0 0 1 3 4
        0 1 0 0 2 0 1 0 0 0 1 9
        3 35 24 26 15 13 17 20 11 14 10 154""",
}
# "Ensemble du Territoire de la Régence" (p.21): validation only.
T4_ENSEMBLE = grid("""
    694 3429 2637 2469 2247 1993 1992 2057 1547 1571 1288 12686
    385 4787 4282 5000 5027 4943 5311 5113 4297 3922 2600 35489
    25 328 307 299 288 324 317 258 249 311 313 7311
    5 60 39 52 39 54 20 20 11 15 19 266
    8 48 45 51 33 30 25 38 28 19 18 340
    91 159 166 121 87 70 80 53 50 48 39 552
    1208 8811 7476 7992 7721 7414 7745 7539 6182 5886 4277 56644""")


def table_iv():
    t = "IV"
    rows = []
    agg = [[0] * 12 for _ in range(6)]
    for (circ, page, view), text in T4.items():
        g = grid(text)
        assert len(g) == 7, circ
        derived = len(g[0]) == 11
        nat_rows = [r[:] for r in g[:6]]
        totals = g[6]
        # column checks (visible columns)
        for j in range(len(totals)):
            check(t, f"{circ} col {DUR[j]}", sum(r[j] for r in nat_rows), totals[j])
        for i in range(6):
            if derived:
                nat_rows[i].append(TABLE_I[circ][i] - sum(nat_rows[i]))
                assert nat_rows[i][-1] >= 0, (circ, i)
            else:
                check(t, f"{circ} {NAT[i]} row vs Table I", sum(nat_rows[i]), TABLE_I[circ][i])
        for i in range(6):
            for j in range(12):
                agg[i][j] += nat_rows[i][j]
                flag = "derived_from_totals" if (derived and j == 11) else ""
                rows.append([CENSUS, t, page, view, circ, NAT[i], NAT_FR[i], DUR[j], DUR_FR[j],
                             nat_rows[i][j], flag])
    # regency totals: every nationality x duration, including derived column
    for i in range(6):
        for j in range(12):
            check(t, f"Ensemble {NAT[i]} {DUR[j]}", agg[i][j], T4_ENSEMBLE[i][j])
    for j in range(12):
        check(t, f"Ensemble Totaux {DUR[j]}", sum(agg[i][j] for i in range(6)), T4_ENSEMBLE[6][j])
    for i in range(6):
        check(t, f"Ensemble {NAT[i]} row vs Table I total", sum(T4_ENSEMBLE[i]), TABLE_I_TOTAL[i])
    hdr = ["census", "table_id", "source_page", "gallica_view", "controle_civil", "nationality",
           "nationality_fr", "residence_duration", "residence_duration_fr", "value", "flag"]
    return write("eur1906_t4_residence_duration", hdr, rows)


# --------------------------------------------------------------------------
# Table V (pp.22-23, views 26-27): nationality x age group x marital status x sex.
AGE = ["lt_10", "10_19", "20_29", "30_39", "40_49", "50_59", "60_plus"]
AGE_FR = ["De moins de 10 ans", "10 à 19 ans", "20 à 29 ans", "30 à 39 ans",
          "40 à 49 ans", "50 à 59 ans", "60 ans et au-dessus"]
MAR = [("single", "Célibataires"), ("married", "Mariés"), ("widowed", "Veufs"),
       ("divorced", "Divorcés")]
SEX = [("male", "Sexe masculin"), ("female", "Sexe féminin")]
# columns: single M F, married M F, widowed M F, divorced M F, total
T5 = {
    ("french", "Français", 22, 26): """
        3782 3629 0 0 0 0 0 0 7411
        2553 2445 5 177 0 0 0 1 5181
        2292 1159 1060 2572 12 53 2 32 7182
        982 423 2593 2481 54 154 30 35 6752
        501 204 1950 1331 104 253 50 34 4427
        173 106 939 490 145 347 29 22 2251
        94 65 398 184 178 472 12 3 1406
        10377 8031 6945 7235 493 1279 123 127 34610""",
    ("italian", "Italiens", 22, 26): """
        10314 9770 0 0 0 0 0 0 20084
        8129 7522 34 650 2 4 1 2 16344
        4305 2062 3304 5019 23 69 7 21 14810
        1159 564 5235 4642 91 178 22 31 11922
        520 304 4652 3327 132 388 18 36 9377
        186 102 2532 1640 168 564 17 24 5233
        96 82 1350 733 262 847 10 6 3386
        24709 20406 17107 16011 678 2050 75 120 81156""",
    ("maltese", "Maltais", 22, 26): """
        1260 1214 0 0 0 0 0 0 2474
        1034 1029 2 47 1 0 0 1 2114
        648 388 256 481 2 16 3 2 1796
        230 108 458 492 11 38 3 10 1350
        123 62 481 360 32 99 5 3 1165
        67 40 327 209 31 126 6 6 812
        36 28 192 90 57 206 5 5 619
        3398 2869 1716 1679 134 485 22 27 10330""",
    ("spanish", "Espagnols", 23, 27): """
        56 53 0 0 0 0 0 0 109
        56 45 0 3 0 0 0 0 104
        39 28 11 23 0 2 1 0 104
        27 21 24 31 1 2 1 1 108
        12 13 27 17 5 4 0 0 78
        8 6 19 11 5 6 2 1 58
        3 0 10 6 2 18 0 0 39
        201 166 91 91 13 32 4 2 600""",
    ("greek", "Grecs", 23, 27): """
        86 70 0 0 0 0 0 0 156
        53 44 0 6 1 0 0 0 104
        56 23 12 39 0 2 0 0 132
        36 7 33 30 3 2 0 0 111
        20 4 40 17 3 3 0 0 87
        11 0 31 6 2 6 0 1 57
        4 3 10 2 5 12 0 0 36
        266 151 126 100 14 25 0 1 683""",
    ("other_european", "Autres Européens", 23, 27): """
        123 116 0 0 0 0 0 0 239
        104 73 1 7 0 0 0 0 185
        174 100 31 55 0 0 0 0 360
        69 61 87 77 6 3 0 4 307
        25 36 82 60 5 12 1 1 222
        10 14 59 23 6 10 0 1 123
        7 11 21 16 6 17 0 2 80
        512 411 281 238 23 42 1 8 1516""",
}
T5_GRAND = [39463, 32034, 26266, 25354, 1355, 3913, 225, 285, 128895]


def table_v():
    t = "V"
    rows = []
    grand = [0] * 9
    for (nat, nat_fr, page, view), text in T5.items():
        g = grid(text)
        assert len(g) == 8 and all(len(r) == 9 for r in g), nat
        for i, r in enumerate(g[:7]):
            check(t, f"{nat} {AGE[i]} row", sum(r[:8]), r[8])
        for j in range(9):
            check(t, f"{nat} col {j}", sum(r[j] for r in g[:7]), g[7][j])
            grand[j] += g[7][j]
        check(t, f"{nat} total vs Table I", g[7][8], TABLE_I_TOTAL[NAT.index(nat)])
        for i, r in enumerate(g[:7]):
            for m, (mar, mar_fr) in enumerate(MAR):
                for s, (sex, sex_fr) in enumerate(SEX):
                    rows.append([CENSUS, t, page, view, nat, nat_fr, AGE[i], AGE_FR[i],
                                 mar, mar_fr, sex, sex_fr, r[2 * m + s], ""])
    for j in range(9):
        check(t, f"Totaux généraux col {j}", grand[j], T5_GRAND[j])
    hdr = ["census", "table_id", "source_page", "gallica_view", "nationality", "nationality_fr",
           "age_group", "age_group_fr", "marital_status", "marital_status_fr", "sex", "sex_fr",
           "value", "flag"]
    return write("eur1906_t5_sex_age_marital", hdr, rows)


# --------------------------------------------------------------------------
# Table VIII (p.34, view 33): instruction. "Parlant français" was not asked of
# the French (footnote 1), so that cell is NA, not zero.
T8 = [
    ("reads_only", "Sachant lire seulement", [223, 872, 105, 9, 0, 6], 1215),
    ("reads_and_writes", "Sachant lire et écrire", [25324, 28426, 4125, 331, 417, 1021], 59644),
    ("speaks_french", "Parlant français", [None, 27008, 4959, 399, 366, 1026], 33758),
]


def table_viii():
    t = "VIII"
    rows = []
    nat_fr = ["Français", "Italiens", "Maltais", "Espagnols", "Grecs", "Autres Européens"]
    for ind, ind_fr, vals, tot in T8:
        check(t, f"{ind} row", sum(v or 0 for v in vals), tot)
        for i, v in enumerate(vals):
            rows.append([CENSUS, t, 34, 33, NAT[i], nat_fr[i], ind, ind_fr,
                         "" if v is None else v, "not_applicable" if v is None else ""])
    hdr = ["census", "table_id", "source_page", "gallica_view", "nationality", "nationality_fr",
           "indicator", "indicator_fr", "value", "flag"]
    return write("eur1906_t8_instruction", hdr, rows)


# --------------------------------------------------------------------------
# Analysis tables in the commentary (pp.35-65). Decimal values are printed with
# a space for the decimal point ("28 3" = 28.3).
CIRCS = list(TABLE_I)  # printed order of circonscriptions in Tables A-C

# Table A (p.35, view 34): % of each nationality in the European population,
# area (myriamètres carrés = 100 km2) and Europeans per myriamètre carré.
# None = "»" (area not determined: Gafsa, Tozeur, Territoires du Sud).
T_A = """
Béja 28.3 69.0 1.5 1.1 14 194.8
Medjez-el-Bab 51.4 43.6 2.8 2.1 23.5 39.4
Bizerte 31.8 63.8 3.5 1.3 35 413.9
Gabès 36.9 40.1 21.5 1.4 53.5 17
Djerba 27.2 12.5 50.2 10.0 6 114.5
Gafsa 33.8 62.0 2.5 1.6 None None
Tozeur 79.5 17.2 0 3.2 None None
Grombalia 31.3 61.3 5 2.3 29.5 111.6
Kairouan 34.6 55.1 2.7 7.6 72 17.3
Le_Kef 27.3 68.9 1.9 1.8 53 53.8
Téboursouk 47.7 46.4 1.5 4.3 13 69.4
Mactar 77.3 16.4 2.1 4.1 28.5 3.4
Sfax 26.9 48.6 19.5 4.9 91 73.5
Souk-el-Arba 38.9 58.0 1.6 1.3 19 135.7
Tabarca 42.1 54.9 1.3 1.5 12.5 161.1
Sousse 27.0 56.0 15.6 1.2 62 131.1
Thala 32.9 66.4 0.9 0 93.3 4.5
Tunis 23.7 66.4 7.8 2 58 1353.7
Territoires_du_Sud 38.9 35.0 17.2 8.8 None None
Ensemble_du_territoire 26.8 63.0 8.0 2.1 663.8 194.2
"""
# Printed spelling in Table A is "Teboursouk"; Table I/IV print "Teboursouk"/"Téboursouk".
A_NAMES = {"Téboursouk": "Teboursouk"}


def num(x):
    return None if x == "None" else float(x)


def table_a():
    t = "A"
    rows = []
    ind = [("pct_french", "Proportion % : Français"),
           ("pct_italian", "Proportion % : Italiens"),
           ("pct_maltese", "Proportion % : Maltais"),
           ("pct_other_european", "Proportion % : Autres Européens"),
           ("area_myriametres2", "Superficie en myriamètres carrés"),
           ("europeans_per_myriametre2", "Nombre d'européens par myriamètre carré")]
    area_sum = 0.0
    for ln in T_A.strip().splitlines():
        p = ln.split()
        name = p[0].replace("_", " ")
        v = [num(x) for x in p[1:]]
        bad = set()
        if name == "Ensemble du territoire":
            tot = TABLE_I_TOTAL
            check(t, "Ensemble area = sum of areas", round(area_sum, 1), v[4])
            # footnote 1: total population over the area of the circonscriptions
            # whose area is known (i.e. Gafsa and Territoires du Sud left out)
            dens = tot[6] / v[4]
            ok = abs(dens - v[5]) < 0.1
            check(t, "Ensemble density", ok, True)
            label = "Ensemble du territoire (printed)"
        else:
            tot = TABLE_I[name]
            if v[4] is not None:
                area_sum += v[4]
                dens = tot[6] / v[4]
                ok = abs(dens - v[5]) < 0.1
                check(t, f"{name} density {dens:.2f}", ok, True)
                if not ok:
                    bad.add(5)
            label = A_NAMES.get(name, name)
        shares = [tot[0], tot[1], tot[2], tot[3] + tot[4] + tot[5]]
        for k in range(4):
            pct = 100 * shares[k] / tot[6]
            # the source mixes truncation and rounding to one decimal
            ok = abs(pct - v[k]) < 0.1
            check(t, f"{name} {ind[k][0]} recomputed {pct:.2f}", ok, True)
            if not ok:
                bad.add(k)
        for k, (code, fr) in enumerate(ind):
            flag = "not_applicable" if v[k] is None else ("total_mismatch" if k in bad else "")
            rows.append([CENSUS, t, 35, 34, label, code, fr, "" if v[k] is None else v[k], flag])
    hdr = ["census", "table_id", "source_page", "gallica_view", "controle_civil", "indicator",
           "indicator_fr", "value", "flag"]
    return write("eur1906_ta_nationality_shares_density", hdr, rows)


# Table B (p.37, view 36): French civilian population by circonscription.
# Differences (printed) are used for validation only.
T_B = """
Béja 91 230 436 773 139 206 337 682
Medjez-el-Bab 74 146 323 476 72 177 153 402
Bizerte 501 934 3559 4611 433 2625 1052 4110
Gabès 246 306 324 335 60 18 11 89
Djerba 86 153 187 187 67 34 0 101
Gafsa 73 174 367 661 101 193 294 588
Tozeur 28 50 69 74 22 19 5 46
Grombalia 168 406 717 1031 238 311 314 863
Kairouan 68 239 300 432 171 61 132 364
Le_Kef 228 306 386 781 78 80 395 553
Teboursouk 17 104 160 431 87 56 271 414
Mactar 35 38 114 75 3 76 -39 40
Sfax 431 798 1373 1801 367 575 428 1370
Souk-el-Arba 394 571 708 1004 177 137 296 610
Tabarca 297 475 522 849 178 47 327 552
Sousse 918 1446 1662 2194 528 216 532 1276
Thala 29 87 106 136 58 19 30 107
Tunis 6240 9667 12793 18626 3327 3126 5833 12386
Territoires_du_Sud 49 77 95 133 28 18 38 84
"""
T_B_TOTAL = [9973, 16207, 24201, 34610, 6234, 7994, 10409, 24637]
YEARS = [1891, 1896, 1901, 1906]
T_B_POP = {}


def table_b():
    t = "B"
    rows = []
    cols = [0] * 8
    for ln in T_B.strip().splitlines():
        p = ln.split()
        name = p[0].replace("_", " ")
        v = [int(x) for x in p[1:]]
        T_B_POP[name] = v[:4]
        for j in range(8):
            cols[j] += v[j]
        check(t, f"{name} 1896-1891", v[1] - v[0], v[4])
        check(t, f"{name} 1901-1896", v[2] - v[1], v[5])
        check(t, f"{name} 1906-1901", v[3] - v[2], v[6])
        check(t, f"{name} 1906-1891", v[3] - v[0], v[7])
        key = "Téboursouk" if name == "Teboursouk" else name
        check(t, f"{name} 1906 vs Table I", v[3], TABLE_I[key][0])
        for y, val in zip(YEARS, v[:4]):
            rows.append([CENSUS, t, 37, 36, name, y, val, ""])
    for j in range(8):
        check(t, f"Total col {j}", cols[j], T_B_TOTAL[j])
    hdr = ["census", "table_id", "source_page", "gallica_view", "controle_civil", "census_year",
           "value", "flag"]
    return write("eur1906_tb_french_population_1891_1906", hdr, rows)


# Table C (p.39, view 38): growth coefficients of the French population.
# Columns: 1896/1891, 1901/1891, 1906/1891, 1901/1896, 1906/1901.
T_C = """
Béja 2.52 4.79 8.49 1.89 1.77
Medjez-el-Bab 1.97 4.36 6.43 2.21 1.47
Bizerte 1.86 7.10 9.20 3.81 1.29
Gabès 1.24 1.32 1.36 1.05 1.03
Djerba 1.77 2.17 2.17 1.22 1.00
Gafsa 2.38 5.02 9.05 2.10 1.80
Tozeur 1.78 2.46 2.64 1.38 1.07
Grombalia 2.41 4.26 6.14 1.76 1.43
Kairouan 3.51 4.41 6.35 1.25 1.44
Le_Kef 1.35 1.69 3.42 1.25 2.04
Teboursouk 5.82 9.41 25.35 1.53 2.67
Mactar 1.08 3.25 2.14 3.00 0.65
Sfax 1.85 3.18 4.17 1.72 1.31
Souk-el-Arba 1.44 1.76 2.54 1.23 1.41
Tabarca 1.59 1.75 2.88 1.09 1.62
Sousse 1.57 1.81 2.38 1.14 1.30
Thala 3.00 3.65 4.68 1.21 1.28
Tunis 1.54 2.05 2.98 1.32 1.45
Territoires_du_Sud 1.59 1.93 2.71 1.23 1.40
Ensemble_du_territoire 1.72 2.42 3.47 1.49 1.42
"""
C_PAIRS = [(1891, 1896), (1891, 1901), (1891, 1906), (1896, 1901), (1901, 1906)]


def table_c():
    t = "C"
    rows = []
    for ln in T_C.strip().splitlines():
        p = ln.split()
        name = p[0].replace("_", " ")
        v = [float(x) for x in p[1:]]
        pop = T_B_POP.get(name) or T_B_TOTAL[:4]
        for (b, e), val in zip(C_PAIRS, v):
            ratio = pop[YEARS.index(e)] / pop[YEARS.index(b)]
            ok = abs(ratio - val) <= 0.011
            check(t, f"{name} {e}/{b} recomputed {ratio:.3f}", ok, True)
            label = name + (" (printed)" if name == "Ensemble du territoire" else "")
            rows.append([CENSUS, t, 39, 38, label, b, e, val, "" if ok else "total_mismatch"])
    hdr = ["census", "table_id", "source_page", "gallica_view", "controle_civil", "base_year",
           "census_year", "value", "flag"]
    return write("eur1906_tc_french_growth_coefficients", hdr, rows)


# Table D (pp.41-45, views 40-44): French civilian population by locality,
# 1891, 1896, 1901, grouped by the contrôle civil / annexe of the time.
# Format: "# <unit>" starts a unit; "page view" lines set the source; each
# locality line is "name | v1891 v1896 v1901" ('-' = cell not printed).
T_D = """
@ 41 40
# Contrôle de Béja
Béja | 71 168 234
Béja (banlieue) | 0 0 21
Amdoun | 0 0 23
Djebel-ben-Drahar, Djebel-Brika, Djebel-Charra, Hammam-es-Semane, Hammam-M'Seïda, Khanguet-Kef-Tout, Oued-Maden et Sidi-Ahmed | 14 32 0
Khanguet-Kef-Tout | 0 0 19
Monchar | 6 23 74
Nefza | 0 0 44
Pont-de-Trajan | 0 7 9
Rebahine | 0 0 12
# Annexe de Medjez-el-Bab
Medjez-el-Bab | 22 61 111
Aïn-Tounga | 0 4 0
Bou-Arada | 0 20 17
Bordj-French | 0 0 5
Bordj-Toum | 18 5 0
Chassart-Tefaha | 0 18 27
Ghanem el-Kebir | 0 3 5
Goubellat | 0 0 76
Ksar-Tyr | 10 6 36
Oued-Zargua | 24 23 30
Testour | 0 6 16
# Contrôle de Bizerte
Bizerte | 466 748 2475
Aïn-Berda, camp | 0 0 25
Aïn-Bittar | 0 0 54
Aïn-Roumi | 1 0 8
Aïn-Meriem | 0 0 6
Baie Sans-Nom | 0 0 90
Cap Blanc | 0 0 2
Cap Serrat | 0 7 0
Dar-el-Koudiat | 0 0 6
Djebel-Kebir | 0 0 5
Djebel-Rara (fort) | 0 0 55
Djebel-Nador (fort) | 0 0 23
El-Alia | 0 10 0
El-Ajib (route de Tunis) | 0 0 9
El-Euch (fort) | 0 0 15
El-Azonaj (camp) | 0 0 15
El-Haouid | 7 8 0
Fartout | 0 5 0
Ferryville | 0 0 338
Ile Cani | 0 12 0
Jalta | 0 1 0
Mateur (ville et gare) | 10 34 114
Région de Mateur | 0 14 161
Menzel-Djemil | 0 7 10
M'Kada | 3 0 0
Oued-Tindja | 0 0 13
Porto-Farina | 14 24 34
Ras-el-Djebel | 0 12 24
# Contrôle de Gabès
Gabès (port) | 241 256 240
Chenini | 0 8 3
Djarra | 0 31 57
El-Hamma | 0 4 1
Menzel | 1 6 14
Oued-Melah | 1 1 9
Ras-el-Oued | 3 0 0
# Annexe de Djerba
Affar | 0 0 6
Beni-Diss | 0 0 7
Bordj-Djellidj | 0 5 7
Djouana | 0 2 0
El-Adjim | 0 16 12
El-Haddada | 0 1 0
El-Kantara | 0 0 3
Gallala | 0 7 60
@ 42 41
Hara-Kebira | 0 3 5
Houmt-Souk | 86 98 121
Metrech | 0 6 0
Midoun | 0 1 3
Ouallag | 0 3 5
Ras-Tuguernisse | 0 5 12
Tadjimès | 0 2 0
Tesdaïn | 0 4 0
# Contrôle de Gafsa
Gafsa-ville | 0 0 166
Gafsa-gare | 70 158 38
El-Haffen | 3 4 0
El-Guettar | 0 8 0
Gamouda | 0 1 3
Maknassy | 0 0 17
Maisonnette des équipes | 0 0 9
Oum-el-Ksob | 0 3 1
Metlaoui | 0 0 133
# Annexe de Tozeur
Tozeur | 21 37 52
El-Hamma | 1 0 0
El-Oudiane | 1 0 2
Nefta | 5 10 9
Tamerza | 0 3 6
# Contrôle de Grombalia
Grombalia | 34 80 105
Grombalia (banlieue) | 0 0 15
Belli | 0 0 13
Beni-Khaled | 0 0 3
Bir-bou-Rekba | 0 12 8
Bou-Argoub | 0 22 9
Cap Bon | 7 11 13
Fondouk-Djedid | 11 15 55
Fondouk-Djedid (banlieue) | 0 0 36
Hammamet | 4 33 58
Kelibia | 0 13 28
Khanguet | 11 66 118
Korba | 0 0 5
Korbeus | 0 0 1
Menzel-Temime | 9 11 11
Menzel-bou-Zelfa | 0 2 8
Nabeul | 55 90 143
Nianou | 0 0 4
Sidi-Daoud | 0 0 1
Soliman | 37 15 42
Takelsa | 0 36 34
Tazerka | 0 0 6
Turki | 0 0 1
# Contrôle de Kairouan
Ville de Kairouan, quartier : Banlieue | 3 0 7
Ville de Kairouan, quartier : Chorfa | 0 0 33
Ville de Kairouan, quartier : Djelbia | 0 0 14
Ville de Kairouan, quartier : Européen | 0 0 129
Ville de Kairouan, quartier : de la Grande Mosquée | 0 0 79
Ville de Kairouan, quartier : de Kheblia | 58 225 4
El-Ala | 0 3 4
Hadjeb-el-Aïoun | 2 2 1
Région de Saadia | 5 9 6
Sidi-Mohamed-b.-Ali | 0 0 23
# Contrôle du Kef
Kef | 210 258 291
Aïn-Touireuf | 0 0 1
Bou-Djabeur | 0 6 6
Djebel-Harraba | 0 3 3
Djebel-Kebbauch | 0 0 4
Fedj-Hassein | 0 0 9
Kalâa-Djerda | 0 1 0
Korhens | 0 0 2
Ksour | 0 7 11
Nebeur | 5 3 6
Oued-Remel | 0 4 0
Oulad-bou-Ghanem | 5 6 3
Sakiet-Sidi-Youssef | 6 16 48
Sers | 0 1 1
Zouarines | 2 1 1
@ 43 42
# Annexe de Teboursouk
Teboursouk | 15 42 56
Aïn-Djemala | 0 0 1
Aïn-el-Garça | 0 0 1
Aïn-Guettar | 0 0 2
Aïn-Hedja | 0 0 4
Bordj-Messaoudi | 0 4 0
Djebba | 0 5 5
Douar Neffet | 0 0 4
Douemis | 0 0 6
El-Akhouat | 0 5 7
Fedj-el-Adoum | 0 3 5
Gafour | 0 8 3
Khalled | 0 5 0
Korib | 0 0 10
Krib | 0 11 0
Nemcha | 0 0 6
St-Joseph-de-Thibar | 0 10 23
Ste-Marie-de-Thibar | 0 0 4
St-Martin-de-Thibar | 0 0 1
Sidi-Zehili | 2 11 6
Teboursouk (camp militaire) | 0 0 14
Tella | 0 0 4
# Contrôle de Mactar
Mactar | 14 26 28
Aïn-Dridja | 0 0 30
Aïn-Sedja | 0 0 2
Aïn-Mzita | 3 0 0
Kessara | 1 2 1
Oued-Ceddine | 0 1 0
Ouzafa | 0 2 0
Rouhia | 0 0 2
Sidi-Saïd | 0 0 48
Souk-el-Djemaa | 17 7 0
Souk-el-Khemis-de-Silama | 0 0 3
# Contrôle de Sfax
Ville de Sfax, quartier : Arabe | 0 0 175
Ville de Sfax, quartier : Européen | 420 590 283
Ville de Sfax, quartier : Gendarmerie | 0 19 21
Ville de Sfax, quartier : Gautheronville | 0 38 34
Ville de Sfax, quartier : Marine | 0 0 460
Ville de Sfax, quartier : Moulinville | 0 27 87
Ville de Sfax, quartier : Picville | 0 43 132
Ville de Sfax, quartier : Banlieue | 0 27 41
Graïba | 0 0 16
Landas-Dajinville | 0 0 7
La Skira | 7 5 12
Autres lieux | 4 49 105
# Contrôle de Souk-el-Arba
Souk-el-Arba | 246 368 439
Ben-Bachir | 1 7 13
Djebel-Chouichia | 0 0 9
El-Feïdja | 22 33 34
Ghardimaou | 64 80 77
Oued-Meliz-Chemtou | 11 9 8
Sidi-Meskine | 9 5 3
Souk-el-Khemis | 41 69 125
# Annexe de Tabarca
Tabarca | 134 286 258
Aïn-Draham | 163 189 105
Beni-Mazem | 0 0 9
Ile de la Galite | 0 0 26
Ghazouane | 0 0 20
Khroumir-Atatfa | 0 0 52
Khroumir-Tabarca | 0 0 44
Mekna | 0 0 8
# Contrôle de Sousse
Sousse | 691 1036 1059
Bou-Ficha | 0 0 17
Djemmal | 2 21 19
@ 44 43
El-Djem | 0 4 8
Enfidaville | 60 84 107
Hammam-Sousse | 0 5 3
Hergla | 1 0 0
Kalâa-Kebira | 0 6 8
Kalâa-Sghira | 0 7 10
Kroussiah | 16 0 7
Ksar-Ellal | 4 3 3
Ksour-Essaf | 0 11 11
Mahdia | 60 90 131
Menzel-dar-bel-Ouar | 0 0 3
Moknine | 2 22 22
Monastir | 57 98 123
M'Saken | 0 6 12
Oued-Laya | 0 0 5
Reyville | 0 0 1
Route de Monastir | 0 0 90
Saïada | 4 0 0
Sahalines | 3 0 7
Sidi-bou-Ali | 7 8 10
Sidi-el-Hani | 5 8 4
Souassi | 0 10 2
Soya | 6 0 0
Teboulba | 0 12 0
Touza | 0 15 0
# Contrôle de Thala
Thala | 0 2 6
Aïn-Frara | 0 0 1
Aïn-Khemouda | 0 0 3
Bir-oum-Ali | 3 8 3
Bou-Chebka | 1 13 18
Dernaïa | 0 3 8
El-Oubira | 4 5 4
Feriana | 11 5 13
Haïdra | 2 4 2
Kasserine | 1 0 4
Lagered | 0 0 3
Sbeïtla | 0 0 2
Sbiba | 0 2 6
# Contrôle de Tunis
Tunis | 4832 7585 9617
Ariana | 0 19 68
Bir-M'Cherga | 0 0 38
Bordj-Toum | 0 0 7
Bordj-Touta | 0 0 13
Carthage | 145 177 196
Chaouat | 0 0 37
Choutrana | 0 0 13
Crétéville | 39 67 63
Djebel-Djelloud | 0 51 26
Djedeïda | 37 38 63
Hammam-Lif | 34 143 225
La Goulette | 497 330 405
La Manouba | 80 126 220
La Marsa | 71 136 151
La Sokra | 18 18 33
Le Bardo | 0 0 97
Le Kram | 6 28 64
Maxula-Radès et Megrine | 70 167 -
Maxula-Radès | - - 225
Megrine | - - 14
Mohammedia | 41 89 39
Mornag | 60 92 340
Mornaghia | 0 0 52
Nassen | 0 0 19
Pont-du-Fahs | 0 0 23
Potinville | 33 107 78
Ras-Tabia | 0 0 40
Saint-Cyprien | 0 0 12
Sainte-Marie-du-Zit | 0 0 90
Schuiggui | 0 0 33
Sebguine | 0 0 10
Sedjoumi | 0 0 53
Sidi-Athmane | 0 0 18
Sidi-Tabet | 25 30 57
Smindja | 0 58 0
@ 45 44
Tebourba | 110 137 189
Zaghouan | 0 76 165
# Territoire du Sud
Ben-Ghardane | 0 0 2
El-Biban | 0 0 9
Kebili | 0 11 12
Mansourah | 0 1 0
Matmata-Kebira | 0 2 1
Medenine | 13 23 23
Tatahouine | 13 7 4
Zarzis | 23 33 44
"""
D_TO_B = {"Contrôle de Béja": "Béja", "Annexe de Medjez-el-Bab": "Medjez-el-Bab",
          "Contrôle de Bizerte": "Bizerte", "Contrôle de Gabès": "Gabès",
          "Annexe de Djerba": "Djerba", "Contrôle de Gafsa": "Gafsa",
          "Annexe de Tozeur": "Tozeur", "Contrôle de Grombalia": "Grombalia",
          "Contrôle de Kairouan": "Kairouan", "Contrôle du Kef": "Le Kef",
          "Annexe de Teboursouk": "Teboursouk", "Contrôle de Mactar": "Mactar",
          "Contrôle de Sfax": "Sfax", "Contrôle de Souk-el-Arba": "Souk-el-Arba",
          "Annexe de Tabarca": "Tabarca", "Contrôle de Sousse": "Sousse",
          "Contrôle de Thala": "Thala", "Contrôle de Tunis": "Tunis",
          "Territoire du Sud": "Territoires du Sud"}
T_D_UNIT_DIFFS = []


def table_d():
    t = "D"
    rows = []
    page = view = None
    unit = None
    sums = {}
    for ln in T_D.strip().splitlines():
        ln = ln.strip()
        if ln.startswith("@"):
            page, view = map(int, ln[1:].split())
            continue
        if ln.startswith("#"):
            unit = ln[1:].strip()
            sums.setdefault(unit, [0, 0, 0])
            continue
        name, vals = [s.strip() for s in ln.split("|")]
        for k, x in enumerate(vals.split()):
            if x == "-":
                continue
            sums[unit][k] += int(x)
            ctrl, annexe = (unit, "") if not unit.startswith("Annexe") else ("", unit)
            rows.append([CENSUS, t, page, view, unit, name, YEARS[k], int(x), ""])
    tot = [0, 0, 0]
    for unit, s in sums.items():
        for k in range(3):
            tot[k] += s[k]
        b = T_B_POP[D_TO_B[unit]][:3]
        if s != b:
            T_D_UNIT_DIFFS.append(f"{unit}: Table D {s} vs Table B {b}")
    for k in range(3):
        check(t, f"Regency total {YEARS[k]} vs Table B total", tot[k], T_B_TOTAL[k])
    hdr = ["census", "table_id", "source_page", "gallica_view", "controle_civil", "locality",
           "census_year", "value", "flag"]
    return write("eur1906_td_french_population_by_locality_1891_1901", hdr, rows)


# Table E (pp.46-48, views 45-47): French civilian population by place of birth.
# The printed "à reporter" running totals are used for validation.
T_E = """
@ 46 45
Tunisie | 1838 3339 5314 9239
Algérie : Alger | 417 650 841 1274
Algérie : Constantine | 908 1521 2377 3529
Algérie : Oran | 162 213 439 448
Ain | 84 125 159 201
Aisne | 19 36 68 86
Allier | 34 96 155 186
Alpes (Basses-) | 82 108 158 195
Alpes (Hautes-) | 127 165 265 360
Alpes-Maritimes | 82 119 130 169
Ardèche | 104 164 247 346
Ardennes | 18 39 42 65
Ariège | 47 70 109 142
Aube | 24 37 47 60
Aude | 97 127 222 301
Aveyron | 114 178 280 321
Bouches-du-Rhône | 414 569 779 822
Calvados | 17 29 23 54
Cantal | 16 37 54 64
Charente | 40 74 120 144
Charente-Inférieure | 75 131 200 227
Cher | 33 74 101 128
Corrèze | 32 60 78 119
Corse | 574 917 1452 2022
Côte-d'Or | 64 114 172 212
Côtes-du-Nord | 43 50 90 119
Creuse | 19 26 44 63
Dordogne | 87 111 151 224
Doubs | 84 148 167 203
Drôme | 116 181 284 335
Eure | 16 18 42 46
Eure-et-Loire | 10 20 44 38
Finistère | 19 43 95 192
Gard | 164 260 343 497
Garonne (Haute-) | 95 177 222 287
Gers | 54 81 102 145
= 6131 10107 15426 22964
@ 47 46
Gironde | 101 170 266 324
Hérault | 135 186 291 368
Ile-et-Vilaine | 30 49 78 106
Indre | 16 49 65 82
Indre-et-Loire | 19 48 91 96
Isère | 173 321 420 546
Jura | 61 87 144 179
Landes | 34 35 73 92
Loire-et-Cher | 32 38 63 72
Loire | 130 169 254 283
Loire (Haute-) | 44 79 113 160
Loire-Inférieure | 40 62 111 151
Loiret | 26 58 81 29
Lot | 46 83 88 115
Lot-et-Garonne | 64 98 134 178
Lozère | 23 40 41 77
Maine-et-Loire | 32 58 73 93
Manche | 25 34 53 78
Marne | 31 52 87 114
Marne (Haute-) | 32 55 65 79
Mayenne | 12 35 49 52
Meurthe-et-Moselle | 75 187 160 185
Meuse | 23 45 78 68
Morbihan | 28 48 79 134
Nièvre | 43 60 85 116
Nord | 69 116 167 199
Oise | 16 26 44 56
Orne | 19 27 32 42
Pas-de-Calais | 32 60 84 105
Puy-de-Dôme | 58 99 169 185
Pyrénées (Basses-) | 62 82 157 206
Pyrénées (Hautes-) | 43 66 119 164
Pyrénées-Orientales | 62 94 180 298
Rhin (Haut-) Belfort | 7 101 54 97
Rhône | 291 448 478 635
= 8055 13362 19972 28778
@ 48 47
Saône (Haute-) | 47 72 93 125
Saône-et-Loire | 102 177 194 296
Sarthe | 18 27 46 52
Savoie | 103 163 203 262
Savoie (Haute-) | 51 74 109 148
Seine | 408 531 802 1228
Seine-Inférieure | 43 76 112 131
Seine-et-Marne | 25 48 53 89
Seine-et-Oise | 49 70 90 147
Sèvres (Deux-) | 33 71 97 130
Somme | 20 51 56 70
Tarn | 56 88 170 194
Tarn-et-Garonne | 26 46 79 103
Var | 118 189 256 403
Vaucluse | 119 181 202 283
Vendée | 9 32 26 45
Vienne | 17 39 87 93
Vienne (Haute-) | 49 67 174 132
Vosges | 47 73 97 119
Yonne | 37 54 89 101
Colonies et Possessions Françaises | 18 27 49 57
Etranger | 523 689 1145 1602
Lieu inconnu | 0 0 0 22
= 9973 16207 24201 34610
"""


# Cells printed inconsistently with the page running totals and the commentary
# (pp.44-45): Bouches-du-Rhône 1906 printed 822 (commentary 922, +143 since
# 1901); Rhône 1901 printed 478 (commentary +137 => 498); Loiret 1906 printed
# 29 (page total implies 79). Printed values kept. Allier 1891: first digit
# broken in the scan, read as 34.
E_FLAGS = {("Bouches-du-Rhône", 1906): "total_mismatch", ("Rhône", 1901): "total_mismatch",
           ("Loiret", 1906): "total_mismatch", ("Allier", 1891): "ocr_corrected"}


def table_e():
    t = "E"
    rows = []
    run = [0, 0, 0, 0]
    page = view = None
    for ln in T_E.strip().splitlines():
        ln = ln.strip()
        if ln.startswith("@"):
            page, view = map(int, ln[1:].split())
        elif ln.startswith("="):
            printed = [int(x) for x in ln[1:].split()]
            for k in range(4):
                check(t, f"running total p.{page} {YEARS[k]}", run[k], printed[k])
        else:
            name, vals = [s.strip() for s in ln.split("|")]
            v = [int(x) for x in vals.split()]
            for k in range(4):
                run[k] += v[k]
                flag = E_FLAGS.get((name, YEARS[k]), "")
                rows.append([CENSUS, t, page, view, name, YEARS[k], v[k], flag])
    for k in range(4):
        check(t, f"total {YEARS[k]} vs Table B", run[k], T_B_TOTAL[k])
    hdr = ["census", "table_id", "source_page", "gallica_view", "birthplace_fr", "census_year",
           "value", "flag"]
    return write("eur1906_te_french_by_birthplace_1891_1906", hdr, rows)


# Table F (p.54, view 53): French population by origin of nationality x age x
# marital status x sex. Columns: single M F, married M F, widowed M F, divorced M F.
T_F = {
    ("by_birth", "Français de naissance"): """
        3620 3494 0 0 0 0 0 0
        2410 2303 5 143 0 0 0 1
        2220 1128 1004 2294 12 43 2 30
        952 417 2472 2213 52 146 30 35
        467 199 1809 1170 98 232 46 33
        163 104 858 432 139 330 25 22
        91 61 349 164 166 455 11 3
        = 9923 7706 6497 6416 467 1206 114 124 32453""",
    ("naturalised", "Français par naturalisation, option ou mariage"): """
        162 135 0 0 0 0 0 0
        143 142 0 34 0 0 0 0
        72 31 56 278 0 10 0 2
        30 6 121 268 2 8 0 0
        34 5 141 161 6 21 4 1
        10 2 81 58 6 17 4 0
        3 4 49 20 12 17 1 0
        = 454 325 448 819 26 73 9 3 2157""",
}


def table_f():
    t = "F"
    rows = []
    fr_v = [r for r in grid(T5[("french", "Français", 22, 26)])]  # Table V, French block
    combined = [[0] * 8 for _ in range(7)]
    for (orig, orig_fr), text in T_F.items():
        lines = [l.strip() for l in text.strip().splitlines()]
        g = grid("\n".join(lines[:7]))
        tot = [int(x) for x in lines[7][1:].split()]
        for j in range(8):
            check(t, f"{orig} col {j}", sum(r[j] for r in g), tot[j])
        check(t, f"{orig} grand total", sum(tot[:8]), tot[8])
        for i, r in enumerate(g):
            for j in range(8):
                combined[i][j] += r[j]
            for m, (mar, mar_fr) in enumerate(MAR):
                for s, (sex, sex_fr) in enumerate(SEX):
                    rows.append([CENSUS, t, 54, 53, orig, orig_fr, AGE[i], AGE_FR[i], mar, mar_fr,
                                 sex, sex_fr, r[2 * m + s], ""])
    for i in range(7):
        for j in range(8):
            check(t, f"by_birth+naturalised vs Table V french {AGE[i]} col {j}",
                  combined[i][j], fr_v[i][j])
    hdr = ["census", "table_id", "source_page", "gallica_view", "nationality_origin",
           "nationality_origin_fr", "age_group", "age_group_fr", "marital_status",
           "marital_status_fr", "sex", "sex_fr", "value", "flag"]
    return write("eur1906_tf_french_by_origin_sex_age_marital", hdr, rows)


# Table G (pp.62-63, view 61): French population by occupational group x sex,
# by circonscription, 1906 and 1901. Columns per group: men women (totals are
# printed and used for validation).
G_GROUPS = [("agriculture", "Agriculture"), ("commerce", "Commerce"), ("industry", "Industrie"),
            ("transport", "Transports"), ("public_administration", "Administrations publiques"),
            ("police_force", "Force publique"), ("liberal_professions", "Professions libérales"),
            ("independent_means", "Personnes vivant exclusivement de leurs revenus"),
            ("unclassified", "Population non classée")]
# each line: circ year | (M F T) x 9 groups | M F T totals
T_G = """
Béja et Medjez-el-Bab 1906 | 269 203 472 57 61 118 127 71 198 72 49 121 110 77 187 15 17 32 21 19 40 4 6 10 5 19 24 730 522 1252
Béja et Medjez-el-Bab 1901 | 165 103 268 46 47 93 100 68 168 30 21 51 72 58 130 12 11 23 12 12 24 1 1 2 0 0 0 438 321 759
Bizerte 1906 | 337 199 536 258 218 476 552 416 968 213 186 399 509 435 944 47 47 94 70 72 142 200 463 663 110 279 389 2296 2315 4611
Bizerte 1901 | 220 124 344 355 278 633 831 616 1447 91 77 168 207 152 359 92 184 276 65 71 136 84 106 190 5 1 6 1950 1609 3559
Gabès 1906 | 4 3 7 18 20 38 55 61 116 2 2 4 56 79 135 5 1 6 4 6 10 10 8 18 0 1 1 154 181 335
Gabès 1901 | 16 6 22 43 39 82 42 33 75 1 0 1 49 32 81 10 25 35 5 6 11 6 11 17 0 0 0 172 152 324
Djerba 1906 | 9 10 19 15 17 32 11 11 22 0 0 0 57 40 97 1 0 1 2 7 9 2 1 3 2 2 4 99 88 187
Djerba 1901 | 20 19 39 10 8 18 17 17 34 9 5 14 34 38 72 1 2 3 2 1 3 2 2 4 0 0 0 95 92 187
Gafsa et Tozeur 1906 | 13 10 23 52 45 97 215 146 361 55 34 89 61 50 111 8 15 23 7 9 16 0 2 2 2 11 13 413 322 735
Gafsa et Tozeur 1901 | 10 4 14 47 37 84 93 61 154 32 18 50 59 33 92 11 16 27 2 0 2 8 5 13 0 0 0 262 174 436
Grombalia 1906 | 268 166 434 46 56 102 90 42 132 38 28 66 94 95 189 16 13 29 15 6 21 19 6 25 5 28 33 691 340 1031
Grombalia 1901 | 177 108 285 61 40 101 40 26 66 26 28 54 77 65 142 17 22 39 13 9 22 3 5 8 0 0 0 414 303 717
Kairouan 1906 | 38 27 65 17 15 32 88 35 123 14 11 25 77 52 129 8 5 13 9 8 17 0 1 1 10 19 29 261 173 434
Kairouan 1901 | 27 21 48 29 20 49 24 13 37 10 5 15 57 39 96 11 20 31 11 9 20 1 3 4 0 0 0 170 130 300
Le Kef 1906 | 38 18 56 61 56 117 152 65 217 52 30 582 113 102 215 14 11 25 7 3 10 2 9 11 11 37 48 450 331 781
Le Kef 1901 | 24 17 41 39 37 76 50 42 92 0 0 0 59 61 120 8 14 22 9 7 16 4 15 19 0 0 0 193 193 386
Teboursouk 1906 | 65 38 103 31 37 68 21 15 36 44 43 87 43 59 102 0 0 0 20 5 25 3 0 3 4 3 7 231 200 431
Teboursouk 1901 | 42 13 55 13 6 19 20 17 37 3 3 6 14 12 26 4 10 14 0 0 0 2 1 3 0 0 0 98 62 160
Mactar 1906 | 10 9 19 0 0 0 5 4 9 0 0 0 29 14 43 0 0 0 0 0 0 0 0 0 0 2 2 46 29 75
Mactar 1901 | 5 0 5 6 4 10 47 14 61 0 0 0 22 13 35 2 0 2 1 0 1 0 0 0 0 0 0 83 31 114
Sfax 1906 | 84 69 153 248 252 500 99 71 170 42 25 67 406 352 758 18 8 26 36 29 65 5 3 8 38 16 54 976 825 1801
Sfax 1901 | 77 59 136 111 87 198 143 114 257 175 118 293 146 120 266 24 47 71 60 51 111 11 26 37 3 1 4 750 623 1373
Souk-el-Arba 1906 | 125 84 209 83 76 159 127 85 212 65 43 108 105 94 199 12 21 32 9 10 19 10 14 24 6 35 41 542 462 1004
Souk-el-Arba 1901 | 80 45 125 82 77 159 66 61 127 32 32 64 77 77 154 16 13 29 13 12 25 9 16 25 0 0 0 375 333 708
Tabarca 1906 | 55 47 102 62 55 117 108 108 216 19 8 27 122 106 228 2 5 7 5 3 8 13 13 26 69 49 118 455 394 849
Tabarca 1901 | 44 23 67 34 40 74 60 45 105 33 47 80 85 70 155 6 13 19 2 0 2 9 11 20 0 0 0 273 249 522
Sousse 1906 | 95 61 156 170 147 317 252 214 466 114 88 202 392 330 722 48 36 84 43 66 109 23 48 71 39 117 156 1176 1107 2283
Sousse 1901 | 56 38 94 113 109 222 188 179 367 70 55 125 222 190 412 46 96 142 95 122 217 32 51 83 0 0 0 822 840 1662
Thala 1906 | 11 4 15 6 9 15 26 5 31 0 0 0 39 29 68 3 2 5 0 0 0 1 1 2 0 0 0 86 50 136
Thala 1901 | 5 1 6 9 7 16 7 0 7 0 0 0 41 32 73 1 0 1 0 1 1 1 1 2 0 0 0 64 42 106
Tunis 1906 | 1184 834 2018 1744 1872 3616 1734 1492 3226 761 680 1441 2149 2175 4324 325 286 611 618 573 1191 275 483 758 787 1413 2200 9577 9808 19385
Tunis 1901 | 1124 577 1701 1160 1147 2307 1419 1329 2748 405 330 735 1141 999 2140 358 448 806 676 585 1261 236 311 547 187 361 548 6706 6087 12793
Territoires du Sud 1906 | 5 1 6 12 14 26 6 4 10 4 3 7 29 19 48 7 0 7 5 1 6 5 2 7 0 23 24 74 67 141
Territoires du Sud 1901 | 9 6 15 10 6 16 10 4 14 1 0 1 18 15 33 3 9 12 0 0 0 1 3 4 0 0 0 52 43 95
"""
T_G_ENSEMBLE = {
    1906: [2660, 1783, 4443, 2880, 2950, 5830, 3668, 2845, 6513, 1495, 1230, 2725, 4391, 4108, 8499,
           529, 467, 996, 871, 817, 1688, 572, 1060, 1632, 1089, 2054, 3143, 18155, 17314, 35469],
    1901: [2101, 1164, 3265, 2168, 1989, 4157, 3157, 2639, 5796, 918, 739, 1657, 2380, 2006, 4386,
           622, 930, 1552, 966, 886, 1852, 410, 568, 978, 195, 363, 558, 12917, 11284, 24201],
}
T_G_FIXES = []
# Flags set after cross-checking with the independent transcription of Tables VI
# and VII (extract_eur1906_t6_t7.py). Djerba 1901 police women was first read as
# 1; the image reads H 1, F 2, T 3 and the printed Djerba 1901 totals then add
# up. Beja 1906 agriculture men is printed 269, but the printed row total (730),
# column total (2.660) and Table VII all imply 319: kept as printed, flagged.
T_G_FLAGS = {
    ("Djerba", 1901, "police_force", "female"): "ocr_corrected",
    ("Béja et Medjez-el-Bab", 1906, "agriculture", "male"): "total_mismatch",
}


def table_g():
    t = "G"
    rows = []
    ens = {1906: [0] * 30, 1901: [0] * 30}
    for ln in T_G.strip().splitlines():
        head, vals = [s.strip() for s in ln.split("|")]
        circ, year = head.rsplit(" ", 1)
        year = int(year)
        v = [int(x) for x in vals.split()]
        assert len(v) == 30, (circ, year, len(v))
        for k in range(30):
            ens[year][k] += v[k]
        for gi, (g, gfr) in enumerate(G_GROUPS + [("total", "Totaux")]):
            m, f, tt = v[3 * gi:3 * gi + 3]
            ok = (m + f == tt)
            check(t, f"{circ} {year} {g} M+F=T", m + f, tt)
            if gi < 9:
                for sex, sex_fr, val in (("male", "Hommes", m), ("female", "Femmes", f)):
                    rows.append([CENSUS, t, 62 if gi < 4 else 63, 61, circ, year, g, gfr, sex,
                                 sex_fr, val,
                                 T_G_FLAGS.get((circ, year, g, sex), "" if ok else "total_mismatch")])
        for s in range(3):
            check(t, f"{circ} {year} totals col {s}", sum(v[3 * gi + s] for gi in range(9)), v[27 + s])
    for year in (1906, 1901):
        for k in range(30):
            check(t, f"Ensemble {year} col {k}", ens[year][k], T_G_ENSEMBLE[year][k])
    hdr = ["census", "table_id", "source_page", "gallica_view", "controle_civil", "census_year",
           "occupation_group", "occupation_group_fr", "sex", "sex_fr", "value", "flag"]
    return write("eur1906_tg_french_by_occupation_1901_1906", hdr, rows)


# --------------------------------------------------------------------------
# Small tables printed in the commentary. Each is written in long form with a
# `measure` column: "count" (persons) or a proportion ("pct_*", "per_1000_*").
GROUPS4 = [("all_european", "Ensemble des Européens"), ("french", "Français"),
           ("italian", "Italiens"), ("maltese", "Maltais")]
TEXT_HDR_BASE = ["census", "table_id", "source_page", "gallica_view"]


def write_text(name, page, view, dims, rows):
    """rows: list of (dim values..., measure, value, flag)."""
    out = [[CENSUS, f"text_{name}", page, view, *r] for r in rows]
    hdr = TEXT_HDR_BASE + dims + ["measure", "value", "flag"]
    return write(f"eur1906_text_{name}", hdr, out)


def eur_total(i):  # Table V totals by nationality index; 'all' = regency
    return TABLE_I_TOTAL[6] if i is None else TABLE_I_TOTAL[i]


def text_tables():
    t = "text"
    n = {}

    # p.36 (view 35): French population at each census since 1880.
    rows = [("1880", "count", 708, ""), ("1891", "count", 10030, ""), ("1896", "count", 16207, ""),
            ("1901", "count", 24201, ""), ("1906", "count", 34610, "")]
    check(t, "1891 French incl. 57 not in Table B", 10030, T_B_TOTAL[0] + 57)
    n["french_totals_1880_1906"] = write_text("french_totals_1880_1906", 36, 35, ["census_year"], rows)

    # p.40 (view 39): place of birth of the European population, 1906.
    bp = [("tunisia", "Tunisie", 45851, 355.34, 9239, 71.60, 36612, 283.74),
          ("algeria", "Algérie", 6096, 47.24, 5251, 40.70, 845, 6.54),
          ("france", "France", 18614, 144.25, 18439, 142.90, 175, 1.35),
          ("french_possessions", "Possessions françaises", 57, 0.44, 57, 0.44, 0, 0),
          ("abroad", "Etranger", 58255, 451.47, 1602, 12.41, 56653, 439.06),
          ("unknown", "Lieu inconnu", 22, 0.17, 22, 0.16, 0, 0)]
    rows = []
    for code, fr, a, ap, f, fp, e, ep in bp:
        check(t, f"birthplace {code} French+foreign", f + e, a)
        for grp, cnt, pct in (("all_european", a, ap), ("french", f, fp), ("foreign", e, ep)):
            rows.append((grp, code, fr, "count", cnt, ""))
            rows.append((grp, code, fr, "per_1000_europeans", pct, ""))
    for k, tot in ((2, 128895), (4, 34610), (6, 94285)):
        check(t, f"birthplace column {k} total", sum(r[k] for r in bp), tot)
    n["birthplace_1906"] = write_text("birthplace_1906", 40, 39,
                                      ["group", "birthplace", "birthplace_fr"], rows)

    # p.40: French born in Tunisia / Algeria / France, 1891-1906.
    fb = {1891: (1838, 18.4, 1487, 14.9, 6107, 61.2), 1896: (3339, 20.6, 2384, 14.6, 9768, 60.2),
          1901: (5314, 21.8, 3657, 15.8, 14036, 57.9), 1906: (9239, 26.6, 5251, 15.1, 18439, 53.2)}
    rows = []
    for y, v in fb.items():
        tot = T_B_TOTAL[YEARS.index(y)]
        for j, (code, fr) in enumerate((("tunisia", "En Tunisie"), ("algeria", "En Algérie"),
                                        ("france", "En France"))):
            cnt, pct = v[2 * j], v[2 * j + 1]
            check(t, f"French born {code} {y} pct", abs(100 * cnt / tot - pct) < 0.11, True)
            rows.append((y, code, fr, "count", cnt, ""))
            rows.append((y, code, fr, "pct_of_french", pct, ""))
    n["french_birthplace_1891_1906"] = write_text("french_birthplace_1891_1906", 40, 39,
                                                  ["census_year", "birthplace", "birthplace_fr"], rows)

    # p.49 (view 48): Europeans settled in Tunisia for < 5 years and 5-10 years.
    # Printed "28.455" French for 5-10 years; Table IV gives 8,455 (and the
    # printed 36 % = 8,455 / 23,174). Printed value kept and flagged.
    fr_ens, tot_ens = T4_ENSEMBLE[0], T4_ENSEMBLE[6]
    lt5_f, lt5_t = sum(fr_ens[1:6]), sum(tot_ens[1:6])
    b5_f, b5_t = sum(fr_ens[6:11]), sum(tot_ens[6:11])
    check(t, "settled <5y French vs Table IV", 12775, lt5_f)
    check(t, "settled <5y others vs Table IV", 26639, lt5_t - lt5_f)
    check(t, "settled 5-10y French vs Table IV", 28455, b5_f)
    check(t, "settled 5-10y others vs Table IV", 23174, b5_t - b5_f)
    rows = [("lt_5y", "depuis cinq ans", "french", "count", 12775, ""),
            ("lt_5y", "depuis cinq ans", "other_european", "count", 26639, ""),
            ("lt_5y", "depuis cinq ans", "french_per_100_other", "pct", 47, ""),
            ("5_10y", "entre cinq et dix ans", "french", "count", 28455, "total_mismatch"),
            ("5_10y", "entre cinq et dix ans", "other_european", "count", 23174, ""),
            ("5_10y", "entre cinq et dix ans", "french_per_100_other", "pct", 36, "")]
    n["recent_settlers"] = write_text("recent_settlers", 49, 48,
                                      ["residence_duration", "residence_duration_fr", "group"], rows)

    # p.49-50 (views 48-49): sex.
    sx = {"all_european": (67309, 52.2, 61586, 47.8, 52.2, 47.8),
          "french": (17938, 13.9, 16672, 12.9, 51.8, 48.2),
          "italian": (42569, 33.0, 38587, 29.9, 52.4, 47.6),
          "maltese": (5270, 14.1, 5060, 13.9, 51.2, 48.8)}
    t5 = {nat: grid(txt)[7] for (nat, _, _, _), txt in T5.items()}
    rows = []
    for grp, v in sx.items():
        if grp != "all_european":
            check(t, f"sex {grp} male vs Table V", v[0], sum(t5[grp][0:8:2]))
            check(t, f"sex {grp} female vs Table V", v[2], sum(t5[grp][1:8:2]))
        grp_tot = v[0] + v[2]
        for sex, cnt, p_eur, p_grp in (("male", v[0], v[1], v[4]), ("female", v[2], v[3], v[5])):
            ok = abs(100 * cnt / 128895 - p_eur) < 0.11
            check(t, f"sex {grp} {sex} pct of Europeans", ok, True)
            rows.append((grp, sex, "count", cnt, ""))
            rows.append((grp, sex, "pct_of_europeans", p_eur, "" if ok else "total_mismatch"))
            rows.append((grp, sex, "pct_of_group", p_grp, ""))
    # p.50 (view 49): share of boys/males under and over 10, and French male share over time.
    for grp, u10, o10 in (("all_european", 51.2, 52.2), ("french", 51.03, 52),
                          ("italian", 51.3, 52.8), ("maltese", 50.9, 50.5)):
        rows.append((grp, "male", "pct_male_age_lt_10", u10, ""))
        rows.append((grp, "male", "pct_male_age_10_plus", o10, ""))
    for y, v in ((1896, 54), (1901, 53), (1906, 51.8)):
        rows.append(("french", "male", f"pct_of_group_{y}", v, ""))
    n["sex"] = write_text("sex", 49, 48, ["group", "sex"], rows)

    # p.50-51 (views 49-50): age structure.
    ag_eur = {"all_european": [(30473, 23.6), (24032, 18.6), (24384, 18.9), (20550, 15.9),
                               (15356, 11.9), (8534, 6.6), (5566, 4.3)],
              "french": [(7411, 5.8), (5181, 4.0), (7182, 5.6), (6752, 5.2), (4427, 3.4),
                         (2251, 1.7), (1406, 1.1)],
              "italian": [(20084, 15.6), (16344, 12.7), (14810, 11.5), (11922, 9.2), (9377, 7.3),
                          (5233, 4.0), (3386, 2.6)],
              "maltese": [(2474, 1.9), (2114, 1.6), (1796, 1.4), (1350, 1.0), (1165, 0.9),
                          (812, 0.6), (619, 0.5)]}
    ag_grp = {"all_european": [23.6, 18.6, 18.9, 15.9, 11.9, 6.6, 4.3],
              "french": [21.7, 14.9, 20.7, 19.7, 12.4, 6.5, 4.1],
              "italian": [24.7, 20.1, 17.9, 14.6, 11.5, 6.4, 4.1],
              "maltese": [23.8, 20.4, 16.3, 13, 11.2, 7.8, 5.9]}
    t5rows = {nat: grid(txt)[:7] for (nat, _, _, _), txt in T5.items()}
    rows = []
    for grp, v in ag_eur.items():
        for i, (cnt, p) in enumerate(v):
            if grp == "all_european":
                exp = sum(t5rows[nat][i][8] for nat in t5rows)
            else:
                exp = t5rows[grp][i][8]
            check(t, f"age {grp} {AGE[i]} vs Table V", cnt, exp)
            rows.append((grp, AGE[i], AGE_FR[i], 1906, "count", cnt, ""))
            rows.append((grp, AGE[i], AGE_FR[i], 1906, "pct_of_europeans", p, ""))
            rows.append((grp, AGE[i], AGE_FR[i], 1906, "pct_of_group", ag_grp[grp][i], ""))
    for y, v in ((1901, [19.97, 14.52, 21.69, 21.33, 12.79, 6.29, 3.41]),
                 (1896, [19.43, 14.66, 21.61, 22.46, 12.46, 5.94, 3.44])):
        check(t, f"French age shares {y} sum to 100", round(sum(v), 2), 100.0)
        for i, p in enumerate(v):
            rows.append(("french", AGE[i], AGE_FR[i], y, "pct_of_group", p, ""))
    n["age"] = write_text("age", 50, 49, ["group", "age_group", "age_group_fr", "census_year"], rows)

    # p.52 (view 51): marital status. The Maltese TOTAL column is cut off in the
    # binding: those proportion cells are NA (illegible).
    cnt = {"all_european": [(39463, 32034), (26266, 25354), (1355, 3913), (225, 285)],
           "french": [(10377, 8031), (6945, 7235), (493, 1279), (123, 127)],
           "italian": [(24709, 20406), (17107, 16011), (678, 2050), (75, 120)],
           "maltese": [(3398, 2869), (1716, 1679), (134, 485), (22, 27)]}
    p_eur = {"all_european": [(30.6, 24.9, 55.5), (20.4, 19.7, 40.1), (1, 3, 4), (0.2, 0.2, 0.4)],
             "french": [(8, 6.2, 14.2), (5.4, 5.6, 11.0), (0.4, 1.0, 1.4), (0.1, 0.1, 0.2)],
             "italian": [(19.2, 15.8, 35), (13.3, 12.4, 25.7), (0.5, 1.6, 2.1), (0, 0.1, 0.1)],
             "maltese": [(2.6, 2.2, None), (1.3, 1.3, None), (0.1, 0.4, None), (0, 0, None)]}
    p_grp = {"all_european": [(30.6, 24.9, 55.5), (20.4, 19.7, 40.1), (1, 3, 4), (0.2, 0.2, 0.4)],
             "french": [(29.9, 23.1, 53.0), (19.9, 20.7, 40.6), (1.6, 4.2, 5.8), (0.3, 0.3, 0.6)],
             "italian": [(30.5, 25.1, 55.6), (21.2, 19.6, 40.8), (0.9, 2.5, 3.4), (0.1, 0.1, 0.2)],
             "maltese": [(32.8, 27.9, None), (16.8, 16.2, None), (1.3, 4.6, None), (0.2, 0.2, None)]}
    rows = []
    for grp in cnt:
        for m, (mar, mar_fr) in enumerate(MAR):
            mm, ff = cnt[grp][m]
            if grp == "all_european":
                check(t, f"marital {mar} M vs Table V", mm, T5_GRAND[2 * m])
                check(t, f"marital {mar} F vs Table V", ff, T5_GRAND[2 * m + 1])
            else:
                check(t, f"marital {grp} {mar} M vs Table V", mm, t5[grp][2 * m])
                check(t, f"marital {grp} {mar} F vs Table V", ff, t5[grp][2 * m + 1])
            for s, sex in enumerate(("male", "female")):
                rows.append((grp, mar, mar_fr, sex, "count", (mm, ff)[s], ""))
            for s, sex in enumerate(("male", "female", "total")):
                for meas, src in (("pct_of_europeans", p_eur), ("pct_of_group", p_grp)):
                    v = src[grp][m][s]
                    rows.append((grp, mar, mar_fr, sex, meas, "" if v is None else v,
                                 "illegible" if v is None else ""))
    n["marital_status"] = write_text("marital_status", 52, 51,
                                     ["group", "marital_status", "marital_status_fr", "sex"], rows)

    # p.53 (view 52): marital status of the French, 1896/1901/1906, and France.
    ms = {"1896": (54.4, 39.72, 4.98, 0.88), "1901": (53.77, 40.52, 5.02, 0.60),
          "1906": (53.0, 40.6, 5.8, 0.6), "France": (51.5, 40.5, 8.1, 0.15)}
    rows = []
    for y, v in ms.items():
        check(t, f"French marital shares {y} sum ~100", abs(sum(v) - 100) < 0.2, True)
        for m, (mar, mar_fr) in enumerate(MAR):
            rows.append((y, mar, mar_fr, "pct_of_french", v[m], ""))
    n["french_marital_status_1896_1906"] = write_text(
        "french_marital_status_1896_1906", 53, 52,
        ["census_year_or_reference", "marital_status", "marital_status_fr"], rows)

    # p.55 (view 54): French by birth vs by naturalisation, option or marriage.
    rows = []
    for y, b, bp_, nn, np_ in ((1906, 32453, 93.7, 2157, 6.2), (1901, 22215, 91.9, 1986, 8.0)):
        check(t, f"French origin {y} sum vs Table B", b + nn, T_B_TOTAL[YEARS.index(y)])
        rows += [(y, "by_birth", "all", "count", b, ""), (y, "by_birth", "all", "pct_of_french", bp_, ""),
                 (y, "naturalised", "all", "count", nn, ""),
                 (y, "naturalised", "all", "pct_of_french", np_, "")]
    cats = ["male", "female", "age_lt_20", "age_20_59", "age_60_plus", "single", "married",
            "widowed", "divorced"]
    birth_c = [17001, 15452, 11976, 19177, 1300, 17629, 12913, 1673, 238]
    birth_p = [52.3, 48.6, 36.9, 59.8, 4.0, 54.3, 39.7, 5.1, 0.7]
    nat_c = [937, 1220, 616, 1435, 106, 779, 1267, 99, 12]
    nat_p = [43.3, 57.6, 28.5, 66.6, 4.8, 36.1, 58.7, 4.5, 0.5]
    tf = {o: grid("\n".join(l.strip() for l in txt.strip().splitlines()[:7]))
          for (o, _), txt in T_F.items()}
    for orig, cc, pp in (("by_birth", birth_c, birth_p), ("naturalised", nat_c, nat_p)):
        g = tf[orig]
        exp = [sum(sum(r[0::2]) for r in g), sum(sum(r[1::2]) for r in g),
               sum(sum(r) for r in g[:2]), sum(sum(r) for r in g[2:6]), sum(g[6]),
               sum(r[0] + r[1] for r in g), sum(r[2] + r[3] for r in g),
               sum(r[4] + r[5] for r in g), sum(r[6] + r[7] for r in g)]
        tot = sum(cc[:2])
        for k, c in enumerate(cats):
            check(t, f"{orig} {c} vs Table F", cc[k], exp[k])
            ok = abs(100 * cc[k] / tot - pp[k]) < 0.11
            check(t, f"{orig} {c} pct", ok, True)
            rows.append((1906, orig, c, "count", cc[k], ""))
            rows.append((1906, orig, c, "pct_of_category", pp[k], "" if ok else "total_mismatch"))
    n["french_by_origin"] = write_text("french_by_origin", 55, 54,
                                       ["census_year", "nationality_origin", "category"], rows)

    # p.57 (view 56): persons exercising a profession vs. their families.
    pf = {"all_european": ((39691, 30.8, 7264, 5.6, 36.4), (22262, 17.2, 46106, 35.7, 53.2)),
          "french": ((11150, 32.5, 2315, 6.7, 39.2), (5344, 15.6, 11885, 34.6, 50.2)),
          "italian": ((24676, 30.5, 4296, 5.3, 35.8), (15171, 18.8, 29749, 36.9, 55.7)),
          "maltese": ((2933, 28.7, 469, 4.6, 33.3), (1801, 17.6, 3802, 37.2, 54.8))}
    pf_tot = {"all_european": (46955, 68768), "french": (13465, 17229), "italian": (28972, 44920),
              "maltese": (3402, 5603)}
    rows = []
    for grp, pair in pf.items():
        for k, (status, status_fr) in enumerate((("exercising_profession", "Exerçant une profession"),
                                                  ("family_of_preceding", "Famille des précédents"))):
            m, pm, f, pff, pt = pair[k]
            check(t, f"professions {grp} {status} M+F", m + f, pf_tot[grp][k])
            rows += [(grp, status, status_fr, "male", "count", m, ""),
                     (grp, status, status_fr, "female", "count", f, ""),
                     (grp, status, status_fr, "male", "pct_of_group", pm, ""),
                     (grp, status, status_fr, "female", "pct_of_group", pff, ""),
                     (grp, status, status_fr, "total", "pct_of_group", pt, "")]
    n["professional_status"] = write_text("professional_status", 57, 56,
                                          ["group", "status", "status_fr", "sex"], rows)

    # p.58 (view 57): occupational groups x (professionals / families) by nationality.
    occ = [("agriculture", "Agriculteurs", [(6320, 4.9), (1986, 5.6), (3964, 4.9), (212, 2.1)],
            [(11241, 8.7), (2457, 6.9), (8229, 10.2), (388, 3.8)], [17561, 4443, 12193, 600]),
           ("commerce", "Commerçants", [(9367, 7.3), (2620, 7.4), (4904, 6.0), (1343, 13.1)],
            [(13438, 10.4), (3210, 9.0), (7337, 9.1), (2399, 23.5)], [22805, 5830, 12241, 3742]),
           ("industry", "Industriels", [(23002, 17.8), (2982, 8.4), (18237, 22.6), (1507, 14.8)],
            [(32366, 25.1), (3531, 10.0), (26357, 32.6), (2261, 22.1)], [55368, 6513, 44594, 3768]),
           ("transport", "Entrepreneurs et agents de transport",
            [(2541, 2.0), (1190, 3.4), (1102, 1.3), (223, 2.1)],
            [(3965, 3.0), (1535, 4.3), (2005, 2.5), (397, 3.9)], [6506, 2725, 3107, 620]),
           ("public_administration", "Fonctionnaires",
            [(3697, 2.9), (3381, 9.5), (236, 0.3), (52, 0.5)],
            [(5616, 4.3), (5118, 14.4), (389, 0.5), (78, 0.7)], [9313, 8499, 625, 130]),
           ("police_force", "Représentants de la force publique",
            [(448, 0.3), (446, 1.3), (0, 0), (1, 0.0)],
            [(556, 0.4), (550, 1.5), (0, 0), (3, 0.03)], [1004, 996, 0, 4]),
           ("liberal_professions", "Représentants des professions libérales",
            [(1580, 1.2), (860, 2.4), (529, 0.7), (64, 0.6)],
            [(1586, 1.2), (828, 2.3), (603, 0.7), (77, 0.7)], [3166, 1688, 1132, 141]),
           ("independent_means", "Personnes vivant de leurs revenus",
            [(3007, 2.3), (1632, 4.6), (916, 1.1), (275, 2.7)], None, None),
           ("unclassified", "Population non classée",
            [(10165, 7.9), (3143, 8.9), (5747, 7.1), (928, 9.0)], None, None)]
    rows = []
    gtot = [0, 0, 0, 0]
    prof = [0, 0, 0, 0]
    for code, fr, pr, fam, sub in occ:
        for gi, (grp, _) in enumerate(GROUPS4):
            gtot[gi] += pr[gi][0] + (fam[gi][0] if fam else 0)
            if fam:
                prof[gi] += pr[gi][0]
                check(t, f"occupation {code} {grp} subtotal", pr[gi][0] + fam[gi][0], sub[gi])
            status = "exercising_profession" if fam else "all"
            rows.append((grp, code, fr, status, "count", pr[gi][0], ""))
            rows.append((grp, code, fr, status, "pct_of_group", pr[gi][1], ""))
            if fam:
                rows.append((grp, code, fr, "family_of_preceding", "count", fam[gi][0], ""))
                rows.append((grp, code, fr, "family_of_preceding", "pct_of_group", fam[gi][1], ""))
    for gi, (grp, _) in enumerate(GROUPS4):
        exp = 128895 if grp == "all_european" else TABLE_I_TOTAL[NAT.index(grp)]
        check(t, f"occupation {grp} grand total vs population", gtot[gi], exp)
        check(t, f"occupation {grp} professionals vs p.57", prof[gi], pf_tot[grp][0])
    n["occupation_groups"] = write_text("occupation_groups", 58, 57,
                                        ["group", "occupation_group", "occupation_group_fr", "status"],
                                        rows)

    # p.61 (view 60): French population by occupational category, % 1896-1906.
    cat = [("agriculture", "Agriculture"), ("commerce_industry", "Commerce, Industrie"),
           ("transport", "Transports"),
           ("public_admin_police_liberal", "Administrations publiques, Force publique, Profess. libérales"),
           ("independent_means", "Vivant de leurs revenus"),
           ("no_or_unknown_profession", "Sans profession, Profession inconnue")]
    pv = {1906: [12.5, 34.8, 7.7, 31.4, 4.6, 8.9], 1901: [13.49, 41.13, 6.85, 32.18, 4.04, 2.31],
          1896: [12.53, 40.50, 4.34, 36.15, 1.92, 4.42]}
    rows = []
    for y, v in pv.items():
        check(t, f"French occupation shares {y} sum ~100", abs(sum(v) - 100) < 0.2, True)
        for k, (code, fr) in enumerate(cat):
            rows.append((y, code, fr, "pct_of_french", v[k], ""))
    n["french_occupation_1896_1906"] = write_text("french_occupation_1896_1906", 61, 60,
                                                  ["census_year", "occupation_group",
                                                   "occupation_group_fr"], rows)
    return {f"eur1906_text_{k}": v for k, v in n.items()}


# --------------------------------------------------------------------------
# Notes files (one .md per CSV). Validation lines are filled in from CHECKS.
SRC = ("Dénombrement de la population européenne civile en Tunisie au 16 décembre 1906 "
       "(Tunis, 1907). Gallica ark bd6t53563851 (Bibliothèques de l'Université de Poitiers, "
       "NUM GIR-220).")
COMMON = """
Common columns: `census` (= eur1906), `table_id`, `source_page` (printed page),
`gallica_view` (Gallica view number), `value`, `flag` (empty, `ocr_corrected`,
`illegible`, `total_mismatch`, `not_applicable`, `derived_from_totals`; see SPEC.md).
Printed "»" is stored as 0. Printed subtotal and total rows are not stored; they
were used for validation.

Method: Gallica's OCR drops many cells on these pages, so every value was
transcribed from the page images (data-raw/bnf_gallica/pages/bd6t53563851/) and
checked against the printed totals by extract_eur1906_t4_t8_analysis.py.
"""
NOTES = {
 "eur1906_t4_residence_duration": ("IV", "Répartition d'après le temps de séjour en Tunisie, par nationalités et circonscriptions administratives",
   "Distribution by length of residence in Tunisia, by nationality and administrative district",
   "pp.18-21, views 22-25",
   """Columns: `controle_civil` (19 circonscriptions as printed), `nationality`, `residence_duration`
(12 classes: passing_through = "de passage en Tunisie", lt_1y, 1_2y ... 9_10y, gt_10y). Counts of persons.

Footnote (1): people temporarily away from their locality but domiciled in Tunisia are counted
as inhabitants of that locality; "de passage" covers only persons whose usual residence is outside Tunisia.

On pp.18 and 20 (Béja, Medjez-el-Bab, Bizerte, Gabès, Djerba, Téboursouk, Mactar, Sfax,
Souk-el-Arba, Tabarca) the last column ("de plus de 10 ans") is lost in the binding of the
scan. Those 60 cells are derived as Table I nationality total minus the sum of the 11 visible
columns (flag `derived_from_totals`). The derived values, summed with the printed pp.19/21
values, reproduce the printed regency totals ("Ensemble du territoire") for every nationality
and duration class, which validates them."""),
 "eur1906_t5_sex_age_marital": ("V", "Répartition d'après le sexe, l'âge et l'état civil",
   "Distribution by sex, age and marital status", "pp.22-23, views 26-27",
   """Columns: `nationality`, `age_group` (7 classes, lt_10 ... 60_plus), `marital_status`
(single, married, widowed, divorced), `sex`. Counts of persons. Nationality totals equal Table I."""),
 "eur1906_t8_instruction": ("VIII", "Degré d'instruction", "Literacy and knowledge of French",
   "p.34, view 33",
   """Columns: `nationality`, `indicator` (reads_only = "Sachant lire seulement",
reads_and_writes = "Sachant lire et écrire", speaks_french = "Parlant français"). Counts of persons.
Footnote (1): the question "speaks French" was not asked of the French, so that cell is NA
(flag `not_applicable`), not zero."""),
 "eur1906_ta_nationality_shares_density": ("A", "Proportion pour cent des Européens de chaque nationalité et densité de la population européenne par circonscriptions",
   "Share of each nationality in the European population, and European population density, by district",
   "p.35, view 34",
   """Columns: `controle_civil`, `indicator`: pct_french, pct_italian, pct_maltese, pct_other_european
(percent of the district's Europeans, numeric with one decimal), area_myriametres2 (area in
myriamètres carrés = 100 km2), europeans_per_myriametre2 (density). Gafsa, Tozeur and Territoires
du Sud have no area ("»"): NA, flag `not_applicable`. The printed "Ensemble du territoire" row is
kept (`controle_civil` = "Ensemble du territoire (printed)") because it is not a simple sum.
Footnote (1) to the total area/density: computed without the circonscriptions whose area is not given.

Validation: every percentage and density was recomputed from Table I. Values that differ from
the recomputation by 0.1 or more are flagged `total_mismatch` (printed values kept; re-read on a
2x zoom of the image, the print is as transcribed)."""),
 "eur1906_tb_french_population_1891_1906": ("B", "Population française civile par circonscriptions administratives. Résultats comparés des recensements de 1891, 1896, 1901 et 1906",
   "French civilian population by district, censuses of 1891, 1896, 1901 and 1906", "p.37, view 36",
   """Columns: `controle_civil`, `census_year`, value = persons. Districts follow the 1906
boundaries (footnote 1: figures regrouped by current territorial divisions). Footnote (2): add
57 French (transient and prison population) counted in 1891 but not included here.
The printed differences (1891-96, 1896-1901, 1901-06, 1891-1906) were used as checks."""),
 "eur1906_tc_french_growth_coefficients": ("C", "Population française civile. Coefficients d'accroissement par circonscriptions administratives",
   "French civilian population: growth coefficients by district", "p.39, view 38",
   """Columns: `controle_civil`, `base_year`, `census_year`, value = population in census_year
divided by population in base_year (numeric, two decimals; base year = 1). Pairs printed:
1891 to 1896/1901/1906, 1896 to 1901, 1901 to 1906. Each coefficient was recomputed from
Table B; those off by more than 0.01 are flagged `total_mismatch` (printed values kept)."""),
 "eur1906_td_french_population_by_locality_1891_1901": ("D", "Répartition de la population française civile par localités. Résultats comparés des recensements de 1891, 1896 et 1901",
   "French civilian population by locality, censuses of 1891, 1896 and 1901", "pp.41-45, views 40-44",
   """Columns: `controle_civil` (the contrôle civil or annexe heading as printed), `locality`
(as printed; city quarters written "Ville de Sfax, quartier : X"), `census_year`, value = persons.
The table prints no subtotals. "Maxula-Radès et Megrine" share one bracketed value in 1891
and 1896, and are separate in 1901. The 1891 Béja row "Djebel-ben-Drahar, ... et Sidi-Ahmed"
groups eight places.

The commentary (p.38) warns that the same place was often recorded under different names
at successive censuses, so localities are not strictly comparable over time.

Validation: unit sums were compared with Table B. They match for 14 of 19 units. For
Bizerte, Djerba, Teboursouk, Thala and Tunis, and so for the regency total, they do not:
Table D lists only named localities, while Table B regroups the population by 1906
boundaries. The source gives no reconciliation, and no value was changed."""),
 "eur1906_te_french_by_birthplace_1891_1906": ("E", "Répartition de la population française civile d'après le lieu de naissance. Résultats comparés des recensements de 1891, 1896, 1901 et 1906",
   "French civilian population by place of birth, censuses of 1891-1906", "pp.46-48, views 45-47",
   """Columns: `birthplace_fr` (Tunisia, the three Algerian départements, each French
département, colonies, abroad, unknown; as printed), `census_year`, value = persons.
Footnote (1): colonies and possessions other than Algeria and Tunisia.

Validation: the printed "à reporter" running totals were checked page by page. p.48 matches
exactly. On pp.46-47 the printed cells do not add up to the printed totals. The commentary
(pp.44-45) confirms three printing errors, all flagged `total_mismatch` with the printed
values kept: Bouches-du-Rhône 1906 printed 822 (commentary 922); Rhône 1901 printed 478
(commentary's +137 since 1901 implies 498); Loiret 1906 printed 29 (the page total implies
79). Smaller residual differences (2-10 persons) remain on pp.46-47 after re-reading the
zoomed images. Allier 1891: the first digit is broken in the scan and was read as 34
(`ocr_corrected`)."""),
 "eur1906_tf_french_by_origin_sex_age_marital": ("F", "Répartition de la population française d'après le sexe, l'âge et l'état civil en distinguant les Français de naissance et les Français par naturalisation, option ou mariage",
   "French population by sex, age and marital status, French by birth vs. by naturalisation, option or marriage",
   "p.54, view 53",
   """Columns: `nationality_origin` (by_birth, naturalised), `age_group`, `marital_status`, `sex`.
Counts of persons. The two blocks add up exactly to the French block of Table V."""),
 "eur1906_tg_french_by_occupation_1901_1906": ("G", "Répartition d'après la profession et le sexe, par circonscriptions administratives. Résultats comparés des recensements de 1901 et 1906",
   "French population by occupational group and sex, by district, censuses of 1901 and 1906",
   "pp.62-63, view 61",
   """Columns: `controle_civil` (as printed; Béja and Medjez-el-Bab, and Gafsa and Tozeur, are
combined), `census_year`, `occupation_group` (agriculture, commerce, industry, transport,
public_administration, police_force, liberal_professions, independent_means, unclassified),
`sex`. Persons, counting both those exercising the profession and their families (N.B. printed
on the table). Printed group totals and the "Totaux" column were used for validation only.

Validation: each M+F against its printed total, each row of totals against the sum of the
groups, and the "Ensemble du territoire" rows against the column sums. The print itself has
inconsistencies (re-read on the image): Le Kef 1906 transport printed 52 + 30 = "582" (82,
which the regency total confirms); Souk-el-Arba 1906 police force 12 + 21 = 32; Territoires du
Sud 1906 unclassified 0 + 23 = 24. Cells in those groups are flagged `total_mismatch`. Some
printed row totals also differ from the sum of their groups (Béja et Medjez-el-Bab 1906 men,
Grombalia 1906 men/women, Djerba 1901 women, Mactar 1906 men), as does the printed regency
total. The commentary (p.60) warns that the 1901 and 1906 categories are not fully comparable."""),
}
TEXT_NOTES = {
 "french_totals_1880_1906": ("p.36, view 35", "French population at each census since the occupation: 708 at 31 December 1880 (an estimate made in 1898 from the registers of the French consulate in Tunis), then 1891-1906. The 1891 figure (10,030) includes the 57 transient and prison population left out of Table B."),
 "birthplace_1906": ("p.40, view 39", "Place of birth of the European population in 1906 (summary of Table III): `group` = all_european, french, foreign; `measure` = count or per_1000_europeans (footnote 2: proportion per 1,000 Europeans). The French count for Tunisia is printed '92.39', which is 9,239."),
 "french_birthplace_1891_1906": ("p.40, view 39", "French born in Tunisia, in Algeria and in France, 1891-1906: counts and percent of the French population. The 1901 percentages for Tunisia and Algeria do not match a recomputation on Table B's total (24,201); printed values are kept."),
 "recent_settlers": ("p.49, view 48", "Europeans settled in Tunisia for less than five years and for five to ten years: French, other Europeans, and French per 100 other Europeans ('Proportion'). The 5-10 year French count is printed 28.455. Table IV gives 8,455, and the printed 36 % equals 8,455 / 23,174. The printed value is kept, flagged `total_mismatch`."),
 "sex": ("pp.49-50, views 48-49", "Sex distribution: counts, percent of all Europeans (`pct_of_europeans`) and percent within each group (`pct_of_group`), for all Europeans, French, Italians and Maltese. Also from the prose: share of males among children under 10 and among people aged 10 and over (`pct_male_age_lt_10`, `pct_male_age_10_plus`), and the male share of the French population in 1896, 1901 and 1906. Maltese percentages of all Europeans are printed 14.1 / 13.9, where the counts imply 4.1 / 3.9 (flagged `total_mismatch`)."),
 "age": ("pp.50-51, views 49-50", "Age structure: counts and percent of all Europeans (p.50); percent within each nationality (p.51); and percent of the French population by age in 1901 and 1896. The bracketed group percentages printed beside the age classes (<20, 20-59, 60+) are not stored. Counts match Table V."),
 "marital_status": ("p.52, view 51", "Marital status by sex: counts, percent of all Europeans, and percent within each nationality. The right edge of the Maltese TOTAL column is cut off in the binding: those 8 proportion cells are NA (`illegible`). Counts match Table V."),
 "french_marital_status_1896_1906": ("p.53, view 52", "Marital status of the French population in 1896, 1901 and 1906, and of the population of metropolitan France (column 'France'), in percent."),
 "french_by_origin": ("p.55, view 54", "French by birth vs. French by naturalisation, option or marriage: counts and shares in 1901 and 1906. Also, for 1906, counts and percentages by sex, broad age group and marital status. The counts match Table F. Some printed percentages differ from a recomputation by more than 0.1 (flagged `total_mismatch`)."),
 "professional_status": ("p.57, view 56", "Persons exercising a profession themselves vs. their dependants ('famille des précédents': no profession, or domestic servants), by sex. Counts, and percent of each group's population (footnote 1). Excludes the two last occupational categories of Table VI. The printed European total for dependants (68,768) is 400 more than male + female (68,368)."),
 "occupation_groups": ("p.58, view 57", "Occupational groups by nationality: persons exercising the profession and their families, counts and percent of each group's population (footnote 1). 'Personnes vivant de leurs revenus' and 'Population non classée' are single lines. Printed group subtotals were checked (all pass). The grand totals are larger than the Table I populations for the French and smaller for the Italians and Maltese, because servants and dependants were attached to the head of household's nationality (commentary p.60)."),
 "french_occupation_1896_1906": ("p.61, view 60", "Percent of the French population in each occupational category in 1896, 1901 and 1906. Footnote (1) on the 1906 agriculture value is cut off at the bottom of the page."),
}


def write_notes():
    by_table = {k: v for k, v in CHECKS.items()}
    for name, (tid, fr, en, where, body) in NOTES.items():
        c = by_table.get(tid, [0, 0, []])
        val = f"Validation: {c[1]} of {c[0]} automated checks pass."
        if c[2]:
            val += " Failing checks (all re-read on the image; printed values kept):\n" + "\n".join(
                f"- {b}" for b in c[2])
        (OUT / f"{name}.md").write_text(
            f"# Table {tid}: {fr}\n\n*{en}*\n\nSource: {SRC} {where}.\n\n{body}\n{COMMON}\n{val}\n",
            encoding="utf-8")
    c = by_table.get("text", [0, 0, []])
    for name, (where, body) in TEXT_NOTES.items():
        (OUT / f"eur1906_text_{name}.md").write_text(
            f"# Text table: {name.replace('_', ' ')}\n\nSource: {SRC} {where}.\n\n"
            f"Small table printed in the commentary. Columns: the dimension columns, `measure` "
            f"(count, or a proportion whose base is named in the column value), `value`, `flag`.\n\n"
            f"{body}\n{COMMON}\nValidation: the text tables share one battery of {c[0]} checks "
            f"(against Tables IV, V, F, B and the printed subtotals); {c[1]} pass. Failing checks "
            f"are listed in the extraction script output and flagged in the data where they "
            f"concern a stored value.\n", encoding="utf-8")


def main():
    n = {"eur1906_t4_residence_duration": table_iv(),
         "eur1906_t5_sex_age_marital": table_v(),
         "eur1906_t8_instruction": table_viii(),
         "eur1906_ta_nationality_shares_density": table_a(),
         "eur1906_tb_french_population_1891_1906": table_b(),
         "eur1906_tc_french_growth_coefficients": table_c(),
         "eur1906_td_french_population_by_locality_1891_1901": table_d(),
         "eur1906_te_french_by_birthplace_1891_1906": table_e(),
         "eur1906_tf_french_by_origin_sex_age_marital": table_f(),
         "eur1906_tg_french_by_occupation_1901_1906": table_g()}
    n.update(text_tables())
    write_notes()
    for d in T_D_UNIT_DIFFS:
        print("  Table D unit vs B:", d)
    for k, v in n.items():
        print(f"{k}: {v} rows")
    for t, (c, p, bad) in CHECKS.items():
        print(f"Table {t}: {p}/{c} checks passed")
        for b in bad:
            print("   ", b)


if __name__ == "__main__":
    main()
