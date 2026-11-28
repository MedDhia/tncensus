# Finances municipales : b) Emprunts communaux (Commune de Tunis)

*Bond loans of the city of Tunis (1891 and 1897): coupons and bonds due, paid in the year and earlier, lapsed, and outstanding at the close of the year.*

Source: *Statistique générale de la Tunisie*, chapter *Communes*, editions sgt1922, sgt1923, sgt1924, sgt1925, sgt1926, sgt1927, sgt1929, sgt1930. Source gallica.bnf.fr / Ministère des Affaires étrangères (NoC-CR).

Pages and views of the stored values: sgt1922 (`bpt6k9105649x`): p. 30, f54, p. 31, f55; sgt1923 (`bpt6k9105649x`): p. 30, f532, p. 31, f533; sgt1924 (`bpt6k9105649x`): p. 30, f1020, p. 31, f1021; sgt1925 (`bpt6k9105650k`): p. 28, f52, p. 29, f53; sgt1926 (`bpt6k9105650k`): p. 36, f600, p. 37, f601; sgt1927 (`bpt6k91056510`): p. 36, f64, p. 37, f65; sgt1929 (`bpt6k9105652d`): p. 36, f64, p. 37, f65; sgt1930 (`bpt6k9105652d`): p. 36, f594, p. 37, f595.

Rebuild: `python3 data-raw/yearbook_other_chapters/extract_communes.py build` (transcriptions `../transcribed/communes_loans_<edition>.txt, section `@tunis_bonds``).

Printed once per edition (SPEC_ADDENDUM rule 5): `year` is the year of the figures. The one year printed twice, 1928 (sgt1928, reprinted unchanged in sgt1929), is stored from the later edition (sgt1929) and every cell of the sgt1928 printing is compared (rule 4; result under Validation).

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
- `flag`: empty, `not_applicable` (text printed instead of a number: value NA; the text is listed below), `illegible` (value NA; for money with hidden centimes the franc part is listed below), `reprint_corrected` (sgt1925 view 52, black image: value taken from sgt1924 = sgt1926), `derived_from_totals` (sgt1925 bond sums due, solved from the right page)

Top of the first loan spread (columns 1–7 on the left page, 8–17 on the right). Editions transcribed: sgt1922–sgt1930; `year` as in `communes_loans_caisse.md` (sgt1929 reprints the 1928 table, sgt1930 gives 1929). All cells read on native-resolution crops. In sgt1922 the column *capitaux (obligations sorties aux tirages)* runs into the binding: centimes hidden, cells NA `illegible` with the franc part below. Checks: total = year + earlier payments (interest and capital), outstanding = due − paid − lapsed, the *Totaux* line, and earlier payments(N) = total payments(N−1) across editions.

**sgt1925** (views 52–53): the left page is a black image; columns 8–17 are transcribed from view 53. Duration, rate and capital (columns 2–5) are taken from sgt1924 = sgt1926 (`reprint_corrected`), and the sums due (columns 6–7) are solved as total paid + lapsed + outstanding (`derived_from_totals`): 3.530.712,50 / 1.755.482,50 (1891) and 1.840.378,75 / 696.851,25 (1897).

**sgt1926 prints stale sums due.** Its columns 6–7 (headed "à la fin de l'exercice 1924") carry exactly the 1925 values solved above, so the 1926 identities outstanding = due − paid − lapsed fail by the 1926 coupons and bonds (listed below); stored as printed. From sgt1927 the column is current again (headed 1927; sgt1928/29 "1927" with 1928 figures; sgt1930 1929).

## Validation

Rows: 256. Years: 1922 (sgt1922), 1923 (sgt1923), 1924 (sgt1924), 1925 (sgt1925), 1926 (sgt1926), 1927 (sgt1927), 1928 (sgt1929), 1929 (sgt1930).

