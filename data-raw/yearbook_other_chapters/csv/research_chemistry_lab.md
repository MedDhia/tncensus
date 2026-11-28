# Laboratoire de chimie. Analyses effectuées

*Chemistry laboratories (Tunis, Sfax): analyses made, by nature of the sample and requesting service.*

Source: *Statistique générale de la Tunisie*, chapter *Institutions d'enseignement et de recherches*, editions sgt1925, sgt1926, sgt1927, sgt1928, sgt1929, sgt1930, sgt1935, sgt1936, sgt1939. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views of the stored values: sgt1925 (`bpt6k9105650k`): p. 317, f341; sgt1926 (`bpt6k9105650k`): p. 287, f851; sgt1927 (`bpt6k91056510`): p. 285, f313; sgt1928 (`bpt6k91056510`): p. 289, f841; sgt1929 (`bpt6k9105652d`): p. 290, f318, p. 291, f319; sgt1930 (`bpt6k9105652d`): p. 297, f855, p. 298, f856; sgt1935 (`bpt6k9105653t`): p. 144, f164, p. 145, f165; sgt1936 (`bpt6k91056547`): p. 111, f122; sgt1939 (`bpt6k9105739w`): p. 115, f121.

Transcriptions: `../transcribed/research_<edition>.txt`; rebuild with `python3 data-raw/yearbook_other_chapters/extract_research.py build`.

Rows: 2718. Years: 1925, 1926, 1927, 1928, 1929, 1930, 1935, 1936, 1939.

Unit: analyses (count); value_type: count.

