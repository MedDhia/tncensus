# Foreigners' arrivals and departures by nationality, 1920-1939

Source: *Statistique générale de la Tunisie*, Régence de Tunis (annual). Source gallica.bnf.fr / Ministère des Affaires étrangères (NoC-CR). Editions and views: see `EDITIONS.md`.

*Mouvement des étrangers en Tunisie, entrées et sorties*: foreigners' arrivals and
departures by nationality, 1920-1939. 1715 rows: one per year, movement and
nationality. Each cell is taken from the latest edition that prints it (`census`).

Columns: `year`, `movement` (`arrivals` / `departures`), `nationality` (English code;
`british_anglo_maltese` = *Anglais et Anglo-Maltais*; `american` = *Américains*, from 1936
*Américains (Nord et Sud)*; `other` = *Autres*), `nationality_fr` (as printed), `value` =
persons. A footnote in the 1929 and 1930 editions says that for 1923-1926 the figures are
declarations of residence (men and women, children excluded). In 1933 Serbs are printed
as "compris dans les Yougoslaves" and Tripolitanians as "compris dans les Italiens":
`value` NA, flag `not_applicable`.

## Sources used

- sgt1929 (pp. 26, view 54): 1920 (and 1921-1923, compared).
- sgt1930 (pp. 26-27, views 584-585): 1921-1930; latest printing of
  1921-1925 and of the 1929 departures (which are in the binding of sgt1935).
- sgt1935 (pp. 16-17, views 36-37): 1926-1935; latest printing of 1926-1931, and of
  1932-1934 for the nationalities that the 1936 edition no longer lists.
- sgt1936 (p. 14, view 25): 1932-1936; latest printing of 1932-1934 where it lists the
  nationality.
- sgt1939 (p. 14, view 20): 1935-1939.

From 1936 the table lists 32 nationalities instead of 46: rows such as Albanians,
Argentines, Armenians, Brazilians, Chinese, Japanese, Latvians, Lebanese, Mexicans,
Persians and Serbs disappear, but the printed totals still include them; so the 1936 and
1939 editions' rows do not add up to their own totals (see Validation).

## Comparison of the overlapping printings

1014 comparisons, 1014 equal, 0 different:


## Not covered (open issues)

- **1917-1919, and the 1925-1928 editions.** The 1926, 1927 and 1928 editions print
  1917-1926, 1918-1927 and 1919-1928. Their first columns carry the figures that the
  1929 and 1930 editions print for 1921 and later (e.g. sgt1926's "1917" = 3.388
  arrivals and 2.302 departures, Italians 2.948 / 1.850, exactly sgt1930's 1921), so the
  year labels of one set of editions are wrong. Until the 1926-1928 tables are
  transcribed in full and the labels resolved, 1917-1919 are left out and those
  editions are not compared. The 1925 edition (1925 only, with separate rows for
  *Anglais* and *Anglo-Maltais*) is not compared either; its totals (2.233 / 1.052)
  equal sgt1930's 1925.

## Validation

22 of 66 printed-total checks pass. Failing checks (each re-read on the image at full resolution; printed values kept):

- sgt1929 1920 arrivals column total: computed 4506 != printed 4505
- sgt1929 1922 arrivals column total: computed 4805 != printed 4830
- sgt1929 1922 departures column total: computed 3116 != printed 3126
- sgt1929 1923 arrivals column total: computed 2729 != printed 2718
- sgt1930 1922 arrivals column total: computed 4805 != printed 4830
- sgt1930 1922 departures column total: computed 3116 != printed 3126
- sgt1930 1923 arrivals column total: computed 2729 != printed 2718
- sgt1930 1924 arrivals column total: computed 2533 != printed 2534
- sgt1930 1925 arrivals column total: computed 2230 != printed 2233
- sgt1930 1925 departures column total: computed 1051 != printed 1052
- sgt1930 1926 arrivals column total: computed 2956 != printed 3562
- sgt1930 1926 departures column total: computed 1230 != printed 1235
- sgt1930 1927 arrivals column total: computed 2522 != printed 2525
- sgt1930 1927 departures column total: computed 1210 != printed 1212
- sgt1930 1928 arrivals column total: computed 13443 != printed 13234
- sgt1930 1929 arrivals column total: computed 15122 != printed 15222
- sgt1930 1930 departures column total: computed 14317 != printed 14257
- sgt1935 1926 arrivals column total: computed 2956 != printed 3562
- sgt1935 1926 departures column total: computed 1230 != printed 1235
- sgt1935 1927 arrivals column total: computed 2522 != printed 2525
- sgt1935 1927 departures column total: computed 1210 != printed 1212
- sgt1935 1928 arrivals column total: computed 13443 != printed 13234
- sgt1935 1929 arrivals column total: computed 15122 != printed 15222
- sgt1935 1930 departures column total: computed 14317 != printed 14257
- sgt1935 1931 arrivals column total: computed 19546 != printed 55302
- sgt1935 1931 departures column total: computed 15723 != printed 44482
- sgt1935 1933 departures column total: computed 2023 != printed 2018
- sgt1935 1934 arrivals column total: computed 2644 != printed 2639
- sgt1935 1934 departures column total: computed 1959 != printed 1955
- sgt1936 1932 arrivals column total: computed 14932 != printed 14946
- sgt1936 1932 departures column total: computed 14311 != printed 14319
- sgt1936 1933 arrivals column total: computed 3798 != printed 3820
- sgt1936 1933 departures column total: computed 2014 != printed 2018
- sgt1936 1934 arrivals column total: computed 2610 != printed 2639
- sgt1936 1934 departures column total: computed 1941 != printed 1955
- sgt1936 1935 arrivals column total: computed 1837 != printed 1866
- sgt1936 1935 departures column total: computed 2178 != printed 2207
- sgt1936 1936 arrivals column total: computed 1761 != printed 1765
- sgt1936 1936 departures column total: computed 2248 != printed 2263
- sgt1939 1935 arrivals column total: computed 1837 != printed 1866
- sgt1939 1935 departures column total: computed 2178 != printed 2207
- sgt1939 1936 arrivals column total: computed 1761 != printed 1765
- sgt1939 1936 departures column total: computed 2248 != printed 2263
- sgt1939 1937 arrivals column total: computed 1777 != printed 1787

Common columns: `census` (source edition, e.g. `sgt1930`), `gallica_ark` (volume ark), `table_id`, `source_page` (printed page), `gallica_view`, `value`, `flag` (empty, `ocr_corrected`, `illegible`, `total_mismatch`, `derived_from_totals`, `not_applicable`, `reprint_corrected`; see `data-raw/colonial_census/SPEC.md`). A printed `»` is stored as 0. Printed totals are not stored; they were used for validation.
