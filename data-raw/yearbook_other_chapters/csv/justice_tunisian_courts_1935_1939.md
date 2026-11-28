# Justice tunisienne, juridictions de droit commun : statistique annuelle (Chambre des requêtes, Tribunaux d'appel de l'Ouzara, Tribunaux de première instance, parquets, chambres d'instruction, présidents et officiers de police judiciaire, assistance judiciaire)

*Tunisian justice, ordinary courts: yearly statistics (from sgt1935).*

Source: *Statistique générale de la Tunisie*, chapter *Justice*, editions sgt1935, sgt1936, sgt1939. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views of the stored values: sgt1935 (`bpt6k9105653t`): p. 55, f75, p. 56, f76, p. 57, f77, p. 58, f78; sgt1936 (`bpt6k91056547`): p. 44, f55, p. 45, f56, p. 46, f57; sgt1939 (`bpt6k9105739w`): p. 44, f50, p. 45, f51, p. 46, f52.

Transcriptions: `../transcribed/justice_<edition>.txt`; rebuild with `python3 data-raw/yearbook_other_chapters/extract_justice.py build`.

Rows: 360. Years: 1934, 1935, 1936, 1938, 1939.

Unit: number of cases (integer); `»` printed = 0.

Printed once per edition for the edition year (SPEC_ADDENDUM rule 5): every edition is kept, `year` = the year of the figures; no year is printed twice, except the two-year columns of the presidents' table (section `presidents`), where the earlier year is taken from the later edition and compared (rule 4).

## Columns

- `census`: edition the value is taken from (`sgt1922` … `sgt1939`)
- `table_id`: transcription section name
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number
- `gallica_view`: Gallica view (fNNNN)
- `year`: year of the figures
- `section`: part of the yearly statistics (see the notes)
- `section_fr`: printed heading of that part
- `tribunal`: court as printed
- `measure`: English code of the printed column (see measure_fr)
- `measure_fr`: printed French heading
- `value`: count of cases (integer); money in francs with centimes; percentages as printed
- `flag`: empty, `ocr_corrected`, `illegible`, `total_mismatch`, `not_applicable`, `reprint_corrected`

From sgt1935 the Tunisian-justice part of the chapter is recast as one-year statistics of the "juridictions de droit commun" (rule 5: printed once per edition; year = the year in the heading). `section` codes: `requests_chamber` (I. Chambre des requêtes), `ouzara_civil` / `ouzara_penal` / `ouzara_indictment` (II. Tribunaux d'appel de l'Ouzara: a) affaires civiles, b) affaires pénales, c) Chambre des mises en accusation), `first_instance_civil` / `first_instance_penal` (III. Tribunaux de première instance), `prosecutors` (c) Travaux des parquets), `investigation` (d) Travaux des chambres d'instruction), `presidents` (IV. Juridictions des présidents et officiers de police judiciaire, two years per edition), `legal_aid` (Travaux du bureau de l'assistance judiciaire). Printed TOTAL columns and TOTAUX lines are checks only. The footnote to III a) says: "there are no default judgments in Tunisian civil procedure".

The page-by-page survey of the chapter in every edition (every table found, with views) is in `justice_survey.md` and in `justice_validation.json` (`_survey`).

## Validation

- Checks against printed totals and identities: 146; passed: 144; failed: 2.

Failed checks (printed values kept; every failure was re-read on a native-resolution crop, or recurs unchanged in another edition's printing of the same cells):

  - sgt1936 p.45 (f56) tn_stats default: lines vs TOTAUX: cells give 6205, printed 6211 (difference 6)
  - sgt1936 p.45 (f56) tn_stats total: lines vs TOTAUX: cells give 19528, printed 19534 (difference 6)

- Overlapping printings: 4 cell comparisons with other editions printing the same cell; 0 differences.

- Flagged cells: none.

## Image versus OCR

- Read cell by cell on the page images (26 printings): sgt1935 f75, sgt1935 f75, sgt1935 f75, sgt1935 f75, sgt1935 f76, sgt1935 f76, sgt1935 f77, sgt1935 f77, sgt1935 f78, sgt1935 f78, sgt1936 f55, sgt1936 f55, sgt1936 f55, sgt1936 f55, sgt1936 f56, sgt1936 f56, sgt1936 f56, sgt1936 f57, sgt1939 f50, sgt1939 f50, sgt1939 f50, sgt1939 f50, sgt1939 f51, sgt1939 f51, sgt1939 f51, sgt1939 f52.
- Drafted from the Gallica OCR and accepted on the checks above, with every failing check and every unclear OCR token re-read on a native-resolution crop (0 printings): none.
- Cells whose image reading differs from the OCR (flag `ocr_corrected`): 0.
