# Extraction spec: 1906 European and 1931 indigenous censuses

Every table is extracted to a tidy CSV in `data-raw/colonial_census/csv/`,
with one row per cell of the printed table. The files are built into
`inst/extdata/colonial/*.parquet` and read by `load_colonial_census()`.

## Sources

| Code | Gallica ark | Document |
|---|---|---|
| `eur1906` | `bd6t53563851` | Dénombrement de la population européenne civile en Tunisie au 16 décembre 1906 (1907) |
| `ind1931` | `bpt6k994559s` | Dénombrement de la population civile indigène (musulmane et israélite) en Tunisie au 22 mars 1931 (1932) |

Page images: `data-raw/bnf_gallica/pages/<ark>/fNNNN.jpg` (NNNN = Gallica view).
OCR helper: `data-raw/colonial_census/ocr.py` (word positions from Gallica OCR).

## File naming

`<source>_<table>.csv`, e.g. `eur1906_t2_locality_nationality.csv`,
`ind1931_t3_cheikhat_nationality.csv`. Use lowercase snake_case.

## Columns (every file)

| Column | Content |
|---|---|
| `census` | `eur1906` or `ind1931` |
| `table_id` | Table number as printed: `I` … `VIII`, `IV_annex`, or a letter (`A`–`G`) for the 1906 analysis tables |
| `source_page` | Printed page number (integer). For a two-page spread, the page the cell is printed on |
| `gallica_view` | Gallica view number (`fNNNN`, integer) |
| geography columns | As applicable, from coarse to fine: `controle_civil`, `annexe`, `caidat`, `cheikhat`, `locality`, `commune`. Spelling **exactly as printed** (fix OCR errors, keep period orthography: `Souk-el-Arba`, `Medjez-el-Bab`). Leave empty when not applicable |
| dimension columns | One per printed dimension, English snake_case values (e.g. `nationality` = `french`, `italian`, `maltese`, `spanish`, `greek`, `other_european`; `sex` = `male`/`female`; `religion` = `muslim`/`jewish`). Add `<dim>_fr` with the label as printed (French) |
| `value` | Integer count (or numeric for rates/percentages; say which in the notes). `»` printed = 0 |
| `flag` | Empty, or one of `ocr_corrected` (value fixed by reading the image), `illegible` (value left NA), `total_mismatch` (row/column sums don't match the printed total even after checking the image; keep printed values), `derived_from_table_i` (cell lost in the binding, derived as the Table I total minus the visible cells), `not_applicable` (question not asked of this group, value NA) |

Do **not** store printed subtotal or total rows/columns as data rows, unless the
table only exists as totals. Use them to validate, and record the result in the
notes. Store a total row only when it carries information not recoverable by
summing (e.g. a contrôle total that includes units not itemised); then add a
dimension value such as `locality = "TOTAL (printed)"` and explain it.

## Validation (mandatory)

1. For every printed row total and every printed column total / "Totaux" /
   "à reporter" line, compare with the sum of the extracted cells.
2. Resolve every mismatch by reading the page image at full resolution
   (crop with PIL around the cell; the image is the ground truth, not the OCR).
3. Report: number of cells, number of checks made, checks passed, cells
   corrected from the image, remaining mismatches (should be 0 or explained).

## Notes file

For each CSV write `<same name>.md` next to it: title (French, plus English
translation), pages and views, what each column means, units, the validation
result, and any footnotes printed under the table (translated).
