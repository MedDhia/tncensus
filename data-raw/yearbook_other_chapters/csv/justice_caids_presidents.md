# Juridiction des caïds, kahias ou khalifas délégués et des présidents des tribunaux régionaux : affaires civiles et pénales

*Jurisdiction of the caïds, kahias or khalifas and of the presidents of the regional courts: civil and penal cases.*

Source: *Statistique générale de la Tunisie*, chapter *Justice*, editions sgt1922, sgt1923, sgt1924, sgt1925, sgt1926, sgt1927, sgt1928, sgt1929, sgt1930. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views of the stored values: sgt1922 (`bpt6k9105649x`): p. 69, f93; sgt1923 (`bpt6k9105649x`): p. 78, f576; sgt1924 (`bpt6k9105649x`): p. 76, f1066; sgt1925 (`bpt6k9105650k`): p. 77, f101; sgt1926 (`bpt6k9105650k`): p. 87, f651; sgt1927 (`bpt6k91056510`): p. 89, f113; sgt1928 (`bpt6k91056510`): p. 85, f637; sgt1929 (`bpt6k9105652d`): p. 87, f115; sgt1930 (`bpt6k9105652d`): p. 91, f649.

Transcriptions: `../transcribed/justice_<edition>.txt`; rebuild with `python3 data-raw/yearbook_other_chapters/extract_justice.py build`.

Rows: 1474. Years: 1921, 1922, 1923, 1924, 1925, 1926, 1927, 1928, 1929, 1930.

Unit: number of cases (integer); `»` printed = 0.

Printed for overlapping year windows (ten years for the French courts until sgt1930, three from sgt1935; five years for the Ouzara and the regional courts; two years for the caïds and presidents): each year is taken from the **latest** edition that prints it (SPEC_ADDENDUM rule 4; `census` = that edition); every other printing of the same cell is compared below and not stored.

## Columns

- `census`: edition the value is taken from (`sgt1922` … `sgt1939`)
- `table_id`: transcription section name
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number
- `gallica_view`: Gallica view (fNNNN)
- `year`: year of the figures
- `matter`: `civil`, `correctional`, `penal`, `criminal` (Affaires civiles / correctionnelles / pénales / criminelles)
- `jurisdiction`: caïdat, kahialik, khalifalik or president of a regional court, as printed
- `measure`: English code of the printed column (see measure_fr)
- `measure_fr`: printed French heading
- `value`: count of cases (integer); money in francs with centimes; percentages as printed
- `flag`: empty, `ocr_corrected`, `illegible`, `total_mismatch`, `not_applicable`, `reprint_corrected`

Cases judged by the caïds, kahias or khalifas (delegated) and by the presidents of the regional courts, per jurisdiction as printed ("Caïd de Béja", "Kahia de Soliman", "Khalifa des Beni-Zid", "Président de la Driba" …), civil and penal, per year. The TOTAUX line is a check only.

The list of jurisdictions changes almost every edition (new khalifaliks, renamings, Tamerza printed "Supprimé" from 1929, stored NA with flag `not_applicable`). Names are as printed in the edition the value is taken from, normalised to "Caïd de …", "Kahia de …", "Khalifa(t) de …", "Président (du Tribunal) de …" (the printed lines carry a dash for the repeated title). sgt1922-sgt1924 print "Khalifa de Sbeitla" twice (the second line from sgt1923; stored as "Khalifa de Sbeitla (second line)"; its figures continue from sgt1925 as "Khalifat de Sbikha" and are matched to it). Printings are matched on the place name (titles, accents and spelling variants such as Djemal / Djemmal, Djelass / Jlass normalised). In sgt1924 the 1924 column of the khalifas from Beni-Zid to Zarzis is printed one line off the 1923 column (sgt1925 prints the same figures one line lower, on Djemmal … Zarzis, consistent with its new list): 1924 is stored from sgt1925 and the sgt1924 cells appear among the differences below. sgt1924 and sgt1925 also swap the 1924 figures of the presidents of Sousse and Sfax. The "A reporter" / "Report" lines of sgt1925-sgt1930 are checks only.

sgt1925 prints the 1925 figures of the khalifalik of Touazine on the Utique line (Utique 136 / 114, Touazine »); sgt1926 prints them on the Touazine line (Touazine 136 / 114, Utique » / 17): the later printing is stored and the difference is listed below.

The page-by-page survey of the chapter in every edition (every table found, with views) is in `justice_survey.md` and in `justice_validation.json` (`_survey`).

## Validation

- Checks against printed totals and identities: 54; passed: 43; failed: 11.

