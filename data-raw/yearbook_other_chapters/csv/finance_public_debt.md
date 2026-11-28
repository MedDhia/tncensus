# Dette tunisienne. a) Opérations auxquelles a donné lieu le service de la dette tunisienne depuis 1884

*Tunisian public debt: cumulative charges and payments (capital, interest) by loan and charge, since 1884.*

Source: *Statistique générale de la Tunisie*, chapter *Finances*, editions sgt1925, sgt1926, sgt1928, sgt1929, sgt1930, sgt1935, sgt1936, sgt1939. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views of the stored values: sgt1925 (`bpt6k9105650k`): p. 192, f216; sgt1926 (`bpt6k9105650k`): p. 208, f772; sgt1928 (`bpt6k91056510`): p. 206, f758; sgt1929 (`bpt6k9105652d`): p. 208, f236; sgt1930 (`bpt6k9105652d`): p. 212, f770, p. 213, f771; sgt1935 (`bpt6k9105653t`): p. 111, f131; sgt1936 (`bpt6k91056547`): p. 86, f97; sgt1939 (`bpt6k9105739w`): p. 90, f96.

Transcriptions: `../transcribed/finance_<edition>.txt`; rebuild with `python3 data-raw/yearbook_other_chapters/extract_finance.py build`.

Rows: 580. Years: 1921, 1923, 1924, 1925, 1927, 1934, 1935, 1938.

Unit: francs (centimes kept); value_type: francs.

Each printing gives the operations cumulated from 1884 to a year named in its title (1921, 1923, 1924, 1924, 1925, 1927, 1934, 1935, 1938): one series by that year, each year from the **latest** edition printing it (SPEC_ADDENDUM rule 4; `census` = that edition). Only 1924 is printed twice (sgt1927 and sgt1928, same standing type): sgt1928 is stored and the sgt1927 printing, read independently on its own image, is compared below.

## Columns

- `census`: edition the value is taken from (the latest edition printing that year; 1924: sgt1928, sgt1927 compared)
- `table_id`: transcription section
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number
- `gallica_view`: Gallica view (fNNNN)
- `year`: last year of the cumulative period ("de 1884 à <year>" in the title)
- `period_fr`: period covered, as printed in the title (cumulative operations since 1884)
- `group`: `temporary_charges` for the lines printed under "Charges temporaires diverses incombant au budget beylical" (a brace up to sgt1930, a heading in sgt1935), `debt` otherwise
- `group_fr`: printed group heading (empty for the debt lines proper)
- `item`: debt or charge line code (English), stable across editions
- `item_fr`: printed line label
- `account`: `charges` (charges: amounts due since the origin) or `payments` (paiements ou conversions consommés depuis l'échéance jusqu'à la date de la prescription au profit de l'Etat)
- `account_fr`: printed column-group heading
- `component`: `capital` or `interest` (intérêts)
- `component_fr`: printed column heading
- `unit`: unit of `value`
- `value`: printed amount (» = 0), francs with centimes, cumulative since 1884
- `flag`: empty, or `ocr_corrected` (image reading differs from the Gallica OCR), `total_mismatch` (printed value kept; identified by a failed check as the faulty cell, see Validation), `illegible` (value NA), `not_applicable` (nothing printed, value NA), `derived_from_totals` (digits hidden in the binding; value = the printed row total minus the other cells of the row, see the notes)

Printed sgt1925-sgt1939 (not in sgt1922-sgt1924, whose Finances chapter opens with the taxe personnelle). sgt1925: "Tableau récapitulatif et balance des opérations auxquelles a donné lieu le service de la dette tunisienne de 1884 à 1921" (one page); sgt1926-sgt1935: "a) Opérations auxquelles a donné lieu le service de la dette tunisienne de 1884 à <year>"; sgt1936-sgt1939: "Opérations relatives au service de la dette tunisienne de 1884 à <year>". sgt1930 spreads the table over two pages (A reporter / Report).

One row per printed cell: debt or charge line x account (charges; paiements ou conversions) x component (capital; intérêts). The lines change across editions: new loans (1920, 1932, 1934, 1937-1938), new charges under the brace "Charges temporaires diverses incombant au budget beylical" up to sgt1930, and from sgt1935 a regrouping (railway loan charges, road network loans, agricultural mortgage credit, State participation in consolidation and in regional and communal expenditure, subsidy to the Archbishopric of Carthage; the remaining temporary charges as "Avances à l'Office Postal" and "Autres charges temporaires diverses", sgt1939 "Autres charges temporaires diverses incombant au budget beylical" alone). `item` codes are stable where the printed line is the same; regrouped lines get new codes. The printed Totaux, the A reporter / Report lines (sgt1930) and the sums printed under the braces (charges capital + intérêts; paiements capital + intérêts) are checks, not stored. Part b) (balance) is in `finance_public_debt_balance`.

