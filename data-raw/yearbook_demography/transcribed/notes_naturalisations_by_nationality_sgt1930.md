## Cell-by-cell comparison with the other printings

`compare_naturalisations_e.py` compares the transcriptions in
`transcribed/naturalisations_e_<edition>.txt` with this file, cell by cell, and
writes `naturalisations_e_comparison.json`. Row mappings are explicit in the
script:
- *Turcs* = *Turcs et Syriens*.
- *Musulmans marocains* = *Divers*.
- 1922–1923's *Musulmans soudanais* goes to the Algerians for 1891–1898 and to the Tunisians for 1923.
- 1922–1923 print one column per year, so 1911–1920 is summed.

Rows a printing does not print were checked to be 0.

| Edition | Views (pp.) | Cells compared | Equal | Different | Own printed totals |
|---|---|---:|---:|---:|---|
| sgt1922 | 44–45 (20–21) | 168 | 168 | 0 | 62 pass, 2 not checkable |
| sgt1923 | 522–523 (20–21) | 231 | 231 | 0 | 68 pass, 2 not checkable |
| sgt1925 | 43 (19) | 391 | 391 | 0 | 25/25 |
| sgt1926 | 588–589 (24–25) | 437 | 437 | 0 | 28/28 |
| sgt1927 | 52–53 (24–25) | 483 | 483 | 0 | 30/31 |
| sgt1928 | 576–577 (24–25) | 529 | 529 | 0 | 34/34 |

Rows absent from a printing were zero in this file in every case (66, 78, 68, 76, 84 and 92 cells).

- **sgt1922, binding:** the 1915 minors column under the 1910 decree is hidden. The values the stored 1911–1920 minors imply for 1915 (Suisses 5, Portugais 2, Israélites tunisiens 3) sum to the derived total of 10 and equal sgt1923's legible 1915 column.
- **Law of 1914:** sgt1922 and sgt1923 print 1915–1922 and 1915–1923 instead of 1915–1924, so these were compared as sub-periods (42 cells each). sgt1923 matches all 42. sgt1922 differs in 3 (Italiens 97/99, Autrichiens 0/1, Musulmans tunisiens 32/33), exactly sgt1923's 1923 grants.
- **sgt1927 misprint:** the 1927 pair total is printed 4,958 for 1,431 + 1,527 = 2,958; sgt1928 prints 2,958.

No printing contradicts a stored value, so nothing is corrected.
