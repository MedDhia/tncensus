# Foreigners' arrivals and departures by nationality, 1917-1939

Source: *Statistique générale de la Tunisie*, Régence de Tunis (annual). Source gallica.bnf.fr / Ministère des Affaires étrangères (NoC-CR). Editions and views: see `EDITIONS.md`.

*Mouvement des étrangers en Tunisie, entrées et sorties*: foreigners' arrivals and
departures by nationality, 1917-1939. 1740 rows: one per year, movement and
nationality. Each cell is taken from the latest edition that prints it (`census`),
except the columns listed under "Corrections", where the latest printing is wrong.

Columns: `year`, `movement` (`arrivals` / `departures`), `nationality` (English code),
`nationality_fr` (as printed), `value` = persons. A footnote in the 1926-1930 editions
says that for 1923-1926 the figures are declarations of residence (men and women,
children excluded). In 1933 Serbs are printed as "compris dans les Yougoslaves" and
Tripolitanians as "compris dans les Italiens": `value` NA, flag `not_applicable`.

Two lists of nationalities are used. The 1926 and 1927 editions list 28 (with *Anglais*
and *Anglo-Maltais* separately, summed here into `british_anglo_maltese`;
*Autrichiens et Hongrois* together, `austrian_hungarian`; *Autres étrangers* = `other`);
from 1928 the table lists 45 (46 with *Indous* from 1935), and from 1936 32. Years taken
from the 1926-1927 editions (1917-1918, 1921-1927, see below) therefore use the short
list.

## Sources used

- sgt1926 (pp. 26-27, views 590-591): 1917-1926; the only printing of 1921.
- sgt1927 (pp. 26-27, views 54-55): 1918-1927; latest printing of 1918.
- sgt1928 (pp. 26-27, views 578-579): 1917, 1919-1928; latest printing of 1917 and 1919.
- sgt1929 (p. 26, view 54): 1920-1923; latest printing of 1920.
- sgt1930 (pp. 26-27, views 584-585): 1921-1930; the 1929 departures (in the binding of
  sgt1935).
- sgt1935 (pp. 16-17, views 36-37): 1926-1935; latest printing of 1928-1931, and of
  1932-1934 for the nationalities that the 1936 edition no longer lists.
- sgt1936 (p. 14, view 25): 1932-1936; latest printing of 1932-1934 where it lists the
  nationality.
- sgt1939 (p. 14, view 20): 1935-1939.

## The year labels of 1917 and 1921

The 1926 edition prints 1917-1926 in order. The 1927 edition (1918-1927) prints 1918,
1919, 1920 and then, in the slot where 1921 belongs, a column labelled **1917** with
1917's figures (3.388 arrivals, 2.302 departures; Italians 2.948 / 1.850), and no 1921.
The 1928 edition does the same (1919, 1920, "1917", 1922...). The 1929 and 1930 editions
keep that column but label it **1921**. So the figures printed as 1921 in the 1929 and
1930 editions are 1917's; the only printing of 1921 is the 1926 edition's (4.740 / 2.483,
whose cells add up to its printed totals). Here, 1917 is taken from sgt1928 (its
correctly labelled column, identical to sgt1926 and sgt1927) and 1921 from sgt1926.

## Corrections (`reprint_corrected`)

Besides 1921, the 1928 edition re-keyed 1922-1927 onto its new list of nationalities, and
the 1929-1935 editions copied it. The re-keyed columns do not add up to their printed
totals, while the 1926-1927 printings do; so those columns are taken from the older
printing (`FOR_GOOD` in the script):

- 1922 arrivals: Spaniards printed 34 for 64; Estonians 5 and Venezuelans 2 added, Yugoslavs
  2 dropped. 1922 departures: Belgians printed 7 for 17.
- 1923 arrivals: Tripolitanians 11 added (not in the older printing, which adds up without
  them).
- 1924 arrivals: Syrians 1 dropped. 1925: Persians 1 and Syrians 2 / 1 dropped. 1926
  departures and 1927: Persians and Syrians dropped; 1927 arrivals Italians 1.725 for 1.726.
