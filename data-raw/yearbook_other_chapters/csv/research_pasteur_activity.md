# Institut Pasteur. b) Travaux de l'Institut ; c) Service vétérinaire

*Institut Pasteur of Tunis: work of the institute (rabies treatments, analyses, vaccines and sera distributed, veterinary service).*

Source: *Statistique générale de la Tunisie*, chapter *Institutions d'enseignement et de recherches*, editions sgt1935, sgt1936, sgt1939. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views of the stored values: sgt1935 (`bpt6k9105653t`): p. 136, f156, p. 137, f157; sgt1936 (`bpt6k91056547`): p. 106, f117, p. 107, f118; sgt1939 (`bpt6k9105739w`): p. 110, f116, p. 111, f117.

Transcriptions: `../transcribed/research_<edition>.txt`; rebuild with `python3 data-raw/yearbook_other_chapters/extract_research.py build`.

Rows: 224. Years: 1935, 1936, 1939.

Units per line (`unit`): persons, analyses, doses, flacons, cc, ampoules, tubes, litres, samples; value_type: mixed (counts in the printed unit).

Selection (SPEC_ADDENDUM rule 5): printed once per edition (the edition's year); all editions kept.

## Columns

- `census`: source edition (`sgt1922` ... `sgt1939`)
- `table_id`: section code of the transcription
- `gallica_ark`: Gallica volume ark
- `source_page`: printed page number
- `gallica_view`: Gallica view
- `year`: year of the figure (for a school year or season: the year it ends; for promotions and once-per-edition tables: the edition year)
- `service`: service of the Institut (ASCII slug of `service_fr`)
- `service_fr`: service heading as printed
- `item`: ASCII slug of `item_fr`
- `item_fr`: line as printed (sub-heading prefixed, ditto marks expanded)
- `unit`: unit of the line (francs, persons, analyses, doses, flacons, cc, tubes, ampoules, litres, samples, quintals, hectares, producers, count)
- `value`: printed figure (» = 0)
- `flag`: empty, or ocr_corrected / illegible / total_mismatch / derived_from_totals / not_applicable / reprint_corrected / row_realigned

The 'Nombre total des analyses pratiquées' is printed with only the principal analyses itemised ('les principales ont été'): it is stored as its own line and not checked. Printed sub-totals (Mordues: total; Vaccin anticlaveleux: au total) are checks only.

Survey of the whole chapter in every edition: `research_survey.md`.

## Validation

- Checks against printed totals and identities: 6; passed: 6; failed: 0.

- Overlapping printings: 0 cell comparisons with other editions printing the same cell; 0 differences.

- Flagged cells: illegible: 2, not_applicable: 1.

  - sgt1936 p.107 1936 service_veterinaire / tuberculine_diluee_au_1_10_pour_usage_hypodermique / doses = NA (illegible)
  - sgt1939 p.110 1939 service_des_analyses_medicales / 1_analyses_microbiologiques_diverses / analyses = NA (illegible)
  - sgt1939 p.110 1939 produits_divers_non_prepares_a_l_institut / serum_antipesteux / flacons = NA (not_applicable)

## Image versus OCR

- Read cell by cell on the page images (21 printings): sgt1935 f156, sgt1935 f156, sgt1935 f156, sgt1935 f156, sgt1935 f156, sgt1935 f156, sgt1935 f157, sgt1936 f117, sgt1936 f117, sgt1936 f117, sgt1936 f117, sgt1936 f117, sgt1936 f117, sgt1936 f118, sgt1939 f116, sgt1939 f116, sgt1939 f116, sgt1939 f116, sgt1939 f116, sgt1939 f116, sgt1939 f117.
- Drafted from the Gallica OCR and accepted on the checks above, with every failing check and every unclear OCR token re-read on a native-resolution crop (0 printings): none.
- Cells whose image reading differs from the OCR (flag `ocr_corrected`): 0.
