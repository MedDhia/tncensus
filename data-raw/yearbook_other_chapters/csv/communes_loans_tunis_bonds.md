# Finances municipales : b) Emprunts communaux (Commune de Tunis)

*Bond loans of the city of Tunis (1891 and 1897): coupons and bonds due, paid in the year and earlier, lapsed, and outstanding at the close of the year.*

Source: *Statistique générale de la Tunisie*, chapter *Communes*, editions sgt1922, sgt1923, sgt1924. Source gallica.bnf.fr / Ministère des Affaires étrangères (NoC-CR).

Pages and views of the stored values: sgt1922 (`bpt6k9105649x`): p. 30, f54, p. 31, f55; sgt1923 (`bpt6k9105649x`): p. 30, f532, p. 31, f533; sgt1924 (`bpt6k9105649x`): p. 30, f1020, p. 31, f1021.

Rebuild: `python3 data-raw/yearbook_other_chapters/extract_communes.py build` (transcriptions `../transcribed/communes_loans_<edition>.txt, section `@tunis_bonds``).

Printed once per edition (SPEC_ADDENDUM rule 5): `year` is the year the edition reports on; no year is printed twice, so there is no overlap to compare.

## Columns

- `census`: edition the value is taken from (`sgt1922` … `sgt1939`)
- `table_id`: transcription section
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number
- `gallica_view`: Gallica view (fNNNN)
- `year`: year of the edition's figures (exercice / calendar year)
- `commune`: commune as printed (for loans: the name in the block heading, e.g. `Tunis` from *Commune de Tunis*; `le Kef` from *Commune du Kef*)
- `commune_heading_fr`: block heading exactly as printed
- `loan_fr`: date of the loan as printed (identifies the loan within the commune)
- `measure`: English code of the printed column
- `measure_fr`: column heading as printed (French)
- `value`: francs with centimes, except `duration_years` and `interest_rate_pct` ("3 1/2" = 3.5)
- `flag`: empty, `not_applicable` (text printed instead of a number: value NA; the text is listed below), `illegible` (value NA; for money with hidden centimes the franc part is listed below)

Top of the first loan spread (columns 1–7 on the left page, 8–17 on the right). Editions transcribed: sgt1922, sgt1923, sgt1924 (sgt1925: left page view 52 is a black image, not transcribed; sgt1926–sgt1930 not done). All cells read on native-resolution crops. In sgt1922 the column *capitaux (obligations sorties aux tirages)* runs into the binding: centimes hidden, cells NA `illegible` with the franc part below. Checks: total = year + earlier payments (interest and capital), outstanding = due − paid − lapsed, the *Totaux* line, and earlier payments(N) = total payments(N−1) across editions.

## Validation