- 1926 arrivals: the 1927 and later editions print Belgians 61 with a total of 3.562, which
  their cells do not reach; the 1926 edition prints 661, and its cells then add up to
  3.562. 661 is kept.

Every cell that changes is listed here:

- 1921 arrivals american: sgt1930 prints 4, kept 13 from sgt1926
- 1921 arrivals austrian_hungarian: sgt1930 prints 0, kept 7 from sgt1926
- 1921 arrivals belgian: sgt1930 prints 41, kept 29 from sgt1926
- 1921 arrivals british_anglo_maltese: sgt1930 prints 275, kept 345 from sgt1926
- 1921 arrivals bulgarian: sgt1930 prints 0, kept 1 from sgt1926
- 1921 arrivals chinese: sgt1930 prints 0, kept 2 from sgt1926
- 1921 arrivals czechoslovak: sgt1930 prints 0, kept 4 from sgt1926
- 1921 arrivals danish: sgt1930 prints 1, kept 0 from sgt1926
- 1921 arrivals dutch: sgt1930 prints 2, kept 14 from sgt1926
- 1921 arrivals egyptian: sgt1930 prints 0, kept 1 from sgt1926
- 1921 arrivals german: sgt1930 prints 0, kept 4 from sgt1926
- 1921 arrivals greek: sgt1930 prints 28, kept 76 from sgt1926
- 1921 arrivals italian: sgt1930 prints 2948, kept 3560 from sgt1926
- 1921 arrivals norwegian: sgt1930 prints 1, kept 4 from sgt1926
- 1921 arrivals other: sgt1930 prints 0, kept 7 from sgt1926
- 1921 arrivals portuguese: sgt1930 prints 0, kept 9 from sgt1926
- 1921 arrivals romanian: sgt1930 prints 0, kept 7 from sgt1926
- 1921 arrivals russian: sgt1930 prints 4, kept 450 from sgt1926
- 1921 arrivals serbian: sgt1930 prints 0, kept 17 from sgt1926
- 1921 arrivals spanish: sgt1930 prints 51, kept 48 from sgt1926
- 1921 arrivals swedish: sgt1930 prints 2, kept 9 from sgt1926
- 1921 arrivals swiss: sgt1930 prints 31, kept 84 from sgt1926
- 1921 arrivals turkish: sgt1930 prints 0, kept 45 from sgt1926
- 1921 arrivals yugoslav: sgt1930 prints 0, kept 4 from sgt1926
- 1921 departures american: sgt1930 prints 5, kept 9 from sgt1926
- 1921 departures austrian_hungarian: sgt1930 prints 0, kept 4 from sgt1926
- 1921 departures belgian: sgt1930 prints 25, kept 14 from sgt1926
- 1921 departures british_anglo_maltese: sgt1930 prints 349, kept 253 from sgt1926
- 1921 departures bulgarian: sgt1930 prints 0, kept 1 from sgt1926
- 1921 departures chinese: sgt1930 prints 0, kept 1 from sgt1926
- 1921 departures czechoslovak: sgt1930 prints 0, kept 2 from sgt1926
- 1921 departures danish: sgt1930 prints 1, kept 0 from sgt1926
- 1921 departures dutch: sgt1930 prints 3, kept 6 from sgt1926
- 1921 departures german: sgt1930 prints 0, kept 3 from sgt1926
- 1921 departures greek: sgt1930 prints 14, kept 39 from sgt1926
- 1921 departures italian: sgt1930 prints 1850, kept 1854 from sgt1926
- 1921 departures norwegian: sgt1930 prints 1, kept 2 from sgt1926
- 1921 departures other: sgt1930 prints 1, kept 4 from sgt1926
- 1921 departures portuguese: sgt1930 prints 0, kept 4 from sgt1926
- 1921 departures romanian: sgt1930 prints 1, kept 8 from sgt1926
- 1921 departures russian: sgt1930 prints 3, kept 120 from sgt1926
- 1921 departures serbian: sgt1930 prints 0, kept 14 from sgt1926
- 1921 departures spanish: sgt1930 prints 21, kept 54 from sgt1926
- 1921 departures swedish: sgt1930 prints 8, kept 7 from sgt1926
- 1921 departures swiss: sgt1930 prints 17, kept 59 from sgt1926
- 1921 departures turkish: sgt1930 prints 3, kept 24 from sgt1926
- 1921 departures yugoslav: sgt1930 prints 0, kept 1 from sgt1926
- 1922 arrivals estonian: sgt1930 prints 5, kept 0 from sgt1927
- 1922 arrivals spanish: sgt1930 prints 34, kept 64 from sgt1927
- 1922 arrivals venezuelan: sgt1930 prints 2, kept 0 from sgt1927
- 1922 arrivals yugoslav: sgt1930 prints 0, kept 2 from sgt1927
- 1922 departures belgian: sgt1930 prints 7, kept 17 from sgt1927
- 1923 arrivals tripolitanian: sgt1930 prints 11, kept 0 from sgt1927
- 1924 arrivals syrian: sgt1930 prints 0, kept 1 from sgt1927
- 1925 arrivals persian: sgt1930 prints 0, kept 1 from sgt1927
- 1925 arrivals syrian: sgt1930 prints 0, kept 2 from sgt1927
- 1925 departures syrian: sgt1930 prints 0, kept 1 from sgt1927
- 1926 arrivals belgian: sgt1935 prints 61, kept 661 from sgt1926
- 1926 arrivals persian: sgt1935 prints 0, kept 3 from sgt1926
- 1926 arrivals syrian: sgt1935 prints 0, kept 3 from sgt1926
- 1926 departures persian: sgt1935 prints 0, kept 2 from sgt1927
- 1926 departures syrian: sgt1935 prints 0, kept 3 from sgt1927
- 1927 arrivals italian: sgt1935 prints 1725, kept 1726 from sgt1927
- 1927 arrivals persian: sgt1935 prints 0, kept 2 from sgt1927
- 1927 departures persian: sgt1935 prints 0, kept 2 from sgt1927

