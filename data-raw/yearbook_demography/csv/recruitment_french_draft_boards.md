# Opérations des Conseils de révision (recrutement français)

Source: *Statistique générale de la Tunisie*, Régence de Tunis (annual). Source gallica.bnf.fr / Ministère des Affaires étrangères (NoC-CR). Editions and views: see `EDITIONS.md`.

*Opérations des Conseils de révision (recrutement français)*: 304 rows, conscription class (classe)s 1902-1939, one row per conscription and item.
Each value is taken from the latest transcribed edition that prints it (`census`).
Columns: `year` (conscription class (classe)), `item` (English code), `item_fr` (printed heading), `value`.

Check per class (1915 onwards): actually called = registered - exempted - neo-French not called - postponed - deferred - enlisted. The third column means *hommes qui, en raison de leur âge, n'ont pas été appelés* before 1913 and *néo-français* later; the pre-1915 classes do not follow the identity and are not checked. Each class is printed in many editions (1913-1915, for example, in every edition from sgt1922 to sgt1930, which is the source kept for them). The 1924 class: sgt1935 prints 39 enlisted, every edition from sgt1924 to sgt1930 prints 93, which the identity requires: 93 kept, flag `reprint_corrected`.

Rows of a class or year that fail a check are flagged `total_mismatch` (all items of that
row); the values are kept as printed.

## Editions used and compared

Transcribed (printed window, Gallica view and printed page per edition): sgt1922 1902-1922 (view 46, p. 22), sgt1923 1902-1923 (view 524, p. 22), sgt1924 1902-1924 (view 1012, p. 22), sgt1925 1902-1925 (view 45, p. 21), sgt1926 1902-1926 (view 592, p. 28), sgt1927 1902-1927 (view 56, p. 28), sgt1928 1902-1928 (view 580, p. 28), sgt1929 1903-1929 (view 56, p. 28), sgt1930 1904-1930 (view 586, p. 28), sgt1935 1916-1935 (view 39, p. 19), sgt1936 1933-1937 (view 26, p. 15), sgt1939 1935-1939 (view 21, p. 15). Transcriptions:
`transcribed/recruitment.txt` (sgt1925, sgt1930, sgt1935, sgt1936, sgt1939) and
`transcribed/recruitment_1922_1929.txt` (sgt1922-sgt1924, sgt1926-sgt1929). Each edition
prints the French tables on one page and the indigenous tables on the facing page.

Source edition of each conscription class (classe) (the latest edition that prints it, rule 4 of
`SPEC_ADDENDUM.md`): 1902 from sgt1928, 1903 from sgt1929, 1904-1915 from sgt1930, 1916-1932 from sgt1935, 1933-1934 from sgt1936, 1935-1939 from sgt1939.

Footnote printed under the table (every edition from sgt1922 to sgt1930), on class 1913: *(1) Application de la loi du 7 août 1913* (application of the law of 7 August 1913).

Every other printing of the same cell was compared with the kept (latest) printing:
1712 comparisons, 1705 equal, 7 different. Per edition (cells compared,
equal, differences):

- sgt1922: 168 compared, 168 equal
- sgt1923: 176 compared, 176 equal
- sgt1924: 184 compared, 183 equal: 1924 enlisted_maritime: 93 (latest printing, sgt1935: 39)
- sgt1925: 192 compared, 191 equal: 1924 enlisted_maritime: 93 (latest printing, sgt1935: 39)
- sgt1926: 200 compared, 199 equal: 1924 enlisted_maritime: 93 (latest printing, sgt1935: 39)
- sgt1927: 208 compared, 207 equal: 1924 enlisted_maritime: 93 (latest printing, sgt1935: 39)
- sgt1928: 208 compared, 207 equal: 1924 enlisted_maritime: 93 (latest printing, sgt1935: 39)
- sgt1929: 208 compared, 207 equal: 1924 enlisted_maritime: 93 (latest printing, sgt1935: 39)
- sgt1930: 120 compared, 119 equal: 1924 enlisted_maritime: 93 (latest printing, sgt1935: 39)
- sgt1935: 24 compared, 24 equal
- sgt1936: 24 compared, 24 equal

The only difference is the 1924 class, enlisted: 93 in every printing from sgt1924 to
sgt1930, 39 in sgt1935 (the latest); see above. One doubtful glyph: sgt1926 prints the
1919 class's postponed as "5" and a broken second glyph (a bare stroke, without the flag
and foot of this font's 1); it is read as 54, like every other printing, which sgt1926's
own row identity also needs (491 - 9 - 0 - 54 - 6 - 178 = 244, printed 244).

## Validation

122 of 138 printed-total checks pass. Failing checks (each re-read on the image at full resolution; printed values kept):

- sgt1922 1920 called = registered - exempted - neo-French - postponed - deferred - enlisted: computed 289 != printed 281
- sgt1923 1920 called = registered - exempted - neo-French - postponed - deferred - enlisted: computed 289 != printed 281
- sgt1924 1920 called = registered - exempted - neo-French - postponed - deferred - enlisted: computed 289 != printed 281
- sgt1925 1920 called = registered - exempted - neo-French - postponed - deferred - enlisted: computed 289 != printed 281
- sgt1926 1920 called = registered - exempted - neo-French - postponed - deferred - enlisted: computed 289 != printed 281
- sgt1926 1926 called = registered - exempted - neo-French - postponed - deferred - enlisted: computed 410 != printed 416
- sgt1927 1920 called = registered - exempted - neo-French - postponed - deferred - enlisted: computed 289 != printed 281
- sgt1927 1926 called = registered - exempted - neo-French - postponed - deferred - enlisted: computed 410 != printed 416
- sgt1928 1920 called = registered - exempted - neo-French - postponed - deferred - enlisted: computed 289 != printed 281
- sgt1928 1926 called = registered - exempted - neo-French - postponed - deferred - enlisted: computed 410 != printed 416
- sgt1929 1920 called = registered - exempted - neo-French - postponed - deferred - enlisted: computed 289 != printed 281
- sgt1929 1926 called = registered - exempted - neo-French - postponed - deferred - enlisted: computed 410 != printed 416
- sgt1930 1920 called = registered - exempted - neo-French - postponed - deferred - enlisted: computed 289 != printed 281
- sgt1930 1926 called = registered - exempted - neo-French - postponed - deferred - enlisted: computed 410 != printed 416
- sgt1935 1920 called = registered - exempted - neo-French - postponed - deferred - enlisted: computed 289 != printed 281
- sgt1935 1926 called = registered - exempted - neo-French - postponed - deferred - enlisted: computed 410 != printed 416

Common columns: `census` (source edition, e.g. `sgt1930`), `gallica_ark` (volume ark), `table_id`, `source_page` (printed page), `gallica_view`, `value`, `flag` (empty, `ocr_corrected`, `illegible`, `total_mismatch`, `derived_from_totals`, `not_applicable`, `reprint_corrected`; see `data-raw/colonial_census/SPEC.md`). A printed `»` is stored as 0. Printed totals are not stored; they were used for validation.
