# Répartition des condamnés d'après la nationalité, l'âge, le sexe et la catégorie pénale

*Condemned prisoners by nationality, age, sex and penal category.*

Source: *Statistique générale de la Tunisie*, chapter *Établissements pénitentiaires*, editions sgt1922, sgt1923, sgt1924, sgt1925, sgt1926, sgt1927, sgt1928, sgt1929, sgt1930, sgt1935, sgt1936, sgt1939. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views of the stored values: sgt1922 (`bpt6k9105649x`): p. 73, f97; sgt1923 (`bpt6k9105649x`): p. 79, f581; sgt1924 (`bpt6k9105649x`): p. 81, f1071; sgt1925 (`bpt6k9105650k`): p. 83, f107; sgt1926 (`bpt6k9105650k`): p. 93, f657; sgt1927 (`bpt6k91056510`): p. 91, f119; sgt1928 (`bpt6k91056510`): p. 91, f643; sgt1929 (`bpt6k9105652d`): p. 93, f121; sgt1930 (`bpt6k9105652d`): p. 97, f655; sgt1935 (`bpt6k9105653t`): p. 63, f83; sgt1936 (`bpt6k91056547`): p. 47, f58; sgt1939 (`bpt6k9105739w`): p. 47, f53.

Transcriptions: `../transcribed/prisons_<edition>.txt`; rebuild with `python3 data-raw/yearbook_other_chapters/extract_prisons.py build`.

Rows: 1551. Years: 1922, 1923, 1924, 1925, 1926, 1927, 1928, 1929, 1930, 1935, 1936, 1939.

Unit: persons (condemned prisoners; the printed tables do not say at which date they are counted).

Printed once per edition for the edition year (SPEC_ADDENDUM rule 5): every edition is kept, with `year`; no year is printed by two editions.

## Columns

- `census`: edition the value is taken from (`sgt1922` … `sgt1939`)
- `table_id`: transcription section name (`condemned_age`); printed as table a) up to sgt1935, without a letter in sgt1936 and sgt1939
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number
- `gallica_view`: Gallica view (fNNNN)
- `year`: year of the figures (the edition year: each edition prints the table for its own year)
- `nationality`: `french`, `algerian`, `italian`, `maltese`, `greek`, `spanish`, `serbian`, `danish`, `other_european`, `tunisian_muslim`, `tunisian_jewish`, `tripolitanian`, `moroccan`, `other`
- `nationality_fr`: line label as printed
- `breakdown`: `age`, `sex` or `penal_category`: the table splits the same prisoners three ways, so each breakdown sums to the prisoners of the nationality
- `category`: `age_0_10` … `age_51_plus`, `male`, `female`, `first_offender` (*primaires*), `recidivist` (*récidivistes*)
- `category_fr`: printed column heading
- `value`: number of condemned prisoners
- `flag`: empty, `ocr_corrected`, `illegible`, `total_mismatch`, `not_applicable` (SPEC.md)

Printed once per edition, for the edition year: a) on the first page of the chapter (sgt1922-sgt1935); first table of the prisons pages inside chapter IV *Justice* in sgt1936 and sgt1939. The printed "Total par nationalité" column, the age "Total" column (printed sgt1922-sgt1926 only) and the "Totaux" line are not stored; they are the checks.

Nationality lines change between editions: sgt1922-sgt1924 print "— (Algériens)" (under Français), "Anglais (Maltais)", Serbes (sgt1922) or Danois (sgt1923-sgt1924), and the Tunisian subjects under a brace labelled "sujet musulmans" (as printed: Musulmans / Israélites); sgt1925 prints Anglo-Maltais and has no Grecs, Espagnols or Autres européens lines; from sgt1926 the lines are fixed (Tunisiens musulmans / israélites). A nationality not printed in an edition has no rows for it.

Checks on every line, Totaux included: sum of the seven age groups = total; age "Total" column = sum of the age groups (sgt1922-sgt1926); male + female = total; primaires + récidivistes = total; and every column against the Totaux line.

Failures that involve only printed totals (no stored cell flagged): sgt1928 Tripolitains, "Total par nationalité" printed 192 where the ages, the sexes and the penal categories all give 198 and the Totaux line (8.282) needs 198; sgt1930 Totaux, "51 ans et au-dessus" printed 397 for lines summing to 387, while the Totaux line's own total 7.828 agrees with 387 (the lines' sums of ages all match their totals); sgt1922 Totaux, ages summing to 8.224 for 8.227, which is the Italiens shortfall of 3 carried into the total line.

