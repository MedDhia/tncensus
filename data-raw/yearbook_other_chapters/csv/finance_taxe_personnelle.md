# Taxe personnelle. Etat des contribuables imposés à la taxe personnelle

*Personal tax (taxe personnelle): taxpayers by caïdat and nationality.*

Source: *Statistique générale de la Tunisie*, chapter *Finances*, editions sgt1922, sgt1923, sgt1924, sgt1925, sgt1926, sgt1927, sgt1928, sgt1929, sgt1930. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views of the stored values: sgt1922 (`bpt6k9105649x`): p. 163, f187; sgt1923 (`bpt6k9105649x`): p. 175, f677; sgt1924 (`bpt6k9105649x`): p. 183, f1173; sgt1925 (`bpt6k9105650k`): p. 194, f218; sgt1926 (`bpt6k9105650k`): p. 210, f774; sgt1927 (`bpt6k91056510`): p. 208, f236; sgt1928 (`bpt6k91056510`): p. 208, f760; sgt1929 (`bpt6k9105652d`): p. 210, f238; sgt1930 (`bpt6k9105652d`): p. 214, f772.

Transcriptions: `../transcribed/finance_<edition>.txt`; rebuild with `python3 data-raw/yearbook_other_chapters/extract_finance.py build`.

Rows: 1977. Years: 1922, 1923, 1924, 1925, 1926, 1927, 1928, 1929, 1930.

Unit: number of taxpayers (contribuables imposés); value_type: count.

Printed once per edition, each printing for its own period (cumulative to a later year, or another tax year): every edition is kept (SPEC_ADDENDUM rule 5); `census` is the edition, `year` the year the printing refers to.

## Columns

- `census`: edition (source code; every edition printing the table is kept, rule 5)
- `table_id`: transcription section
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number
- `gallica_view`: Gallica view (fNNNN)
- `year`: year of the roll (no year printed: the edition year)
- `region`: région as printed (sgt1925 on; "Territoires militaires du Sud" for the southern caïdats); empty when the table lists caïdats only
- `controle_civil`: contrôle civil as printed (sgt1925 on); empty when the table lists caïdats only
- `caidat`: caïdat as printed; two caïdats joined by ", " = a figure printed once for both (bracket)
- `nationality`: nationality of the taxpayers: `french`, `italian`, `british_maltese` (Anglais et Maltais), `spanish`, `greek`, `other_european`, `tunisian` (sujets tunisiens)
- `nationality_fr`: printed column head
- `value`: number of taxpayers (contribuables imposés)
- `flag`: empty, or `ocr_corrected` (image reading differs from the Gallica OCR), `total_mismatch` (printed value kept; identified by a failed check as the faulty cell, see Validation), `illegible` (value NA), `not_applicable` (nothing printed, value NA), `derived_from_totals` (digits hidden in the binding; value = the printed row total minus the other cells of the row, see the notes)

Printed in every edition sgt1922-sgt1930 (not from sgt1935): one page in sgt1922-sgt1924 ("Etat des contribuables imposés à la taxe personnelle", caïdats only), a two-page spread from sgt1925 (by région, contrôle civil and caïdat; "soumis à" from sgt1926). No year is printed: `year` is the edition year. The list of caïdats changes (Djerba from sgt1923, Djebeniana from sgt1927, Tatahouine from sgt1928; sgt1922-sgt1924 bracket Ouled-Aoun and Ouled-Ayar, with the European columns and the Total printed once for both and the Sujets tunisiens separately: stored as caïdat "Ouled-Aoun, Ouled-Ayar" for the European nationalities and under each caïdat for the Tunisians).

Columns stored: Français, Italiens, Anglais et Maltais, Espagnols, Grecs, Autres Européens, Sujets tunisiens. Total des Européens, Total and the Totaux line are checks, not stored.