Failed checks, each re-read on zoomed native-resolution crops (printed errors): sgt1925, paiements capital: the lines sum to 518.887.615 13 against the printed Totaux 521.887.985 13 (3.000.370 more). The Certificats de coupons line is printed 6.884.838 70 here and 9.884.838 70 in every later edition: the 3.000.000 is that cell (flagged `total_mismatch`, printed value kept); the remaining 370 cannot be placed. sgt1929, charges intérêts: the lines sum to 353.693.320 69 (also printed in the balance), the Totaux line prints 353.693.320 62 (zoomed), and the brace sum 1.465.949.248 51 follows the 62; a misprinted total, no cell flagged. sgt1936, charges capital: the lines sum to 2.108.586.561 67, the Totaux (and the balance) print 2.107.586.561 67 (1.000.000 less); every line re-read, no cell can be identified.

Survey of the whole chapter in every edition: `finance_survey.md`.

## Validation

- Checks against printed totals and identities: 62; passed: 58; failed: 4.

Failed checks (printed values kept; every failure was re-read on a native-resolution crop, or recurs unchanged in another edition's printing of the same cells):

  - sgt1925 p.192 (f216) debt pay_cap: Totaux = lines: cells give 518887615.13, printed 521887985.13 (difference 3000370.00)
  - sgt1929 p.208 (f236) debt ch_int: Totaux = lines: cells give 353693320.69, printed 353693320.62 (difference -0.07)
  - sgt1929 p.208 (f236) debt charges: capital + intérêts (brace): cells give 1465949248.44, printed 1465949248.51 (difference 0.07)
  - sgt1936 p.86 (f97) debt ch_cap: Totaux = lines: cells give 2108586561.67, printed 2107586561.67 (difference -1000000.00)

- Overlapping printings: 64 cell comparisons with other editions printing the same cell; 0 differences.

- Flagged cells: ocr_corrected: 37, total_mismatch: 1.

  - sgt1925 p.192 1921 debt / coupon_certificates_pre1870 / payments / capital / francs = 6884838.70 (total_mismatch)
  - sgt1925 p.192 1921 debt / redeemable_3pct_1892 / payments / capital / francs = 15228496.25 (ocr_corrected)
  - sgt1926 p.208 1923 debt / coupon_certificates_pre1870 / charges / capital / francs = 10171756.20 (ocr_corrected)
  - sgt1926 p.208 1923 debt / debt_5pct_1880 / payments / capital / francs = 124965500 (ocr_corrected)
  - sgt1926 p.208 1923 debt / debt_5pct_1880 / payments / interest / francs = 325942 (ocr_corrected)
  - sgt1926 p.208 1923 debt / perpetual_4pct_1884 / charges / interest / francs = 29793570.72 (ocr_corrected)
  - sgt1926 p.208 1923 debt / redeemable_3_5pct_1889 / charges / interest / francs = 20369842.93 (ocr_corrected)
  - sgt1926 p.208 1923 debt / redeemable_3pct_1892 / payments / capital / francs = 17073471.25 (ocr_corrected)
  - sgt1926 p.208 1923 debt / redeemable_3pct_1902_1907 / charges / interest / francs = 61694942.80 (ocr_corrected)
  - sgt1926 p.208 1923 debt / redeemable_3_5pct_1903 / charges / interest / francs = 6863955.16 (ocr_corrected)
  - sgt1926 p.208 1923 debt / redeemable_3_5pct_1903 / payments / capital / francs = 14834973.75 (ocr_corrected)
  - sgt1926 p.208 1923 debt / redeemable_4pct_1912 / charges / interest / francs = 19794331.28 (ocr_corrected)
  - sgt1926 p.208 1923 debt / loan_1920 / charges / interest / francs = 2622275.67 (ocr_corrected)
  - sgt1926 p.208 1923 temporary_charges / tgm_railway_buyback / payments / capital / francs = 4778147.25 (ocr_corrected)
  - sgt1926 p.208 1923 temporary_charges / railway_operating_deficit / payments / capital / francs = 4168563.52 (ocr_corrected)
  - sgt1926 p.208 1923 temporary_charges / postal_office_telephone_advances / payments / capital / francs = 1479952.88 (ocr_corrected)
  - sgt1928 p.206 1924 debt / coupon_certificates_pre1870 / payments / capital / francs = 9884838.70 (ocr_corrected)
  - sgt1928 p.206 1924 debt / redeemable_3_5pct_1903 / charges / capital / francs = 17658000 (ocr_corrected)
  - sgt1929 p.208 1925 debt / redeemable_3pct_1892 / payments / capital / francs = 18859276.25 (ocr_corrected)
  - sgt1929 p.208 1925 debt / redeemable_3_5pct_1903 / charges / interest / francs = 7058126.41 (ocr_corrected)
  - sgt1929 p.208 1925 debt / redeemable_3_5pct_1903 / payments / capital / francs = 14889973.75 (ocr_corrected)
  - sgt1929 p.208 1925 debt / loan_1920 / charges / interest / francs = 9656956.42 (ocr_corrected)
  - sgt1929 p.208 1925 temporary_charges / metropole_military_contribution / charges / capital / francs = 1120000 (ocr_corrected)
  - sgt1930 p.212 1927 debt / perpetual_4pct_1884 / charges / interest / francs = 29793570.72 (ocr_corrected)
  - sgt1930 p.212 1927 debt / perpetual_4pct_1884 / payments / interest / francs = 29792321.93 (ocr_corrected)
  - sgt1930 p.212 1927 debt / loan_1920 / charges / interest / francs = 19770034.18 (ocr_corrected)
  - sgt1935 p.111 1934 debt / redeemable_4pct_1912 / charges / capital / francs = 90500000 (ocr_corrected)
  - sgt1935 p.111 1934 debt / loan_1932 / payments / interest / francs = 4030560 (ocr_corrected)
  - sgt1936 p.86 1935 debt / debt_5pct_1880 / payments / capital / francs = 124965500 (ocr_corrected)
  - sgt1936 p.86 1935 debt / redeemable_4pct_1912 / charges / interest / francs = 66863018.52 (ocr_corrected)
  - sgt1936 p.86 1935 debt / loan_1932 / payments / interest / francs = 8291767.50 (ocr_corrected)
  - sgt1936 p.86 1935 debt / agricultural_mortgage_credit / charges / capital / francs = 29656099.12 (ocr_corrected)
  - sgt1939 p.90 1938 debt / debt_5pct_1880 / charges / capital / francs = 125000000 (ocr_corrected)
  - sgt1939 p.90 1938 debt / debt_5pct_1880 / payments / capital / francs = 124965500 (ocr_corrected)
  - sgt1939 p.90 1938 debt / perpetual_4pct_1884 / charges / capital / francs = 157688000 (ocr_corrected)
  - sgt1939 p.90 1938 debt / loan_1932 / charges / interest / francs = 44463498.75 (ocr_corrected)
  - sgt1939 p.90 1938 debt / railway_loan_charges / charges / interest / francs = 24351033.73 (ocr_corrected)
  - sgt1939 p.90 1938 debt / road_network_loan_charges / charges / interest / francs = 27456028.64 (ocr_corrected)

## Image versus OCR

- Read cell by cell on the page images (10 printings): sgt1925 f216, sgt1926 f772, sgt1927 f234, sgt1928 f758, sgt1929 f236, sgt1930 f770, sgt1930 f771, sgt1935 f131, sgt1936 f97, sgt1939 f96.
- Drafted from the Gallica OCR and accepted on the checks above, with every failing check and every unclear OCR token re-read on a native-resolution crop (0 printings): none.
- Cells whose image reading differs from the OCR (flag `ocr_corrected`): 40.