Every cell of every edition was read on the native-resolution page image (crops of the whole table), and each failing line re-read on a separate crop.

Cells flagged `total_mismatch` (printed value kept, re-read on a native-resolution crop): sgt1922: Italiens / age_0_10, Italiens / age_11_15, Italiens / age_16_20, Italiens / age_21_30, Italiens / age_31_40, Italiens / age_41_50, Italiens / age_51_plus (the seven age groups sum to 141, the printed total, the sex and the penal-category columns to 144; the age-group column totals agree with the lines, so the shortfall of 3 is in the printing of this line); sgt1929: Français / male (35 men and 0 women for a printed total of 34 (the ages sum to 34) and the men column sums to 7.655 for a printed 7.654: the 35 is one too many); sgt1929: Français / first_offender, Français / recidivist, Algériens / first_offender, Algériens / recidivist, Italiens / first_offender, Italiens / recidivist, Maltais / first_offender, Maltais / recidivist, Grecs / first_offender, Grecs / recidivist, Tunisiens israélites / first_offender, Tunisiens israélites / recidivist, Marocains / first_offender, Marocains / recidivist, Tripolitains / first_offender, Tripolitains / recidivist, Divers / first_offender, Divers / recidivist (primaires + récidivistes do not give the line total on nine of the twelve lines and the two columns do not sum to their printed totals (4.109 for 4.035, 3.692 for 3.795); several of these cells repeat sgt1928's (Français 22 / 19, Algériens and Italiens primaires 89 and 91, Divers récidivistes 38)).

## Validation

- Checks against printed totals and identities: 670; passed: 647; failed: 23.

Failed checks (printed values kept; every failure was re-read on a native-resolution crop, or recurs unchanged in another edition's printing of the same cells):

  - sgt1922 p.73 (f97) condemned_age Italiens: total = age_0_10 + age_11_15 + age_16_20 + age_21_30 + age_31_40 + age_41_50 + age_51_plus: cells give 141, printed 144 (difference 3)
  - sgt1922 p.73 (f97) condemned_age Totaux: total = age_0_10 + age_11_15 + age_16_20 + age_21_30 + age_31_40 + age_41_50 + age_51_plus: cells give 8224, printed 8227 (difference 3)
  - sgt1922 p.73 (f97) condemned_age Italiens: age_total = age_0_10 + age_11_15 + age_16_20 + age_21_30 + age_31_40 + age_41_50 + age_51_plus: cells give 141, printed 144 (difference 3)
  - sgt1922 p.73 (f97) condemned_age Totaux: age_total = age_0_10 + age_11_15 + age_16_20 + age_21_30 + age_31_40 + age_41_50 + age_51_plus: cells give 8224, printed 8227 (difference 3)
  - sgt1928 p.91 (f643) condemned_age Tripolitains: total = age_0_10 + age_11_15 + age_16_20 + age_21_30 + age_31_40 + age_41_50 + age_51_plus: cells give 198, printed 192 (difference -6)
  - sgt1928 p.91 (f643) condemned_age Tripolitains: total = male + female: cells give 198, printed 192 (difference -6)
  - sgt1928 p.91 (f643) condemned_age Tripolitains: total = first_offender + recidivist: cells give 198, printed 192 (difference -6)
  - sgt1928 p.91 (f643) condemned_age total: lines vs Totaux: cells give 8276, printed 8282 (difference 6)
  - sgt1929 p.93 (f121) condemned_age Français: total = male + female: cells give 35, printed 34 (difference -1)
  - sgt1929 p.93 (f121) condemned_age Français: total = first_offender + recidivist: cells give 41, printed 34 (difference -7)
  - sgt1929 p.93 (f121) condemned_age Algériens: total = first_offender + recidivist: cells give 141, printed 72 (difference -69)
  - sgt1929 p.93 (f121) condemned_age Italiens: total = first_offender + recidivist: cells give 144, printed 96 (difference -48)
  - sgt1929 p.93 (f121) condemned_age Maltais: total = first_offender + recidivist: cells give 20, printed 14 (difference -6)
  - sgt1929 p.93 (f121) condemned_age Grecs: total = first_offender + recidivist: cells give 2, printed 1 (difference -1)
  - sgt1929 p.93 (f121) condemned_age Tunisiens israélites: total = first_offender + recidivist: cells give 60, printed 57 (difference -3)
  - sgt1929 p.93 (f121) condemned_age Marocains: total = first_offender + recidivist: cells give 27, printed 24 (difference -3)
  - sgt1929 p.93 (f121) condemned_age Tripolitains: total = first_offender + recidivist: cells give 189, printed 365 (difference 176)
  - sgt1929 p.93 (f121) condemned_age Divers: total = first_offender + recidivist: cells give 77, printed 67 (difference -10)
  - sgt1929 p.93 (f121) condemned_age male: lines vs Totaux: cells give 7655, printed 7654 (difference -1)
  - sgt1929 p.93 (f121) condemned_age first_offender: lines vs Totaux: cells give 4109, printed 4035 (difference -74)
  - sgt1929 p.93 (f121) condemned_age recidivist: lines vs Totaux: cells give 3692, printed 3795 (difference 103)
  - sgt1930 p.97 (f655) condemned_age Totaux: total = age_0_10 + age_11_15 + age_16_20 + age_21_30 + age_31_40 + age_41_50 + age_51_plus: cells give 7838, printed 7828 (difference -10)
  - sgt1930 p.97 (f655) condemned_age age_51_plus: lines vs Totaux: cells give 387, printed 397 (difference 10)

- Overlapping printings: 0 cell comparisons with other editions printing the same cell; 0 differences.

- Flagged cells: total_mismatch: 26.

  - sgt1922 p.73 1922 italian / age / age_0_10 = 0 (total_mismatch)
  - sgt1922 p.73 1922 italian / age / age_11_15 = 0 (total_mismatch)
  - sgt1922 p.73 1922 italian / age / age_16_20 = 20 (total_mismatch)
  - sgt1922 p.73 1922 italian / age / age_21_30 = 64 (total_mismatch)
  - sgt1922 p.73 1922 italian / age / age_31_40 = 26 (total_mismatch)
  - sgt1922 p.73 1922 italian / age / age_41_50 = 13 (total_mismatch)
  - sgt1922 p.73 1922 italian / age / age_51_plus = 18 (total_mismatch)
  - sgt1929 p.93 1929 french / sex / male = 35 (total_mismatch)
  - sgt1929 p.93 1929 french / penal_category / first_offender = 22 (total_mismatch)
  - sgt1929 p.93 1929 french / penal_category / recidivist = 19 (total_mismatch)
  - sgt1929 p.93 1929 algerian / penal_category / first_offender = 89 (total_mismatch)
  - sgt1929 p.93 1929 algerian / penal_category / recidivist = 52 (total_mismatch)
  - sgt1929 p.93 1929 italian / penal_category / first_offender = 91 (total_mismatch)
  - sgt1929 p.93 1929 italian / penal_category / recidivist = 53 (total_mismatch)
  - sgt1929 p.93 1929 maltese / penal_category / first_offender = 12 (total_mismatch)
  - sgt1929 p.93 1929 maltese / penal_category / recidivist = 8 (total_mismatch)
  - sgt1929 p.93 1929 greek / penal_category / first_offender = 1 (total_mismatch)
  - sgt1929 p.93 1929 greek / penal_category / recidivist = 1 (total_mismatch)
  - sgt1929 p.93 1929 tunisian_jewish / penal_category / first_offender = 28 (total_mismatch)
  - sgt1929 p.93 1929 tunisian_jewish / penal_category / recidivist = 32 (total_mismatch)
  - sgt1929 p.93 1929 moroccan / penal_category / first_offender = 16 (total_mismatch)
  - sgt1929 p.93 1929 moroccan / penal_category / recidivist = 11 (total_mismatch)
  - sgt1929 p.93 1929 tripolitanian / penal_category / first_offender = 97 (total_mismatch)
  - sgt1929 p.93 1929 tripolitanian / penal_category / recidivist = 92 (total_mismatch)
  - sgt1929 p.93 1929 other / penal_category / first_offender = 39 (total_mismatch)
  - sgt1929 p.93 1929 other / penal_category / recidivist = 38 (total_mismatch)

## Image versus OCR

- Read cell by cell on the page images (12 printings): sgt1922 f97, sgt1923 f581, sgt1924 f1071, sgt1925 f107, sgt1926 f657, sgt1927 f119, sgt1928 f643, sgt1929 f121, sgt1930 f655, sgt1935 f83, sgt1936 f58, sgt1939 f53.
- Drafted from the Gallica OCR and accepted on the checks above, with every failing check and every unclear OCR token re-read on a native-resolution crop (0 printings): none.
- Cells whose image reading differs from the OCR (flag `ocr_corrected`): 0.