Selection (SPEC_ADDENDUM rule 5): printed once per edition (the edition's year); all editions kept.

## Columns

- `census`: source edition (`sgt1922` ... `sgt1939`)
- `table_id`: section code of the transcription
- `gallica_ark`: Gallica volume ark
- `source_page`: printed page number
- `gallica_view`: Gallica view
- `year`: year of the figure (for a school year or season: the year it ends; for promotions and once-per-edition tables: the edition year)
- `laboratory`: laboratory (Tunis, Sfax)
- `sample`: ASCII slug of `sample_fr`
- `sample_fr`: nature des échantillons, as printed
- `service`: service of the Institut (ASCII slug of `service_fr`)
- `service_fr`: service heading as printed
- `value`: printed figure (» = 0)
- `flag`: empty, or ocr_corrected / illegible / total_mismatch / derived_from_totals / not_applicable / reprint_corrected / row_realigned

Row totals (Totaux par catégories) and column totals (Totaux par service) are checks only.

Every failed check below was re-read on a zoomed native-resolution crop: they are printed inconsistencies (printed values kept). sgt1927 Tunis Huiles essentielles: the 1 printed under Analyses payantes contradicts both the row total (6) and the column total (2.337); flagged total_mismatch. sgt1928 Tunis Spiritueux et liqueurs: row total printed 10 and the public cell », where the column totals need public 10 and row total 73 (public flagged total_mismatch). sgt1929 Tunis: grand total 6.674 for 6.666 (sum of the service totals). sgt1929 Tunis Engrais/Epices/Farines fraud cells printed one line high (realigned, row_realigned). sgt1930 Sfax: Études column total 185 for 183 and grand total 2.939 for 2.941.

Survey of the whole chapter in every edition: `research_survey.md`.

## Validation

- Checks against printed totals and identities: 535; passed: 524; failed: 11.

Failed checks (printed values kept; every failure was re-read on a native-resolution crop, or recurs unchanged in another edition's printing of the same cells):

  - sgt1927 p.285 (f313) chemlab [Tunis] Huiles essentielles: total = sum: cells give 7, printed 6 (difference -1)
  - sgt1927 p.285 (f313) chemlab [Tunis] public: lines vs Totaux par service: cells give 2338, printed 2337 (difference -1)
  - sgt1928 p.289 (f841) chemlab [Tunis] Spiritueux et liqueurs: total = sum: cells give 63, printed 10 (difference -53)
  - sgt1928 p.289 (f841) chemlab [Tunis] public: lines vs Totaux par service: cells give 2616, printed 2626 (difference 10)
  - sgt1928 p.289 (f841) chemlab [Tunis] total: lines vs Totaux par service: cells give 5780, printed 5843 (difference 63)
  - sgt1929 p.290 (f318) chemlab [Tunis] Totaux par service: total = sum: cells give 6666, printed 6674 (difference 8)
  - sgt1929 p.290 (f318) chemlab [Tunis] total: lines vs Totaux par service: cells give 6666, printed 6674 (difference 8)
  - sgt1930 p.298 (f856) chemlab [Sfax] Totaux: total = sum: cells give 2941, printed 2939 (difference -2)
  - sgt1930 p.298 (f856) chemlab [Sfax] studies: lines vs Totaux: cells give 183, printed 185 (difference 2)
  - sgt1936 p.111 (f122) chemlab [Sfax] Goudrons, huiles de goudron: total = sum: cells give 12, printed 2 (difference -10)
  - sgt1936 p.111 (f122) chemlab [Sfax] customs: lines vs Totaux par service: cells give 1671, printed 1661 (difference -10)

- Overlapping printings: 0 cell comparisons with other editions printing the same cell; 0 differences.

- Flagged cells: derived_from_totals: 1, row_realigned: 16, total_mismatch: 4.

  - sgt1927 p.285 1927 Tunis / huiles_essentielles / paid_public = 1 (total_mismatch)
  - sgt1928 p.289 1928 Tunis / spiritueux_et_liqueurs / paid_public = 0 (total_mismatch)
  - sgt1929 p.290 1929 Tunis / engrais_produits_anticryptogamiques / fraud_repression_good = 0 (row_realigned)
  - sgt1929 p.290 1929 Tunis / engrais_produits_anticryptogamiques / fraud_repression_suspect = 0 (row_realigned)
  - sgt1929 p.290 1929 Tunis / epices / fraud_repression_good = 20 (row_realigned)
  - sgt1929 p.290 1929 Tunis / epices / fraud_repression_suspect = 12 (row_realigned)
  - sgt1929 p.290 1929 Tunis / farines_et_farineux_alimentaires / fraud_repression_good = 12 (row_realigned)
  - sgt1929 p.290 1929 Tunis / farines_et_farineux_alimentaires / fraud_repression_suspect = 12 (row_realigned)
  - sgt1929 p.291 1929 Sfax / engrais_produits_anticryptogamiques / fraud_repression_good = 0 (row_realigned)
  - sgt1929 p.291 1929 Sfax / engrais_produits_anticryptogamiques / fraud_repression_suspect = 0 (row_realigned)
  - sgt1929 p.291 1929 Sfax / epices / fraud_repression_good = 0 (row_realigned)
  - sgt1929 p.291 1929 Sfax / epices / fraud_repression_suspect = 0 (row_realigned)
  - sgt1936 p.111 1936 Tunis / goudrons_huiles_de_goudron / customs = 7 (total_mismatch)
  - sgt1936 p.111 1936 Tunis / mouts_mutes / customs = 429 (row_realigned)
  - sgt1936 p.111 1936 Tunis / petroles_mazouts_essences / customs = 430 (row_realigned)
  - sgt1936 p.111 1936 Tunis / produits_alimentaires_divers / customs = 68 (row_realigned)
  - sgt1936 p.111 1936 Tunis / produits_chimiques / customs = 0 (derived_from_totals)
  - sgt1936 p.111 1936 Sfax / goudrons_huiles_de_goudron / customs = 12 (total_mismatch)
  - sgt1936 p.111 1936 Sfax / mouts_mutes / customs = 0 (row_realigned)
  - sgt1936 p.111 1936 Sfax / petroles_mazouts_essences / customs = 0 (row_realigned)
  - sgt1936 p.111 1936 Sfax / produits_alimentaires_divers / customs = 2 (row_realigned)

## Image versus OCR

- Read cell by cell on the page images (13 printings): sgt1925 f341, sgt1926 f851, sgt1927 f313, sgt1928 f841, sgt1929 f318, sgt1929 f319, sgt1930 f855, sgt1930 f856, sgt1935 f164, sgt1935 f165, sgt1936 f122, sgt1936 f122, sgt1939 f121.
- Drafted from the Gallica OCR and accepted on the checks above, with every failing check and every unclear OCR token re-read on a native-resolution crop (0 printings): none.
- Cells whose image reading differs from the OCR (flag `ocr_corrected`): 0.
