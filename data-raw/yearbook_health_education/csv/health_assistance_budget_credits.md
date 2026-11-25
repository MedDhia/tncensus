# Dépenses du budget de l'Assistance publique : crédits par article

*Public assistance budget: credits (expenditure) by article (sgt1924–sgt1930).*

Source: *Statistique générale de la Tunisie*, chapter III (health and assistance), editions sgt1924, sgt1925, sgt1926, sgt1927, sgt1928, sgt1929, sgt1930. Source gallica.bnf.fr / BnF.

Pages and views of the stored values: sgt1924 (`bpt6k9105649x`): p. 48, f1038, p. 49, f1039, p. 50, f1040, p. 51, f1041; sgt1925 (`bpt6k9105650k`): p. 48, f72, p. 49, f73, p. 50, f74, p. 51, f75; sgt1926 (`bpt6k9105650k`): p. 57, f621, p. 58, f622, p. 59, f623; sgt1927 (`bpt6k91056510`): p. 56, f84, p. 57, f85, p. 58, f86, p. 59, f87; sgt1928 (`bpt6k91056510`): p. 56, f608, p. 57, f609, p. 58, f610, p. 59, f611, p. 61, f613; sgt1929 (`bpt6k9105652d`): p. 58, f86, p. 59, f87, p. 60, f88, p. 61, f89; sgt1930 (`bpt6k9105652d`): p. 61, f619, p. 62, f620, p. 63, f621.

Transcriptions: `../transcribed/health_finance_<edition>.txt`, sections `[budget_expenditure]`, `[complementary_allocations]`; rebuild with `python3 data-raw/yearbook_health_education/extract_health_finance.py build`. Per-check output: `health_finance_validation.json`.

Rows: 671. Years: 1924–1930. Unit of `value`: francs; amounts are as printed, centimes kept as decimals (printed » = 0).

Printed once per edition; all editions are kept (SPEC_ADDENDUM rule 5).

## Columns

- `census`: edition the value is taken from (`sgt1922` … `sgt1939`)
- `table_id`: transcription section the value comes from
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number (for a table over two pages, the page of the column group)
- `gallica_view`: Gallica view (fNNNN)
- `year`: year the value refers to (budget year, account year or calendar year; see below)
- `section_fr`: the last one or two headings printed above the line
- `article`: article number as printed (`-` = printed without a number; letters/prefixes added where the edition numbers sub-items or restarts numbering by section, see the transcription file)
- `line_type`: `article` (a budget line with its own amount) or `detail` (an amount printed in the label column breaking down the article above it; do not add details to articles)
- `line_fr`: budget line / article label as printed (ditto marks expanded)
- `line_en`: English code built from the French label (key words translated, place names kept)
- `measure`: what the value is (see below)
- `column_fr`: column heading as printed (French)
- `value`: francs; empty where the flag says so
- `flag`: empty, or `derived_from_totals`, `total_mismatch`, `not_applicable`, `illegible`, `reprint_corrected` (see below)

"Dépenses" of the public-assistance budget by article (sgt1924–sgt1930), for the edition's budget year. Column layouts change: sgt1924–sgt1925 one credit column (`credit`); sgt1926 credits on the lump-sum allocation (`credit_lump_sum_allocation`) and a complementary allocation (`credit_complementary_allocation`); sgt1927 Titre I (`credit_title_I`), Titre II from the reserve fund (`credit_title_II`) and Titre II from the complementary allocation on the 1926 surplus (`credit_title_II_complementary`); sgt1928–sgt1930 Titre I and Titre II. Printed Total columns and the "différence avec le budget de l'année précédente, en plus / en moins" columns are not stored (checked; the totals-line difference is cross-checked against the previous edition below). Amounts printed in the label column under an article (e.g. the elderly-care subsidies under "Vieillards et incurables") are stored as `line_type` = `detail`, `measure` = `credit_detail`; they break down the article and must not be added to it. "A reporter", section totals (sgt1930) and TOTAUX are not stored. sgt1928 adds "Allocations complémentaires à provenir des excédents de recettes de 1927" (table `complementary_allocations`, stored with `measure` = `credit`). The child-protection credit (one article) is broken down in `health_child_protection_credits`. sgt1930 prints the budget as I. Assistance publique (Dépenses d'État), II. Chapitre 1er (four sections) and a recapitulation; article numbers restart in each section and are stored with a section prefix (I.1, 1.III.31, …).