- Checks (row identities and commune *Totaux*): 222; passed: 197; failed: 25 (printed values kept; each re-read on the image).
  - sgt1926 p.36 Commune de Tunis / 17 février 1891: int_outstanding printed 49026.25, int_due - int_paid_total - int_lapsed = -14796.25
  - sgt1926 p.36 Commune de Tunis / 17 février 1891: cap_outstanding printed 95777.50, cap_due - cap_paid_total - cap_lapsed = 6777.50
  - sgt1926 p.36 Commune de Tunis / 31 janvier 1897: int_outstanding printed 34755, int_due - int_paid_total - int_lapsed = -13203.75
  - sgt1926 p.36 Commune de Tunis / 31 janvier 1897: cap_outstanding printed 42823.75, cap_due - cap_paid_total - cap_lapsed = 2323.75
  - sgt1926 p.36 Commune de Tunis / Totaux: cap_outstanding printed 138601.25, cap_due - cap_paid_total - cap_lapsed = 9101.25
  - sgt1927 p.36 Commune de Tunis / 17 février 1891: cap_paid_total printed 1849451.25, cap_paid_year + cap_paid_before = 1849951.25
  - sgt1927 p.36 Commune de Tunis / 17 février 1891: cap_outstanding printed 87031.25, cap_due - cap_paid_total - cap_lapsed = 114531.25
  - sgt1927 p.36 Commune de Tunis cap_due: cells give 2743333.75, printed total 2716333.75 (difference -27000.00)
  - sgt1927 p.36 Commune de Tunis cap_paid_total: cells give 2591891.25, printed total 2592391.25 (difference 500.00)
  - sgt1928 p.36 Commune de Tunis / 17 février 1891: int_paid_total printed 3563047.50, int_paid_year + int_paid_before = 3663047.50
  - sgt1928 p.36 Commune de Tunis / 17 février 1891: cap_paid_total printed 1938846.25, cap_paid_year + cap_paid_before = 1938346.25
  - sgt1928 p.36 Commune de Tunis / 17 février 1891: int_outstanding printed 47775, int_due - int_paid_total - int_lapsed = 147775.00
  - sgt1928 p.36 Commune de Tunis / 31 janvier 1897: cap_paid_total printed 779922.50, cap_paid_year + cap_paid_before = 779932.50
  - sgt1928 p.36 Commune de Tunis cap_paid_year: cells give 126387.50, printed total 126377.50 (difference -10.00)
  - sgt1928 p.36 Commune de Tunis cap_paid_before: cells give 2591891.25, printed total 2592391.25 (difference 500.00)
  - sgt1928 p.36 Commune de Tunis int_paid_total: cells give 5506868.75, printed total 5606868.75 (difference 100000.00)
  - sgt1929 p.36 Commune de Tunis / 17 février 1891: int_paid_total printed 3563047.50, int_paid_year + int_paid_before = 3663047.50
  - sgt1929 p.36 Commune de Tunis / 17 février 1891: cap_paid_total printed 1938846.25, cap_paid_year + cap_paid_before = 1938346.25
  - sgt1929 p.36 Commune de Tunis / 17 février 1891: int_outstanding printed 47775, int_due - int_paid_total - int_lapsed = 147775.00
  - sgt1929 p.36 Commune de Tunis / 31 janvier 1897: cap_paid_total printed 779922.50, cap_paid_year + cap_paid_before = 779932.50
  - sgt1929 p.36 Commune de Tunis cap_paid_year: cells give 126387.50, printed total 126377.50 (difference -10.00)
  - sgt1929 p.36 Commune de Tunis cap_paid_before: cells give 2591891.25, printed total 2592391.25 (difference 500.00)
  - sgt1929 p.36 Commune de Tunis int_paid_total: cells give 5506868.75, printed total 5606868.75 (difference 100000.00)
  - sgt1930 p.36 Commune de Tunis / Totaux: cap_outstanding printed 173678.25, cap_due - cap_paid_total - cap_lapsed = 173678.75
  - sgt1930 p.36 Commune de Tunis cap_outstanding: cells give 173678.75, printed total 173678.25 (difference -0.50)
- Cross-edition checks (paid before in year N = paid total in year N-1): 28; differences: 1.
  - Tunis 17 février 1891: interest_paid_before 1929 (sgt1930) = 3663047.50, interest_paid_total 1928 (sgt1929) = 3563047.50
- 1928 printed twice (sgt1928 and sgt1929; stored from sgt1929, rule 4): 32 cells compared; differences: 0.
- sgt1925 view 52 (black image), left-page cells: 12 filled, 0 left out:
  - Commune de Tunis / 17 février 1891 duration_years: 50 (sgt1924 = sgt1926)
  - Commune de Tunis / 17 février 1891 capital_received: 3000000 (sgt1924 = sgt1926)
  - Commune de Tunis / 17 février 1891 capital_nominal: 3623500 (sgt1924 = sgt1926)
  - Commune de Tunis / 17 février 1891 interest_rate_pct: 3.5 (sgt1924 = sgt1926)
  - Commune de Tunis / 17 février 1891 interest_due: 3530712.50 (paid total + lapsed + outstanding)
  - Commune de Tunis / 17 février 1891 capital_due: 1755482.50 (paid total + lapsed + outstanding)
  - Commune de Tunis / 31 janvier 1897 duration_years: 50 (sgt1924 = sgt1926)
  - Commune de Tunis / 31 janvier 1897 capital_received: 2000000 (sgt1924 = sgt1926)
  - Commune de Tunis / 31 janvier 1897 capital_nominal: 2087500 (sgt1924 = sgt1926)
  - Commune de Tunis / 31 janvier 1897 interest_rate_pct: 3.5 (sgt1924 = sgt1926)
  - Commune de Tunis / 31 janvier 1897 interest_due: 1840378.75 (paid total + lapsed + outstanding)
  - Commune de Tunis / 31 janvier 1897 capital_due: 696851.25 (paid total + lapsed + outstanding)
Flagged cells: derived_from_totals: 4, illegible: 2, reprint_corrected: 8.
  - sgt1925 Tunis / 17 février 1891 interest_due: derived_from_totals
  - sgt1925 Tunis / 17 février 1891 capital_due: derived_from_totals
  - sgt1925 Tunis / 31 janvier 1897 interest_due: derived_from_totals
  - sgt1925 Tunis / 31 janvier 1897 capital_due: derived_from_totals
  - sgt1922 Tunis / 17 février 1891 capital_due: illegible (franc part 1505982)
  - sgt1922 Tunis / 31 janvier 1897 capital_due: illegible (franc part 583851)
  - sgt1925 Tunis / 17 février 1891 duration_years: reprint_corrected
  - sgt1925 Tunis / 17 février 1891 interest_rate_pct: reprint_corrected
  - sgt1925 Tunis / 17 février 1891 capital_received: reprint_corrected
  - sgt1925 Tunis / 17 février 1891 capital_nominal: reprint_corrected
  - sgt1925 Tunis / 31 janvier 1897 duration_years: reprint_corrected
  - sgt1925 Tunis / 31 janvier 1897 interest_rate_pct: reprint_corrected
  - sgt1925 Tunis / 31 janvier 1897 capital_received: reprint_corrected
  - sgt1925 Tunis / 31 janvier 1897 capital_nominal: reprint_corrected
