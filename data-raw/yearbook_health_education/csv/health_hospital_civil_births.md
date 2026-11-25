# Hôpital civil français de Tunis : naissances à la maternité

*French Civil Hospital of Tunis: births in the maternity ward.*

Source: *Statistique générale de la Tunisie*, chapter III (health), editions sgt1922, sgt1923, sgt1924, sgt1925. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views used: sgt1922 (`bpt6k9105649x`): p. 49, f73; sgt1923 (`bpt6k9105649x`): p. 55, f557; sgt1924 (`bpt6k9105649x`): p. 57, f1047; sgt1925 (`bpt6k9105650k`): p. 57, f81.

Transcriptions: `../transcribed/health_pop_<edition>.txt`, section `@civil_births`; rebuild with `python3 data-raw/yearbook_health_education/extract_health_population.py build`. Per-check output: `health_validation.json`.

Rows: 17. Years: 1922–1925.

Printed once per edition, for the edition's own year; all editions are kept (SPEC_ADDENDUM rule 5).

## Columns

- `census`: edition the value is taken from (`sgt1922` … `sgt1939`)
- `table_id`: transcription section the value comes from
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number
- `gallica_view`: Gallica view (fNNNN)
- `year`: year the value refers to
- `category`: `legitimate`, `illegitimate`, `stillborn`
- `category_fr`: as printed
- `sex`: `male`, `female`, or `total` / empty where not split
- `sex_fr`: as printed
- `value`: count (integer), except where the notes say otherwise; printed » = 0
- `flag`: empty, or `ocr_corrected`, `illegible`, `total_mismatch`, `not_applicable`, `reprint_corrected` (see below)

Printed totals (row totals, TOTAUX lines, nationality brackets) and the printed "différence en plus / en moins" columns are not stored; they were used for validation.

Table d) "Naissances" (maternity of the Hôpital civil français), printed sgt1922–sgt1925. Garçons / Filles by Légitimes / Illégitimes; the TOTAL column and TOTAUX row are not stored. sgt1925 adds a "Récapitulation" with Morts-nés 12 (stored as `stillborn` / `total`; recap total 354 = 342 + 12).

## Validation

- Checks against printed totals: 24; passed: 24; failed: 0.

- Flagged cells: none.