Identified misprints (printed value kept, `total_mismatch`): sgt1928 art. 3 (Aliénés) Titre II printed 194.100 (the total 272.000 and all later "A reporter" lines need 194.900; re-read on the image); sgt1928 art. 25 and sgt1929 art. 26 (Œuvre israélite des couvertures) Titre I printed 7.500 with a total of 7.000 (the "A reporter" lines need 7.000; confirmed on the OCR and the image); sgt1929 art. 3 Titre II 292.000 (272.000 needed); the printed totals of sgt1929 art. 18 (483.000 for 483.400) and art. 50 and 51 ("1.00", "637 60") are misprints too, but totals are not stored. Other failed checks are misprinted "A reporter" or TOTAUX lines (e.g. sgt1924: en moins 4.000 carried on page 49, 2.000 everywhere else; total 745.500 against articles summing to 745.450; sgt1927 Titre II TOTAUX 160.900 against 166.900 in the "A reporter" lines and the recapitulation).

## Remarks recorded in the transcriptions

- sgt1924: printed under the totals: "en plus : 186.400 fr." The article printed "9." before Union des Femmes de France is the eighth article (misnumbered; the next one is also "9.").
- sgt1925: The column heading reads "avec les crédits de 1924" on pages 48-49 and "de 1923" on pages 50-51. the "A reporter" line on page 49 and the "Reports" lines on pages 50 and 51 print no amounts except 10.000 (en moins) here printed under the totals: "en plus : 114.800 fr."
- sgt1926: printed under the totals: net difference "63.800" (crédits) and "95.000" (allocation complémentaire), together "158.800".
- sgt1927: The five lines under "2. Vieillards" carry, in the label column, 70.000, 8.000, 8.000, 75.000 and 5.000 (equal to their totals). Ferryville and Béja "en moins" carry call (1): "Subventions dont le rétablissement est subordonné à la production de comptes rendus réguliers". printed under the totals: En plus 474.900; En moins 52.000; En plus pour 1927: 422.900. Récapitulation printed below: Budget de 1926: Art. 14, § 1 = 924.100, Titre II = 94.000 (sic; 95.000 in the receipts), total 1.019.100; Budget de 1927: Art. 13, § 1 = 1.027.600, Titre II = 166.900 + 247.500 = 414.400, total 1.442.000; en plus 103.500, 319.400, 422.900.
- sgt1928: art. 25: Titre I printed 7.500, total printed 7.000; the "A reporter" lines are consistent with 7.000 in both columns, so the Titre I cell is the misprint. Two articles are numbered 46 (Gafsa and Legs Virieu); the second is stored as "46bis". printed under the totals: En plus 290.825; En moins 172.425; En plus pour 1928: 118.400. Récapitulation: Art. 13 § 1: 1.027.600 (1927), 1.164.100 (1928), +136.500; Titre II art. 1: 414.400, 396.300, -18.100; totals 1.442.000 and 1.560.400; "En plus au budget de 1928 ... 118.100" (sic; 118.400 above). Provenance des crédits complémentaires: Fonds de réserve au 15 décembre 1927 357.124,76; versement en 1928 au 5 % 39.205; total 396.329,76; crédits demandés 396.300; reste au fonds de réserve 29,76.
- sgt1929: The Report on page 60 prints Titre I as 1.125.500 (A reporter on page 59: 1.115.500). Béja and Mateur (israélite) lines are printed close together; the 250 and 750 are assigned to Béja (see notes). art. 47 total printed "1.0000", art. 50 total printed "1.00", art. 51 total printed "637 60", art. 52a en plus printed "30»000". Stored as 1000, 1000 (flagged), 637.60 (flagged), 30000.
- sgt1930: Kind "B" = printed subtotal of a section (the sum restarts after it). Article numbers restart in each section; they are stored with a section prefix (I.1 = Assistance publique art. 1; 1.I.1 = chapitre 1er, section I, art. 1, etc.). The "Reports" line on page 63 prints Titre I as 185.500 (A reporter on page 62: 187.500). Récapitulation du chapitre I « Assistance privée » (page 65): Section I 108.000 85.000 193.000 47.400 »; Section II 154.500 56.500 211.000 51.500 31.000; Section III 376.000 171.750 547.750 65.750 15.000; Section IV 82.300 280.000 362.300 121.800 13.000; total 720.800 593.250 1.314.050 286.450 59.000 (checked in the build).

## Validation

- Checks against printed totals: 395; passed: 367; failed: 28.