Failed checks, each re-read on zoomed native-resolution crops. sgt1930 La Skhira: Français printed 49 (legible on both sides of the gutter), the Total des Européens 56, the Total 7.667 and the Totaux of the Français column (24.490) all require 40: the Français cell is flagged `total_mismatch` (printed value kept). Misprinted check figures, no stored cell involved: sgt1925 Total of Zaghouan printed 11.166 for 11.156 and of L'Arad 18.504 for 18.514 (the two errors cancel in the Totaux); sgt1929 Total of Sfax printed 26.350 for 26.530 (the Totaux 623.943 is right).

Survey of the whole chapter in every edition: `finance_survey.md`.

## Validation

- Checks against printed totals and identities: 663; passed: 657; failed: 6.

Failed checks (printed values kept; every failure was re-read on a native-resolution crop, or recurs unchanged in another edition's printing of the same cells):

  - sgt1925 p.194 (f218) taxe 2me Région ; Zaghouan ; Zaghouan: Total = Européens + Sujets tunisiens: cells give 11156, printed 11166 (difference 10)
  - sgt1925 p.194 (f218) taxe 5me Région ; Gabès ; L'Arad: Total = Européens + Sujets tunisiens: cells give 18514, printed 18504 (difference -10)
  - sgt1929 p.210 (f238) taxe 5me Région ; Sfax ; Sfax: Total = Européens + Sujets tunisiens: cells give 26530, printed 26350 (difference -180)
  - sgt1929 p.210 (f238) taxe Totaux tot: Totaux = sum of the lines: cells give 623763, printed 623943 (difference 180)
  - sgt1930 p.214 (f772) taxe 5me Région ; Sfax ; La Skhira: Total des Européens = six nationalities: cells give 65, printed 56 (difference -9)
  - sgt1930 p.214 (f772) taxe Totaux fr: Totaux = sum of the lines: cells give 24499, printed 24490 (difference -9)

- Overlapping printings: 0 cell comparisons with other editions printing the same cell; 0 differences.

- Flagged cells: ocr_corrected: 79, total_mismatch: 1.

  - sgt1922 p.163 1922  /  / Djérid / tunisian = 9408 (ocr_corrected)
  - sgt1922 p.163 1922  /  / Kef / tunisian = 15263 (ocr_corrected)
  - sgt1922 p.163 1922  /  / Nefzaoua / tunisian = 8828 (ocr_corrected)
  - sgt1923 p.175 1923  /  / L'Arad / french = 168 (ocr_corrected)
  - sgt1923 p.175 1923  /  / Kef / tunisian = 14668 (ocr_corrected)
  - sgt1923 p.175 1923  /  / Souk-el-Arba / tunisian = 23998 (ocr_corrected)
  - sgt1924 p.183 1924  /  / L'Arad / italian = 80 (ocr_corrected)
  - sgt1924 p.183 1924  /  / Mateur / french = 284 (ocr_corrected)
  - sgt1924 p.183 1924  /  / Monastir / british_maltese = 41 (ocr_corrected)
  - sgt1924 p.183 1924  /  / Sousse / tunisian = 29451 (ocr_corrected)
  - sgt1924 p.183 1924  /  / Tunis et Banlieue / french = 8470 (ocr_corrected)
  - sgt1924 p.183 1924  /  / Tunis et Banlieue / british_maltese = 2225 (ocr_corrected)
  - sgt1925 p.194 1925 1re Région / Béja / Béja / french = 384 (ocr_corrected)
  - sgt1925 p.194 1925 1re Région / Bizerte / Mateur / french = 300 (ocr_corrected)
  - sgt1925 p.194 1925 1re Région / Tabarka / Aïn-Draham / french = 291 (ocr_corrected)
  - sgt1925 p.194 1925 1re Région / Souk-el-Arba / Souk-el-Arba / french = 355 (ocr_corrected)
  - sgt1925 p.194 1925 1re Région / Souk-el-Arba / Souk-el-Arba / tunisian = 24433 (ocr_corrected)
  - sgt1925 p.194 1925 2me Région / Tunis / Banlieue / french = 9943 (ocr_corrected)
  - sgt1925 p.194 1925 5me Région / Sfax / La Skhira / tunisian = 7422 (ocr_corrected)
  - sgt1925 p.194 1925 5me Région / Gabès / L'Arad / french = 167 (ocr_corrected)
  - sgt1926 p.210 1926 1re Région / Béja / Béja / italian = 441 (ocr_corrected)
  - sgt1926 p.210 1926 1re Région / Béja / Béja / tunisian = 18168 (ocr_corrected)
  - sgt1926 p.210 1926 1re Région / Bizerte / Bizerte / italian = 1323 (ocr_corrected)
  - sgt1926 p.210 1926 1re Région / Bizerte / Bizerte / tunisian = 16509 (ocr_corrected)
  - sgt1926 p.210 1926 1re Région / Bizerte / Mateur / french = 282 (ocr_corrected)
  - sgt1926 p.210 1926 1re Région / Tabarka / Aïn-Draham / italian = 216 (ocr_corrected)
  - sgt1926 p.210 1926 1re Région / Souk-el-Arba / Souk-el-Arba / italian = 355 (ocr_corrected)
  - sgt1926 p.210 1926 2me Région / Tunis / Banlieue / spanish = 67 (ocr_corrected)
  - sgt1926 p.210 1926 2me Région / Tunis / Banlieue / other_european = 625 (ocr_corrected)
  - sgt1926 p.210 1926 2me Région / Tunis / Banlieue / tunisian = 45726 (ocr_corrected)
  - sgt1926 p.210 1926 2me Région / Zaghouan / Zaghouan / italian = 423 (ocr_corrected)
  - sgt1926 p.210 1926 2me Région / Grombalia / Cap Bon / italian = 972 (ocr_corrected)
  - sgt1926 p.210 1926 2me Région / Grombalia / Cap Bon / greek = 6 (ocr_corrected)
  - sgt1926 p.210 1926 3me Région / Le Kef / Tadjerouine / italian = 849 (ocr_corrected)
  - sgt1926 p.210 1926 3me Région / Le Kef / Tadjerouine / spanish = 6 (ocr_corrected)
  - sgt1926 p.210 1926 3me Région / Mactar / Oulad Ayar / tunisian = 9694 (ocr_corrected)
  - sgt1926 p.210 1926 4me Région / Sousse / Mahdia / french = 78 (ocr_corrected)
  - sgt1926 p.210 1926 4me Région / Sousse / Monastir / spanish = 6 (ocr_corrected)
  - sgt1926 p.210 1926 5me Région / Sfax / La Skhira / french = 9 (ocr_corrected)
  - sgt1926 p.210 1926 5me Région / Sfax / La Skhira / tunisian = 7549 (ocr_corrected)
  - sgt1926 p.210 1926 5me Région / Sfax / Sfax / other_european = 56 (ocr_corrected)
  - sgt1926 p.210 1926 5me Région / Gabès / L'Arad / tunisian = 19681 (ocr_corrected)
  - sgt1926 p.210 1926 5me Région / Gafsa / Hemmama / italian = 104 (ocr_corrected)
  - sgt1926 p.210 1926 5me Région / Gafsa / Hemmama / tunisian = 16156 (ocr_corrected)
  - sgt1926 p.210 1926 5me Région / Gafsa / Gafsa / italian = 458 (ocr_corrected)
  - sgt1926 p.210 1926 Territoires militaires du Sud /  / Ouerghema / french = 63 (ocr_corrected)
  - sgt1927 p.208 1927 1re Région / Bizerte / Bizerte / italian = 1306 (ocr_corrected)
  - sgt1927 p.208 1927 2me Région / Tunis-Ville et banlieue / Banlieue / french = 12730 (ocr_corrected)
  - sgt1927 p.208 1927 2me Région / Zaghouan / Zaghouan / french = 498 (ocr_corrected)
  - sgt1927 p.208 1927 2me Région / Grombalia / Cap Bon / french = 404 (ocr_corrected)
  - sgt1927 p.208 1927 3me Région / Téboursouk / Téboursouk / italian = 128 (ocr_corrected)
  - sgt1927 p.208 1927 3me Région / Mactar / Oulad Aoun / french = 28 (ocr_corrected)
  - sgt1927 p.208 1927 5me Région / Sfax / Sfax / other_european = 61 (ocr_corrected)
  - sgt1927 p.208 1927 5me Région / Gabès / L'Arad / french = 181 (ocr_corrected)
  - sgt1927 p.208 1927 5me Région / Gafsa / Gafsa / french = 566 (ocr_corrected)
  - sgt1928 p.208 1928 1re Région / Béja / Béja / french = 427 (ocr_corrected)
  - sgt1928 p.208 1928 1re Région / Bizerte / Bizerte / italian = 1344 (ocr_corrected)
  - sgt1928 p.208 1928 1re Région / Bizerte / Mateur / french = 315 (ocr_corrected)
  - sgt1928 p.208 1928 1re Région / Tabarka / Aïn-Draham / french = 236 (ocr_corrected)
  - sgt1928 p.208 1928 1re Région / Souk-el-Arba / Souk-el-Arba / french = 426 (ocr_corrected)
  - sgt1928 p.208 1928 2me Région / Tunis-Ville et banlieue / Banlieue / french = 12393 (ocr_corrected)
  - sgt1928 p.208 1928 2me Région / Zaghouan / Zaghouan / french = 492 (ocr_corrected)
  - sgt1928 p.208 1928 2me Région / Grombalia / Cap Bon / french = 415 (ocr_corrected)
  - sgt1928 p.208 1928 5me Région / Sfax / Djebeniana / tunisian = 11787 (ocr_corrected)
  - sgt1929 p.210 1929 1re Région / Bizerte / Bizerte / italian = 1395 (ocr_corrected)
  - sgt1929 p.210 1929 2me Région / Tunis-Ville et banlieue / Banlieue / french = 13689 (ocr_corrected)
  - sgt1929 p.210 1929 2me Région / Grombalia / Cap Bon / french = 406 (ocr_corrected)
  - sgt1929 p.210 1929 2me Région / Grombalia / Cap Bon / tunisian = 34197 (ocr_corrected)
  - sgt1929 p.210 1929 3me Région / Téboursouk / Téboursouk / french = 415 (ocr_corrected)
  - sgt1929 p.210 1929 4me Région / Thala / Fraichiches-Majeurs / french = 174 (ocr_corrected)
  - sgt1929 p.210 1929 5me Région / Sfax / Sfax / french = 1082 (ocr_corrected)
  - sgt1929 p.210 1929 5me Région / Gabès / L'Arad / tunisian = 18181 (ocr_corrected)
  - sgt1930 p.214 1930 1re Région / Bizerte / Bizerte / italian = 1356 (ocr_corrected)
  - sgt1930 p.214 1930 2me Région / Tunis-Ville et banlieue / Banlieue / french = 13701 (ocr_corrected)
  - sgt1930 p.214 1930 3me Région / Le Kef / Le Kef / french = 390 (ocr_corrected)
  - sgt1930 p.214 1930 3me Région / Medjez-el-Bab / Medjez-el-Bab / french = 665 (ocr_corrected)
  - sgt1930 p.214 1930 4me Région / Sousse / Sousse / french = 1189 (ocr_corrected)
  - sgt1930 p.214 1930 4me Région / Kairouan / Djelass / french = 129 (ocr_corrected)
  - sgt1930 p.214 1930 5me Région / Sfax / La Skhira / french = 49 (total_mismatch)
  - sgt1930 p.214 1930 5me Région / Gafsa / Hemmama / italian = 41 (ocr_corrected)

## Image versus OCR

- Read cell by cell on the page images (9 printings): sgt1922 f187, sgt1923 f677, sgt1924 f1173, sgt1925 f218, sgt1926 f774, sgt1927 f236, sgt1928 f760, sgt1929 f238, sgt1930 f772.
- Drafted from the Gallica OCR and accepted on the checks above, with every failing check and every unclear OCR token re-read on a native-resolution crop (0 printings): none.
- Cells whose image reading differs from the OCR (flag `ocr_corrected`): 79.