Columns that still do not add up are misprints with no consistent printing: 1920 arrivals
(sgt1929 prints a total of 4.505; cells and the older printings give 4.506), 1928 arrivals,
1929 arrivals, 1930 departures, 1931 (arrivals printed 55.302, cells 19.546), 1933-1934,
and the 1936-1939 editions, whose rows omit 14 nationalities that their totals include.

## Comparison of the overlapping printings

Every other printing of each cell was compared with the kept value (categories mapped
between the two lists: Anglais + Anglo-Maltais; Autrichiens + Hongrois): 2441
comparisons, 2253 equal, 188 different:

- 1921 arrivals american: sgt1929 prints 4, sgt1926 prints 13
- 1921 arrivals austrian_hungarian: sgt1929 prints 0, sgt1926 prints 7
- 1921 arrivals belgian: sgt1929 prints 41, sgt1926 prints 29
- 1921 arrivals british_anglo_maltese: sgt1929 prints 275, sgt1926 prints 345
- 1921 arrivals bulgarian: sgt1929 prints 0, sgt1926 prints 1
- 1921 arrivals chinese: sgt1929 prints 0, sgt1926 prints 2
- 1921 arrivals czechoslovak: sgt1929 prints 0, sgt1926 prints 4
- 1921 arrivals danish: sgt1929 prints 1, sgt1926 prints 0
- 1921 arrivals dutch: sgt1929 prints 2, sgt1926 prints 14
- 1921 arrivals egyptian: sgt1929 prints 0, sgt1926 prints 1
- 1921 arrivals german: sgt1929 prints 0, sgt1926 prints 4
- 1921 arrivals greek: sgt1929 prints 28, sgt1926 prints 76
- 1921 arrivals italian: sgt1929 prints 2948, sgt1926 prints 3560
- 1921 arrivals norwegian: sgt1929 prints 1, sgt1926 prints 4
- 1921 arrivals other: sgt1929 prints 0, sgt1926 prints 7
- 1921 arrivals portuguese: sgt1929 prints 0, sgt1926 prints 9
- 1921 arrivals romanian: sgt1929 prints 0, sgt1926 prints 7
- 1921 arrivals russian: sgt1929 prints 4, sgt1926 prints 450
- 1921 arrivals serbian: sgt1929 prints 0, sgt1926 prints 17
- 1921 arrivals spanish: sgt1929 prints 51, sgt1926 prints 48
- 1921 arrivals swedish: sgt1929 prints 2, sgt1926 prints 9
- 1921 arrivals swiss: sgt1929 prints 31, sgt1926 prints 84
- 1921 arrivals turkish: sgt1929 prints 0, sgt1926 prints 45
- 1921 arrivals yugoslav: sgt1929 prints 0, sgt1926 prints 4
- 1921 arrivals american: sgt1930 prints 4, sgt1926 prints 13
- 1921 arrivals austrian_hungarian: sgt1930 prints 0, sgt1926 prints 7
- 1921 arrivals belgian: sgt1930 prints 41, sgt1926 prints 29
- 1921 arrivals british_anglo_maltese: sgt1930 prints 275, sgt1926 prints 345
- 1921 arrivals bulgarian: sgt1930 prints 0, sgt1926 prints 1
- 1921 arrivals chinese: sgt1930 prints 0, sgt1926 prints 2
- 1921 arrivals czechoslovak: sgt1930 prints 0, sgt1926 prints 4
- 1921 arrivals danish: sgt1930 prints 1, sgt1926 prints 0
- 1921 arrivals dutch: sgt1930 prints 2, sgt1926 prints 14
- 1921 arrivals egyptian: sgt1930 prints 0, sgt1926 prints 1
- 1921 arrivals german: sgt1930 prints 0, sgt1926 prints 4
- 1921 arrivals greek: sgt1930 prints 28, sgt1926 prints 76
- 1921 arrivals italian: sgt1930 prints 2948, sgt1926 prints 3560
- 1921 arrivals norwegian: sgt1930 prints 1, sgt1926 prints 4
- 1921 arrivals other: sgt1930 prints 0, sgt1926 prints 7
- 1921 arrivals portuguese: sgt1930 prints 0, sgt1926 prints 9
- 1921 arrivals romanian: sgt1930 prints 0, sgt1926 prints 7
- 1921 arrivals russian: sgt1930 prints 4, sgt1926 prints 450
- 1921 arrivals serbian: sgt1930 prints 0, sgt1926 prints 17
- 1921 arrivals spanish: sgt1930 prints 51, sgt1926 prints 48
- 1921 arrivals swedish: sgt1930 prints 2, sgt1926 prints 9
- 1921 arrivals swiss: sgt1930 prints 31, sgt1926 prints 84
- 1921 arrivals turkish: sgt1930 prints 0, sgt1926 prints 45
- 1921 arrivals yugoslav: sgt1930 prints 0, sgt1926 prints 4
- 1921 departures american: sgt1929 prints 5, sgt1926 prints 9
- 1921 departures austrian_hungarian: sgt1929 prints 0, sgt1926 prints 4
- 1921 departures belgian: sgt1929 prints 25, sgt1926 prints 14
- 1921 departures british_anglo_maltese: sgt1929 prints 349, sgt1926 prints 253
- 1921 departures bulgarian: sgt1929 prints 0, sgt1926 prints 1
- 1921 departures chinese: sgt1929 prints 0, sgt1926 prints 1
- 1921 departures czechoslovak: sgt1929 prints 0, sgt1926 prints 2
- 1921 departures danish: sgt1929 prints 1, sgt1926 prints 0
- 1921 departures dutch: sgt1929 prints 3, sgt1926 prints 6
- 1921 departures german: sgt1929 prints 0, sgt1926 prints 3
- 1921 departures greek: sgt1929 prints 14, sgt1926 prints 39
- 1921 departures italian: sgt1929 prints 1850, sgt1926 prints 1854
- 1921 departures norwegian: sgt1929 prints 1, sgt1926 prints 2
- 1921 departures other: sgt1929 prints 1, sgt1926 prints 4
- 1921 departures portuguese: sgt1929 prints 0, sgt1926 prints 4
- 1921 departures romanian: sgt1929 prints 1, sgt1926 prints 8
- 1921 departures russian: sgt1929 prints 3, sgt1926 prints 120
- 1921 departures serbian: sgt1929 prints 0, sgt1926 prints 14
- 1921 departures spanish: sgt1929 prints 21, sgt1926 prints 54
- 1921 departures swedish: sgt1929 prints 8, sgt1926 prints 7
- 1921 departures swiss: sgt1929 prints 17, sgt1926 prints 59
- 1921 departures turkish: sgt1929 prints 3, sgt1926 prints 24
- 1921 departures yugoslav: sgt1929 prints 0, sgt1926 prints 1
- 1921 departures american: sgt1930 prints 5, sgt1926 prints 9
- 1921 departures austrian_hungarian: sgt1930 prints 0, sgt1926 prints 4
- 1921 departures belgian: sgt1930 prints 25, sgt1926 prints 14
- 1921 departures british_anglo_maltese: sgt1930 prints 349, sgt1926 prints 253
- 1921 departures bulgarian: sgt1930 prints 0, sgt1926 prints 1
- 1921 departures chinese: sgt1930 prints 0, sgt1926 prints 1
- 1921 departures czechoslovak: sgt1930 prints 0, sgt1926 prints 2
- 1921 departures danish: sgt1930 prints 1, sgt1926 prints 0
- 1921 departures dutch: sgt1930 prints 3, sgt1926 prints 6
- 1921 departures german: sgt1930 prints 0, sgt1926 prints 3
- 1921 departures greek: sgt1930 prints 14, sgt1926 prints 39
- 1921 departures italian: sgt1930 prints 1850, sgt1926 prints 1854
- 1921 departures norwegian: sgt1930 prints 1, sgt1926 prints 2
- 1921 departures other: sgt1930 prints 1, sgt1926 prints 4
- 1921 departures portuguese: sgt1930 prints 0, sgt1926 prints 4
- 1921 departures romanian: sgt1930 prints 1, sgt1926 prints 8
- 1921 departures russian: sgt1930 prints 3, sgt1926 prints 120
- 1921 departures serbian: sgt1930 prints 0, sgt1926 prints 14
- 1921 departures spanish: sgt1930 prints 21, sgt1926 prints 54
- 1921 departures swedish: sgt1930 prints 8, sgt1926 prints 7
- 1921 departures swiss: sgt1930 prints 17, sgt1926 prints 59
- 1921 departures turkish: sgt1930 prints 3, sgt1926 prints 24
- 1921 departures yugoslav: sgt1930 prints 0, sgt1926 prints 1
- 1922 arrivals estonian: sgt1928 prints 5, sgt1927 prints None
- 1922 arrivals spanish: sgt1928 prints 34, sgt1927 prints 64
- 1922 arrivals venezuelan: sgt1928 prints 2, sgt1927 prints None
- 1922 arrivals yugoslav: sgt1928 prints 0, sgt1927 prints 2
- 1922 arrivals estonian: sgt1929 prints 5, sgt1927 prints None
- 1922 arrivals spanish: sgt1929 prints 34, sgt1927 prints 64
- 1922 arrivals venezuelan: sgt1929 prints 2, sgt1927 prints None
- 1922 arrivals yugoslav: sgt1929 prints 0, sgt1927 prints 2
- 1922 arrivals estonian: sgt1930 prints 5, sgt1927 prints None
- 1922 arrivals spanish: sgt1930 prints 34, sgt1927 prints 64
- 1922 arrivals venezuelan: sgt1930 prints 2, sgt1927 prints None
- 1922 arrivals yugoslav: sgt1930 prints 0, sgt1927 prints 2
- 1922 departures other: sgt1926 prints 5, sgt1927 prints 6
- 1922 departures belgian: sgt1929 prints 7, sgt1927 prints 17
- 1922 departures belgian: sgt1930 prints 7, sgt1927 prints 17
- 1923 arrivals tripolitanian: sgt1928 prints 11, sgt1927 prints None
- 1923 arrivals tripolitanian: sgt1929 prints 11, sgt1927 prints None
- 1923 arrivals tripolitanian: sgt1930 prints 11, sgt1927 prints None
- 1924 arrivals syrian: sgt1928 prints 0, sgt1927 prints 1
- 1924 arrivals syrian: sgt1930 prints 0, sgt1927 prints 1
- 1925 arrivals persian: sgt1928 prints 0, sgt1927 prints 1
- 1925 arrivals syrian: sgt1928 prints 0, sgt1927 prints 2
- 1925 arrivals persian: sgt1930 prints 0, sgt1927 prints 1
- 1925 arrivals syrian: sgt1930 prints 0, sgt1927 prints 2
- 1925 departures syrian: sgt1928 prints 0, sgt1927 prints 1
- 1925 departures syrian: sgt1930 prints 0, sgt1927 prints 1
- 1926 arrivals belgian: sgt1927 prints 61, sgt1926 prints 661
- 1926 arrivals belgian: sgt1928 prints 61, sgt1926 prints 661
- 1926 arrivals persian: sgt1928 prints 0, sgt1926 prints 3
- 1926 arrivals syrian: sgt1928 prints 0, sgt1926 prints 3
- 1926 arrivals belgian: sgt1930 prints 61, sgt1926 prints 661
- 1926 arrivals persian: sgt1930 prints 0, sgt1926 prints 3
- 1926 arrivals syrian: sgt1930 prints 0, sgt1926 prints 3
- 1926 arrivals belgian: sgt1935 prints 61, sgt1926 prints 661
- 1926 arrivals persian: sgt1935 prints 0, sgt1926 prints 3
- 1926 arrivals syrian: sgt1935 prints 0, sgt1926 prints 3
- 1926 departures persian: sgt1928 prints 0, sgt1927 prints 2
- 1926 departures syrian: sgt1928 prints 0, sgt1927 prints 3
- 1926 departures persian: sgt1930 prints 0, sgt1927 prints 2
- 1926 departures syrian: sgt1930 prints 0, sgt1927 prints 3
- 1926 departures persian: sgt1935 prints 0, sgt1927 prints 2
- 1926 departures syrian: sgt1935 prints 0, sgt1927 prints 3
- 1927 arrivals italian: sgt1928 prints 1725, sgt1927 prints 1726
- 1927 arrivals persian: sgt1928 prints 0, sgt1927 prints 2
- 1927 arrivals italian: sgt1930 prints 1725, sgt1927 prints 1726
- 1927 arrivals persian: sgt1930 prints 0, sgt1927 prints 2
- 1927 arrivals italian: sgt1935 prints 1725, sgt1927 prints 1726
- 1927 arrivals persian: sgt1935 prints 0, sgt1927 prints 2
- 1927 departures persian: sgt1928 prints 0, sgt1927 prints 2
- 1927 departures persian: sgt1930 prints 0, sgt1927 prints 2
- 1927 departures persian: sgt1935 prints 0, sgt1927 prints 2
- 1932 arrivals albanian: sgt1935 prints 1, sgt1936 prints None
- 1932 arrivals australian: sgt1935 prints 1, sgt1936 prints None
- 1932 arrivals chinese: sgt1935 prints 12, sgt1936 prints None
- 1932 departures australian: sgt1935 prints 3, sgt1936 prints None
- 1932 departures chinese: sgt1935 prints 4, sgt1936 prints None
- 1932 departures japanese: sgt1935 prints 1, sgt1936 prints None
- 1933 arrivals albanian: sgt1935 prints 1, sgt1936 prints None
- 1933 arrivals argentine: sgt1935 prints 2, sgt1936 prints None
- 1933 arrivals armenian: sgt1935 prints 1, sgt1936 prints None
- 1933 arrivals chinese: sgt1935 prints 17, sgt1936 prints None
- 1933 arrivals mexican: sgt1935 prints 1, sgt1936 prints None
- 1933 departures argentine: sgt1935 prints 1, sgt1936 prints None
- 1933 departures brazilian: sgt1935 prints 1, sgt1936 prints None
- 1933 departures chinese: sgt1935 prints 7, sgt1936 prints None
- 1934 arrivals albanian: sgt1935 prints 1, sgt1936 prints None
- 1934 arrivals argentine: sgt1935 prints 1, sgt1936 prints None
- 1934 arrivals armenian: sgt1935 prints 4, sgt1936 prints None
- 1934 arrivals brazilian: sgt1935 prints 2, sgt1936 prints None
- 1934 arrivals chinese: sgt1935 prints 17, sgt1936 prints None
- 1934 arrivals colombian: sgt1935 prints 2, sgt1936 prints None
- 1934 arrivals latvian: sgt1935 prints 1, sgt1936 prints None
- 1934 arrivals lebanese: sgt1935 prints 3, sgt1936 prints None
- 1934 arrivals serbian: sgt1935 prints 3, sgt1936 prints None
- 1934 departures chinese: sgt1935 prints 13, sgt1936 prints None
- 1934 departures colombian: sgt1935 prints 2, sgt1936 prints None
- 1934 departures lebanese: sgt1935 prints 1, sgt1936 prints None
- 1934 departures serbian: sgt1935 prints 2, sgt1936 prints None
- 1935 arrivals albanian: sgt1935 prints 3, sgt1939 prints None
- 1935 arrivals armenian: sgt1935 prints 10, sgt1939 prints None
- 1935 arrivals brazilian: sgt1935 prints 2, sgt1939 prints None
- 1935 arrivals latvian: sgt1935 prints 1, sgt1939 prints None
- 1935 arrivals lebanese: sgt1935 prints 4, sgt1939 prints None
- 1935 arrivals mexican: sgt1935 prints 2, sgt1939 prints None
- 1935 arrivals persian: sgt1935 prints 5, sgt1939 prints None
- 1935 arrivals serbian: sgt1935 prints 2, sgt1939 prints None
- 1935 departures albanian: sgt1935 prints 2, sgt1939 prints None
- 1935 departures armenian: sgt1935 prints 1, sgt1939 prints None
- 1935 departures brazilian: sgt1935 prints 1, sgt1939 prints None
- 1935 departures chinese: sgt1935 prints 16, sgt1939 prints None
- 1935 departures japanese: sgt1935 prints 1, sgt1939 prints None
- 1935 departures lebanese: sgt1935 prints 3, sgt1939 prints None
- 1935 departures persian: sgt1935 prints 3, sgt1939 prints None
- 1935 departures serbian: sgt1935 prints 2, sgt1939 prints None

