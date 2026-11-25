# Hôpital civil français de Tunis : mouvement de la consultation et des pansements externes ; opérations

*French Civil Hospital of Tunis: external consultations and dressings; operations.*

Source: *Statistique générale de la Tunisie*, chapter III (health), editions sgt1927, sgt1929, sgt1930, sgt1935, sgt1936, sgt1939. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views used: sgt1927 (`bpt6k91056510`): p. 64, f92; sgt1929 (`bpt6k9105652d`): p. 66, f94; sgt1930 (`bpt6k9105652d`): p. 70, f628; sgt1935 (`bpt6k9105653t`): p. 42, f62; sgt1936 (`bpt6k91056547`): p. 32, f43; sgt1939 (`bpt6k9105739w`): p. 33, f39.

Transcriptions: `../transcribed/health_pop_<edition>.txt`, section `@civil_consultations`; rebuild with `python3 data-raw/yearbook_health_education/extract_health_population.py build`. Per-check output: `health_validation.json`.

Rows: 54. Years: 1924–1939 (14 years: 1924, 1925, 1926, 1927, 1928, 1929, 1930, 1933, 1934, 1935, 1936, 1937, 1938, 1939).

Printed for overlapping year windows: each year is taken from the **latest** edition that prints it (SPEC_ADDENDUM rule 4; `census` = that edition) and every other printing of the same cell is compared below. Duplicate printings are not stored.

Years printed by each edition: sgt1926 1924–1926; sgt1927 1924–1927; sgt1928 1925–1928; sgt1929 1925–1929; sgt1930 1926–1930; sgt1935 1933–1935; sgt1936 1934–1936; sgt1939 1937–1939.

## Columns

- `census`: edition the value is taken from (`sgt1922` … `sgt1939`)
- `table_id`: transcription section the value comes from
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number
- `gallica_view`: Gallica view (fNNNN)
- `year`: year the value refers to
- `measure`: what is counted (see below)
- `measure_fr`: column heading (French)
- `value`: count (integer), except where the notes say otherwise; printed » = 0
- `flag`: empty, or `ocr_corrected`, `illegible`, `total_mismatch`, `not_applicable`, `reprint_corrected` (see below)

Printed totals (row totals, TOTAUX lines, nationality brackets) and the printed "différence en plus / en moins" columns are not stored; they were used for validation.

Table d) "Mouvement de la consultation et des pansements externes avec distribution de médicaments à titre gratuit — Opérations", printed from sgt1926. Columns: sgt1926–sgt1930 "Personnel externe" (`staff_external`), "Consultations gratuites", "Service de la radiologie", TOTAL, "Nombre des opérations"; from sgt1935 the first column is headed "Pansements …" (`external_dressings`). Operations 1924–1925 are printed » meaning not recorded (not stored). TOTAL is not stored.

1929 radiology: sgt1930 prints 5.003, sgt1929 6.003; with 6.003 the parts give 51.254 against the 51.253 printed in both, so the sgt1929 value is kept (`reprint_corrected`). Remaining failures are printed totals off by 1–5: 1926 (72.070 vs 72.071, all five printings), 1929 (51.254 vs 51.253), 1936 (223.847 vs 223.852).

## Validation

- Checks against printed totals: 30; passed: 22; failed: 8.

Failed checks (printed values kept; every one was re-read on the page image and the printed figures are as transcribed; see the commentary above for the cells involved):

  - sgt1926 civil_consultations 1926: parts vs total: cells give 72070, printed 72071
  - sgt1927 civil_consultations 1926: parts vs total: cells give 72070, printed 72071
  - sgt1928 civil_consultations 1926: parts vs total: cells give 72070, printed 72071
  - sgt1929 civil_consultations 1926: parts vs total: cells give 72070, printed 72071
  - sgt1929 civil_consultations 1929: parts vs total: cells give 51254, printed 51253
  - sgt1930 civil_consultations 1926: parts vs total: cells give 72070, printed 72071
  - sgt1930 civil_consultations 1929: parts vs total: cells give 50254, printed 51253
  - sgt1936 civil_consultations 1936: parts vs total: cells give 223847, printed 223852

- Overlapping printings: 80 cell comparisons between editions; 1 differences.

| year | cell | edition | printed | latest edition | printed | stored (edition, flag) |
|---|---|---|---|---|---|---|
| 1929 | radiology | sgt1929 | 6003 | sgt1930 | 5003 | 6003 (sgt1929, reprint_corrected) |

- Flagged cells: reprint_corrected: 1.

  - sgt1929 1929 radiology / Service de la radiologie = 6003 (reprint_corrected)