Rows: 96.
Checks (loans): 597; failed: 35.
  - sgt1922 p.30 Commune de Tunis / Totaux: remaining printed 9052156.44, cap_nom - amortised = 5052156.44
  - sgt1922 p.30 Commune de Béja / 3 avril 1907: arrears printed 0, due - paid_total = 200.00
  - sgt1922 p.30 Commune de Béja / 3 avril 1907: remaining printed 82902.52, cap_nom - amortised = 82909.52
  - sgt1922 p.30 Commune de Ferryville / 16 mars 1911: remaining printed 71876.17, cap_nom - amortised = 71876.47
  - sgt1922 p.30 Commune de Tunis cap_net: cells give 9600000, printed total 5600000 (difference -4000000)
  - sgt1922 p.30 Commune de Tunis cap_nom: cells give 9984600, printed total 5984600 (difference -4000000)
  - sgt1922 p.32 Commune de Kairouan / 19 octobre 1912: paid_total printed 120091.22, paid_year + paid_before = 120090.68
  - sgt1922 p.32 Commune de Souk-el-Arba / 1er mars 1921: remaining printed 165344.52, cap_nom - amortised = -2655.48
  - sgt1923 p.30 Commune de Béja / 3 avril 1907: paid_total printed 162596.98, paid_year + paid_before = 162566.98
  - sgt1923 p.30 Commune de Tunis cap_net: cells give 9600000, printed total 5600000 (difference -4000000)
  - sgt1923 p.32 Commune de Nabeul / 5 avril 1910: remaining printed 2653.18, cap_nom - amortised = 2653.08
  - sgt1923 p.32 Commune de Sfax / 1er août 1904 et 22 juin 1909: remaining printed 201706.86, cap_nom - amortised = 201706.36
  - sgt1923 p.32 Commune de Souk-el-Arba / 1er mars 1921: remaining printed 163415.67, cap_nom - amortised = -4584.33
  - sgt1923 p.32 Commune de Sfax remaining: cells give 9667532.18, printed total 9667531.68 (difference -0.50)
  - sgt1924 p.32 Commune de Sfax / 1er août 1904 et 22 juin 1909: paid_total printed 202569.84, paid_year + paid_before = 292569.84
  - sgt1924 p.32 Commune de Sfax / 1er août 1904 et 22 juin 1909: arrears printed 0, due - paid_total = 90000.00
  - sgt1924 p.32 Commune de Sfax / 22 juin 1909: paid_total printed 4640519.36, paid_year + paid_before = 4359032.46
  - sgt1924 p.32 Commune de Sfax / 22 juin 1909: remaining printed 9272276.27, cap_nom - amortised = 9273276.27
  - sgt1924 p.32 Commune de Sfax / Totaux: paid_total printed 5001458.22, paid_year + paid_before = 4719971.32
  - sgt1924 p.32 Commune de Sfax paid_total: cells give 4911458.22, printed total 5001458.22 (difference 90000.00)
  - sgt1924 p.32 Commune de Sfax amortised: cells give 507504.60, printed total 508504.60 (difference 1000.00)
  - sgt1925 p.30 Commune de Monastir / Totaux: remaining printed 32814.27, cap_nom - amortised = 32014.27
  - sgt1925 p.30 Commune de Sfax / 22 juin 1909: remaining printed 9179907.72, cap_nom - amortised = 9229907.72
  - sgt1925 p.30 Commune de Monastir cap_nom: cells give 48800, printed total 48000 (difference -800)
  - sgt1925 p.30 Commune de Sfax annuity: cells give 597419.94, printed total 597410.94 (difference -9.00)
  - sgt1925 p.30 Commune de Sfax amortised: cells give 582546.14, printed total 632546.14 (difference 50000.00)
  - sgt1925 p.32 Commune de Sousse / 21 février 1906 et 1er mars 1911: remaining printed 272483.32, cap_nom - amortised = 272483.42
  - sgt1925 p.32 Commune de La Marsa / 16 avril 1924: remaining printed 200000, cap_nom - amortised = 300000
  - sgt1925 p.32 Commune de La Marsa / Totaux: paid_total printed 30093.89, paid_year + paid_before = 30693.89
  - sgt1925 p.32 Commune de La Marsa / Totaux: arrears printed 0, due - paid_total = 600.00
  - sgt1925 p.32 Commune de Carthage / 5 juin 1924: remaining printed 123928.53, cap_nom - amortised = 123028.53
  - sgt1925 p.32 Commune de Mateur / 6 juin 1923: arrears printed 0, due - paid_total = -4550.00
  - sgt1925 p.32 Commune de Sousse remaining: cells give 1328203.57, printed total 1328203.67 (difference 0.10)
  - sgt1925 p.32 Commune de La Marsa paid_total: cells give 30693.89, printed total 30093.89 (difference -600.00)
  - sgt1925 p.32 Commune de La Marsa remaining: cells give 348714.23, printed total 448714.23 (difference 100000.00)
Cross-edition checks (paid before in year N = paid total in year N-1): 62; differences: 5.
  - Béja 3 avril 1907: paid_before 1923 (sgt1923) = 152669.04, paid_total 1922 (sgt1922) = 152699.04
  - Béja 3 avril 1907: paid_before 1924 (sgt1924) = 162956.98, paid_total 1923 (sgt1923) = 162596.98
  - Sfax 22 juin 1909: paid_before 1924 (sgt1924) = 4221811.26, paid_total 1923 (sgt1923) = 3940324.36
  - Sfax 1er août 1904 et 22 juin 1909: paid_before 1925 (sgt1925) = 292569.84, paid_total 1924 (sgt1924) = 202569.84
  - La Marsa 5 avril 1924: paid_before 1925 (sgt1925) = 3300.00, paid_total 1924 (sgt1924) = 9930.28
Flagged cells: illegible: 2.
  - sgt1922 Tunis / 17 février 1891 capital_due: illegible (franc part 1505982)
  - sgt1922 Tunis / 31 janvier 1897 capital_due: illegible (franc part 583851)