Failed checks (printed values kept, unless a flag below says otherwise; `L<n>` = line of the transcription file). See the commentary above for which ones were re-read on the page images and which are repeated identically in several printings:

  - sgt1924 budget_expenditure A reporter (line 64) col 2: cells give 2000, printed 4000
  - sgt1924 budget_expenditure TOTAUX (line 101) col 0: cells give 745450.0, printed 745500
  - sgt1927 budget_expenditure TOTAUX (line 82) col 1: cells give 166900, printed 160900
  - sgt1927 budget_expenditure TOTAUX (line 82): titles vs total: cells give 1436000, printed 1442000
  - sgt1928 budget_expenditure art 3 Aliénés : Placement d'aliénés dans les a: titles vs total: cells give 271200, printed 272000
  - sgt1928 budget_expenditure A reporter (line 33) col 1: cells give 284600, printed 285400
  - sgt1928 budget_expenditure art 25 Œuvre israélite des couvertures: titles vs total: cells give 7500, printed 7000
  - sgt1928 budget_expenditure A reporter (line 52) col 0: cells give 1015100, printed 1014600
  - sgt1928 budget_expenditure A reporter (line 52) col 1: cells give 369600, printed 370400
  - sgt1928 budget_expenditure A reporter (line 78) col 0: cells give 1122600, printed 1122100
  - sgt1928 budget_expenditure A reporter (line 78) col 1: cells give 379600, printed 380400
  - sgt1928 budget_expenditure TOTAUX (line 83) col 0: cells give 1164600.0, printed 1164100
  - sgt1928 budget_expenditure TOTAUX (line 83) col 1: cells give 395500, printed 396300
  - sgt1929 budget_expenditure art 3 Aliénés : Placement d'aliénés dans les a: titles vs total: cells give 292000, printed 272000
  - sgt1929 budget_expenditure A reporter (line 33) col 1: cells give 474600, printed 454600
  - sgt1929 budget_expenditure art 18 Crédits réservés, suivant le tableau de : titles vs total: cells give 483400, printed 483000
  - sgt1929 budget_expenditure art 26 Œuvre israélite des couvertures: titles vs total: cells give 7500, printed 7000
  - sgt1929 budget_expenditure A reporter (line 53) col 0: cells give 1116000, printed 1115500
  - sgt1929 budget_expenditure A reporter (line 53) col 1: cells give 528000, printed 508000
  - sgt1929 budget_expenditure A reporter (line 53) col 2: cells give 1623100, printed 1623500
  - sgt1929 budget_expenditure A reporter (line 75) col 0: cells give 1217500, printed 1217000
  - sgt1929 budget_expenditure A reporter (line 75) col 1: cells give 540250, printed 520250
  - sgt1929 budget_expenditure A reporter (line 75) col 2: cells give 1736850, printed 1737200
  - sgt1929 budget_expenditure A reporter (line 75): titles vs total: cells give 1737250, printed 1737200
  - sgt1929 budget_expenditure art 51 Legs Joséphine Virieu. — Dotation à une : titles vs total: cells give 637.5, printed 637.6
  - sgt1929 budget_expenditure TOTAUX (line 93) col 0: cells give 1344500.0, printed 1344000
  - sgt1929 budget_expenditure TOTAUX (line 93) col 1: cells give 710000, printed 690000
  - sgt1929 budget_expenditure TOTAUX (line 93) col 2: cells give 2033600.1, printed 2034000

- Flagged cells: not_applicable: 2, total_mismatch: 4.

  - sgt1925 1925 Première partie / a) Assistance médical / 4 / article / Tuberculeux / credit / Crédits alloués en 1925 = None (not_applicable)
  - sgt1926 1926 a) Assistance publique / 4 / article / Tuberculeux / credit_lump_sum_allocation / Crédits prélevés sur la dotation forfaitaire: crédits prévus pour 1926 = None (not_applicable)
  - sgt1928 1928 a) Assistance publique / 2. Vieillards et incurables / 3 / article / Aliénés : Placement d'aliénés dans les asiles de la Métropole / credit_title_II / Titre II, = 194100 (total_mismatch)
  - sgt1928 1928 d) Sociétés de Bienfaisance et Œuvres d'Assistance diverses / Tunis / 25 / article / Œuvre israélite des couvertures / credit_title_I / Titre I, art. 13, § 1 = 7500 (total_mismatch)
  - sgt1929 1929 a) Assistance publique / 2. Vieillards et incurables / 3 / article / Aliénés : Placement d'aliénés dans les asiles de la Métropole / credit_title_II / Titre II, = 292000 (total_mismatch)
  - sgt1929 1929 d) Sociétés de Bienfaisance et Œuvres d'Assistance diverses / Tunis / 26 / article / Œuvre israélite des couvertures / credit_title_I / Titre I, art. 13, § 1 = 7500 (total_mismatch)

## Cross-check of budget totals

The total of each budget year printed in the receipt series, the expenditure series, the receipts table and the credits table of every edition that prints it, and the printed difference with the previous budget (totals line) against the two totals: 81 comparisons, 76 equal.
  - 1919: receipts series TOTAUX (sgt1922) 252937.5 vs expenditure series TOTAUX (sgt1923) 238937.5
  - 1920: receipts series TOTAUX (sgt1922) 349700 vs expenditure series TOTAUX (sgt1923) 350700
  - 1926: receipts series TOTAUX (sgt1926) 924100 vs budget receipts TOTAUX (sgt1926) 1019100
  - 1926: receipts series TOTAUX (sgt1926) 924100 vs budget receipts TOTAUX (sgt1927) 1019100
  - 1926: receipts series TOTAUX (sgt1926) 924100 vs budget credits TOTAUX (sgt1926) 1019100

