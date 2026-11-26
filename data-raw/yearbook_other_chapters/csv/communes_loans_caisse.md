# Finances municipales : c) Emprunts contractés à la Caisse des Prêts Communaux

*Municipal loans from the Caisse des Prêts Communaux: one block per commune, one line per loan, with terms, annuities due and paid, arrears and capital amortised / outstanding at the end of the year.*

Source: *Statistique générale de la Tunisie*, chapter *Communes*, editions sgt1922, sgt1923, sgt1924, sgt1925. Source gallica.bnf.fr / Ministère des Affaires étrangères (NoC-CR).

Pages and views of the stored values: sgt1922 (`bpt6k9105649x`): p. 30, f54, p. 31, f55, p. 32, f56, p. 33, f57; sgt1923 (`bpt6k9105649x`): p. 30, f532, p. 31, f533, p. 32, f534, p. 33, f535; sgt1924 (`bpt6k9105649x`): p. 30, f1020, p. 31, f1021, p. 32, f1022, p. 33, f1023; sgt1925 (`bpt6k9105650k`): p. 30, f54, p. 31, f55, p. 32, f56, p. 33, f57.

Rebuild: `python3 data-raw/yearbook_other_chapters/extract_communes.py build` (transcriptions `../transcribed/communes_loans_<edition>.txt, section `@caisse``).

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
- `value`: francs with centimes, except `duration_years` (years) and `interest_rate_pct` (percent: "3 75" = 3.75, "7 »" = 7)
- `flag`: empty, `not_applicable` (text printed instead of a number: value NA; the text is listed below), `illegible` (value NA; for money with hidden centimes the franc part is listed below)

Two-page spreads (left page: columns 1–6, date to annuity; right page: columns 7–13). `gallica_view` is the view of the page the cell is printed on. Editions transcribed: **sgt1922, sgt1923, sgt1924 and sgt1925 only**. sgt1925: the first spread (views 52–53: Tunis, Béja, Bizerte, Ferryville) is not transcribed because view 52 is a black image in the Gallica scan; only views 54–57 are stored for that edition. sgt1926–sgt1930 (three to four spreads each, e.g. sgt1930 views 594–601) are not done.

**Image versus OCR.** Every cell was read on native-resolution crops of the spreads (left and right page stitched at the same height); the OCR was used to find the column positions and lines. In sgt1922 the annuity column runs into the binding: the centimes are hidden, so those cells are NA, `illegible` (franc parts listed below); sgt1924 has the same for the first two Tunis loans and the three Sfax/Sousse 3,75 % loans and Souk-el-Khemis total.

Checks: for every loan line and total line, total payments = payments in the year + earlier payments; arrears = annuities due − total payments; capital remaining = nominal capital − capital amortised; and every commune *Totaux* line against its loans. Cross-edition: earlier payments of year N = total payments of year N−1. Every failure was re-read on a native-resolution crop and the printed value is kept; most are visible slips in the print (e.g. sgt1922 and sgt1923 print Tunis's total capital 5.600.000 for four loans summing to 9.600.000; sgt1923 and sgt1924 repeat the 1923 payment 137.221,20 of the Sfax 1909 9-million loan while the total includes 418.708,10; Souk-el-Arba's nominal capital is printed » in sgt1922–23).

Durations are as printed ("30 ans" → 30). The *Capital nominal* of Souk-el-Arba 1921 is printed » in sgt1922 and sgt1923 (stored 0.00).

## Validation

Rows: 1140.
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
Flagged cells: illegible: 29.
  - sgt1922 Tunis / 28 août 1903 annuity: illegible (franc part 81656)
  - sgt1922 Tunis / 1er octobre 1907 annuity: illegible (franc part 11912)
  - sgt1922 Tunis / 30 juin 1908 annuity: illegible (franc part 184726)
  - sgt1922 Tunis / 31 décembre 1921 annuity: illegible (franc part 140000)
  - sgt1922 Béja / 3 avril 1907 annuity: illegible (franc part 9897)
  - sgt1922 Bizerte / 20 février 1904 annuity: illegible (franc part 44301)
  - sgt1922 Ferryville / 16 mars 1911 annuity: illegible (franc part 3333)
  - sgt1922 Hammam-Lif / 1er décembre 1908 annuity: illegible (franc part 1132)
  - sgt1922 Kairouan / 19 octobre 1912 annuity: illegible (franc part 11945)
  - sgt1922 Mahdia / 27 mars 1909 annuity: illegible (franc part 6608)
  - sgt1922 Monastir / 3 mars 1908 annuity: illegible (franc part 1648)
  - sgt1922 Nabeul / 5 avril 1910 annuity: illegible (franc part 1385)
  - sgt1922 Sfax / 1er août 1904 et 22 juin 1909 annuity: illegible (franc part 9019)
  - sgt1922 Sfax / 22 juin 1909 annuity: illegible (franc part 4551)
  - sgt1922 Sfax / 22 juin 1909 annuity: illegible (franc part 418708)
  - sgt1922 Souk-el-Arba / 1er mars 1921 annuity: illegible (franc part 13469)
  - sgt1922 Sousse / 21 février 1906 et 1er mars 1911 annuity: illegible (franc part 13462)
  - sgt1922 Sousse / 2 mars 1908 et 1er mars 1911 annuity: illegible (franc part 13170)
  - sgt1922 Sousse / 1er mars 1911 annuity: illegible (franc part 14286)
  - sgt1922 Tébourba / 25 avril 1907 annuity: illegible (franc part 1321)
  - sgt1924 Tunis / 28 août 1903 annuity: illegible (franc part 81656)
  - sgt1924 Tunis / 1er octobre 1907 annuity: illegible (franc part 11912)
  - sgt1924 Nabeul / 5 avril 1910 annuity: illegible (franc part 1385)
  - sgt1924 Sfax / 1er août 1904 et 22 juin 1909 annuity: illegible (franc part 9019)
  - sgt1924 Sfax / 22 juin 1909 annuity: illegible (franc part 4551)
  - sgt1924 Sfax / 22 juin 1909 annuity: illegible (franc part 418708)
  - sgt1924 Sousse / 21 février 1906 et 1er mars 1911 annuity: illegible (franc part 13462)
  - sgt1924 Sousse / 2 mars 1908 et 1er mars 1911 annuity: illegible (franc part 13170)
  - sgt1924 Sousse / 1er mars 1911 annuity: illegible (franc part 14286)