Failed checks (printed values kept; every failure was re-read on a native-resolution crop, or recurs unchanged in another edition's printing of the same cells):

  - sgt1922 p.69 (f93) tn_caids civil:1921: lines vs TOTAUX: cells give 14939, printed 14844 (difference -95)
  - sgt1922 p.69 (f93) tn_caids civil:1922: lines vs TOTAUX: cells give 13512, printed 13572 (difference 60)
  - sgt1924 p.76 (f1066) tn_caids civil:1924: lines vs TOTAUX: cells give 13210, printed 13220 (difference 10)
  - sgt1924 p.76 (f1066) tn_caids penal:1924: lines vs TOTAUX: cells give 40547, printed 40558 (difference 11)
  - sgt1925 p.77 (f101) tn_caids penal:1924: lines vs TOTAUX: cells give 40557, printed 40547 (difference -10)
  - sgt1926 p.87 (f651) tn_caids penal:1926: lines vs A reporter: cells give 43839, printed 43842 (difference 3)
  - sgt1926 p.87 (f651) tn_caids civil:1926: lines vs TOTAUX: cells give 9324, printed 9334 (difference 10)
  - sgt1927 p.89 (f113) tn_caids penal:1926: lines vs A reporter: cells give 43841, printed 43842 (difference 1)
  - sgt1927 p.89 (f113) tn_caids civil:1926: lines vs TOTAUX: cells give 9328, printed 9334 (difference 6)
  - sgt1927 p.89 (f113) tn_caids penal:1927: lines vs TOTAUX: cells give 53263, printed 53163 (difference -100)
  - sgt1928 p.85 (f637) tn_caids penal:1927: lines vs TOTAUX: cells give 53263, printed 53163 (difference -100)

- Overlapping printings: 1090 cell comparisons with other editions printing the same cell; 25 differences.

| cell | edition | printed | stored from | printed |
|---|---|---|---|---|
| 1922 /  / civil /  /  / zarzis / cases | sgt1922 | 107 | sgt1923 | 167 |
| 1924 /  / civil /  /  / djemmal / cases | sgt1924 | 59 | sgt1925 | 227 |
| 1924 /  / penal /  /  / djemmal / cases | sgt1924 | 84 | sgt1925 | 692 |
| 1924 /  / civil /  /  / jlasselguebala / cases | sgt1924 | 345 | sgt1925 | 59 |
| 1924 /  / penal /  /  / jlasselguebala / cases | sgt1924 | 13 | sgt1925 | 94 |
| 1924 /  / civil /  /  / eldjem / cases | sgt1924 | 39 | sgt1925 | 345 |
| 1924 /  / penal /  /  / eldjem / cases | sgt1924 | 128 | sgt1925 | 13 |
| 1924 /  / civil /  /  / hadjebelaioun / cases | sgt1924 | 30 | sgt1925 | 39 |
| 1924 /  / penal /  /  / hadjebelaioun / cases | sgt1924 | 28 | sgt1925 | 128 |
| 1924 /  / civil /  /  / maknassi / cases | sgt1924 | 20 | sgt1925 | 30 |
| 1924 /  / penal /  /  / maknassi / cases | sgt1924 | 170 | sgt1925 | 28 |
| 1924 /  / civil /  /  / metlaoui / cases | sgt1924 | 0 | sgt1925 | 20 |
| 1924 /  / penal /  /  / metlaoui / cases | sgt1924 | 442 | sgt1925 | 170 |
| 1924 /  / civil /  /  / tebourba / cases | sgt1924 | 168 | sgt1925 | 0 |
| 1924 /  / penal /  /  / tebourba / cases | sgt1924 | 157 | sgt1925 | 442 |
| 1924 /  / civil /  /  / zarzis / cases | sgt1924 | 0 | sgt1925 | 117 |
| 1924 /  / penal /  /  / zarzis / cases | sgt1924 | 0 | sgt1925 | 179 |
| 1924 /  / civil /  /  / P:sousse / cases | sgt1924 | 770 | sgt1925 | 945 |
| 1924 /  / civil /  /  / P:sfax / cases | sgt1924 | 945 | sgt1925 | 770 |
| 1925 /  / civil /  /  / utique / cases | sgt1925 | 136 | sgt1926 | 0 |
| 1925 /  / penal /  /  / utique / cases | sgt1925 | 114 | sgt1926 | 0 |
| 1925 /  / civil /  /  / touazine / cases | sgt1925 | 0 | sgt1926 | 136 |
| 1925 /  / penal /  /  / touazine / cases | sgt1925 | 0 | sgt1926 | 114 |
| 1926 /  / penal /  /  / P:kef / cases | sgt1926 | 622 | sgt1927 | 624 |
| 1926 /  / civil /  /  / ouledouezzez / cases | sgt1926 | 0 | sgt1927 | 4 |

- Flagged cells: not_applicable: 4, ocr_corrected: 3.

  - sgt1930 p.91 1929 civil / Khalifat de Tamerza / cases = NA (not_applicable)
  - sgt1930 p.91 1930 civil / Khalifat de Tamerza / cases = NA (not_applicable)
  - sgt1929 p.87 1928 civil / Président du Tribunal de Gabès / cases = 149 (ocr_corrected)
  - sgt1930 p.91 1929 penal / Khalifat de Tamerza / cases = NA (not_applicable)
  - sgt1930 p.91 1930 penal / Khalifat de Tamerza / cases = NA (not_applicable)
  - sgt1929 p.87 1928 penal / Président du Tribunal de Gabès / cases = 806 (ocr_corrected)
  - sgt1930 p.91 1929 penal / Président du Tribunal de la Driba / cases = 19380 (ocr_corrected)

## Image versus OCR

- Read cell by cell on the page images (6 printings): sgt1923 f576, sgt1924 f1066, sgt1925 f101, sgt1926 f651, sgt1927 f113, sgt1928 f637.
- Drafted from the Gallica OCR and accepted on the checks above, with every failing check and every unclear OCR token re-read on a native-resolution crop (3 printings): sgt1922 f93 (civil 1921 column (whole column re-read on the image: sum 14.939, printed 14.844)), sgt1929 f115, sgt1930 f649 (Kairouan to Mateur; the rest OCR).
- Cells whose image reading differs from the OCR (flag `ocr_corrected`): 8.