The 1925 edition (1925 only, with its own list including Cubains, Lithuaniens, Péruviens)
was not transcribed; its totals (2.233 / 1.052) equal the kept 1925 values.

## Validation

69 of 125 printed-total checks pass. Failing checks (each re-read on the image at full resolution; printed values kept):

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
- sgt1927 1926 arrivals column total: computed 2962 != printed 3562
- sgt1928 1920 arrivals column total: computed 4506 != printed 4505
- sgt1928 1922 arrivals column total: computed 4805 != printed 4830
- sgt1928 1923 arrivals column total: computed 2729 != printed 2718
- sgt1928 1924 arrivals column total: computed 2533 != printed 2534
- sgt1928 1925 arrivals column total: computed 2230 != printed 2233
- sgt1928 1925 departures column total: computed 1051 != printed 1052
- sgt1928 1926 arrivals column total: computed 2956 != printed 3562
- sgt1928 1926 departures column total: computed 1230 != printed 1235
- sgt1928 1927 arrivals column total: computed 2522 != printed 2525
- sgt1928 1927 departures column total: computed 1210 != printed 1212
- sgt1928 1928 arrivals column total: computed 13443 != printed 13234

Common columns: `census` (source edition, e.g. `sgt1930`), `gallica_ark` (volume ark), `table_id`, `source_page` (printed page), `gallica_view`, `value`, `flag` (empty, `ocr_corrected`, `illegible`, `total_mismatch`, `derived_from_totals`, `not_applicable`, `reprint_corrected`; see `data-raw/colonial_census/SPEC.md`). A printed `»` is stored as 0. Printed totals are not stored; they were used for validation.
