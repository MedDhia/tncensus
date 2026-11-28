# Taxe de change (mandats-poste internationaux)

*Exchange rates applied to international money orders, by country and date.*

Source: *Statistique générale de la Tunisie*, chapter *Postes - Télégraphes - Téléphones*, section "c) Taxe de change" (heading of the first page; later editions print it the same way or as "Taux de change"), editions transcribed: sgt1922, sgt1923, sgt1924, sgt1925, sgt1926, sgt1927, sgt1928, sgt1929, sgt1930. Source gallica.bnf.fr / Ministère des Affaires étrangères.

Pages and views: sgt1922 (`bpt6k9105649x`): f159-f171; sgt1923 (`bpt6k9105649x`): f643-f661; sgt1924 (`bpt6k9105649x`): f1133-f1156; sgt1925 (`bpt6k9105650k`): f169-f197; sgt1926 (`bpt6k9105650k`): f719-f752; sgt1927 (`bpt6k91056510`): f181-f214; sgt1928 (`bpt6k91056510`): f705-f738; sgt1929 (`bpt6k9105652d`): f183-f216; sgt1930 (`bpt6k9105652d`): f717-f750. Survey page by page: `posts_exchange_survey.md`.

Transcriptions: `../transcribed/posts_exchange_<edition>.txt`; rebuild with `python3 data-raw/yearbook_other_chapters/extract_posts_exchange.py build`.

Rows: 3795 (one per printed date and rate). Years: 1915-1930. Stored from: sgt1930 3795.

Units: see `unit`. For the six countries under *Mandats émis en monnaie étrangère* the rate is the number of French francs given for one pound, dollar, florin or crown (the printed par value is in `par_fr`). For Switzerland and Greece the column is *Change %* with the sub-heading *FR.*: the premium of the foreign currency over the franc, in francs per 100 (e.g. 150 = 150 % premium). Greece switches on 27 April 1921 to a direct quotation: the value cell of that date prints *Cours norm.*, the next line *1 dr. =*, and the following values (preceded by a dash that repeats *1 dr. =*) are francs per drachma (`fr_per_drachma`). value_type: rate.

Every edition reprints the whole series from 1915 with the new dates added, so the printings overlap. Each country-year is taken from the **latest** edition that prints it (SPEC_ADDENDUM rule 4; `census` = that edition); every other printing of the same country-year, read on its own page images, is compared date by date below.

## Columns

- `census`: edition the value is taken from (`sgt1922` … `sgt1930`): the latest edition printing that country and year
- `table_id`: `c` (section c) of the chapter's money-order tables: *Taxe de change*, later *Taux de change*)
- `gallica_ark`: Gallica volume ark (views are numbered within a volume)
- `source_page`: printed page number
- `gallica_view`: Gallica view (fNNNN)
- `year`: year of `date_from` (the *Années* column, printed at the top of each page and where the year changes)
- `date_from`: ISO date printed in the *Dates* column: the date from which the rate applied
- `date_to`: derived, not printed: the day before the next later date printed for the same country in the stored series; empty for the last date of a country, for a date printed twice, and before the printed interruption of the Greek service
- `period_fr`: the date as printed (day, month and the year of the *Années* column as printed)
- `country`: English code: `united_kingdom`, `united_states`, `netherlands`, `denmark`, `sweden`, `norway`, `switzerland`, `greece`
- `country_fr`: country heading as printed (capitals in the source)
- `money_order_fr`: sub-heading printed over the country (*Mandats émis en monnaie étrangère*: money orders issued in the foreign currency); empty for Suisse and Grèce, which print none
- `par_fr`: normal (par) value of the conversion printed under the heading; empty where none is printed
- `unit`: `fr_per_pound`, `fr_per_dollar`, `fr_per_florin`, `fr_per_krone` (French francs for one unit of the foreign currency, column *Francs*), `change_pct` (column *Change %*, sub-heading *FR.*: the exchange premium in French francs per 100 francs of the foreign currency), `fr_per_drachma` (Greece from May 1921: francs for one drachma, after the printed line *Cours norm. 1 dr. =*)
- `unit_fr`: the column heading as printed and the unit it implies
- `value`: the rate as printed (`26 »` = 26; `25 60` = 25.60; `5 875` = 5.875)
- `value_type`: `rate`
- `flag`: empty, `ocr_corrected` (read on the image, the Gallica OCR differs), `illegible`, or `not_applicable` (a date printed with text instead of a rate; the text is in `note_fr`)
- `note_fr`: text printed with the entry: a value cell holding text, or a line printed in the column before the entry (interruption of service)

## Footnote

Printed under the first page, against the title *Taxe de change (1)*: "(1) A l'égard des pays pour lesquels les titres sont émis en monnaie étrangère, elle ressort du taux de conversion (voir tableaux ci-après, pages 146 et 147)." Translation: (1) For the countries for which the money orders are issued in foreign currency, the exchange charge follows from the conversion rate (see the tables below, pages 146 and 147). The page numbers are those of sgt1922 (the Swiss and Greek tables).

## Validation

There are no totals. Checks made instead:

- Order of the dates down each country's column, in every printing: 28377 consecutive pairs checked; 121 anomalies (dates not increasing, or a misprinted year), kept as printed:
  - sgt1922 p.139 (f163) Grande-Bretagne: "3 août 1922" (55) printed after "4 août 1922" (56.50): dates not increasing
  - sgt1922 p.139 (f163) États-Unis d'Amérique: year printed 1822 in the Années column, read as 1922
  - sgt1922 p.141 (f165) Danemark: "6 juin 1919" (1.50) printed after "10 juin 1919" (1.52): dates not increasing
  - sgt1922 p.145 (f169) Norvège: "13 juillet 1922" (2.25) printed after "18 juillet 1922" (2.20): dates not increasing
  - sgt1922 p.147 (f171) Suisse: "7 mars 1922" (120) printed after "22 mars 1922" (125): dates not increasing
  - sgt1922 p.146 (f170) Grèce: "6 novembre 1915" (8) printed after "8 novembre 1915" (11): dates not increasing
  - sgt1922 p.147 (f171) Grèce: "9 février 1921" printed 10 between 20 and 20 (isolated jump)
  - sgt1923 p.145 (f647) Grande-Bretagne: "3 août 1922" (55) printed after "4 août 1922" (56.50): dates not increasing
  - sgt1923 p.145 (f647) États-Unis d'Amérique: year printed 1822 in the Années column, read as 1922
  - sgt1923 p.148 (f650) États-Unis d'Amérique: "9 novembre 1923" printed 48 between 17.50 and 18.50 (isolated jump)
  - sgt1923 p.151 (f653) Danemark: "6 juin 1919" (1.50) printed after "10 juin 1919" (1.52): dates not increasing
  - sgt1923 p.153 (f655) Suède: "25 janvier 1921" printed 20 between 3.37 and 3.13 (isolated jump)
  - sgt1923 p.155 (f657) Norvège: "13 juillet 1922" (2.25) printed after "18 juillet 1922" (2.20): dates not increasing
  - sgt1923 p.158 (f660) Suisse: "7 mars 1922" (120) printed after "22 mars 1922" (125): dates not increasing
  - sgt1923 p.157 (f659) Grèce: "6 novembre 1915" (8) printed after "8 novembre 1915" (11): dates not increasing
  - sgt1923 p.158 (f660) Grèce: "6 août 1923" (value cell prints only ») printed after "6 août 1923" (0.32): dates not increasing
  - sgt1923 p.158 (f660) Grèce: date printed "4 août 1923" out of sequence, read as 1923-08-14 (`period_fr` keeps the printed date)
  - sgt1923 p.158 (f660) Grèce: "9 février 1921" printed 10 between 20 and 20 (isolated jump)
  - sgt1924 p.147 (f1137) Grande-Bretagne: "3 août 1922" (55) printed after "4 août 1922" (56.50): dates not increasing
  - sgt1924 p.147 (f1137) États-Unis d'Amérique: year printed 1822 in the Années column, read as 1922
  - sgt1924 p.150 (f1140) États-Unis d'Amérique: "9 novembre 1923" printed 48 between 17.50 and 18.50 (isolated jump)
  - sgt1924 p.157 (f1147) Danemark: "6 juin 1919" (1.50) printed after "10 juin 1919" (1.52): dates not increasing
  - sgt1924 p.163 (f1153) Danemark: date printed "28 février 1924" out of sequence, read as 1924-04-28 (`period_fr` keeps the printed date)
  - sgt1924 p.159 (f1149) Suède: "25 janvier 1921" printed 20 between 3.37 and 3.13 (isolated jump)
  - sgt1924 p.161 (f1151) Norvège: "13 juillet 1922" (2.25) printed after "18 juillet 1922" (2.20): dates not increasing
  - sgt1924 p.162 (f1152) Norvège: date printed "28 février 1924" out of sequence, read as 1924-04-28 (`period_fr` keeps the printed date)
  - sgt1924 p.165 (f1155) Suisse: "7 mars 1922" (120) printed after "22 mars 1922" (125): dates not increasing
  - sgt1924 p.164 (f1154) Grèce: "6 novembre 1915" (8) printed after "8 novembre 1915" (11): dates not increasing
  - sgt1924 p.165 (f1155) Grèce: "6 août 1923" (value cell prints only ») printed after "6 août 1923" (0.32): dates not increasing
  - sgt1924 p.165 (f1155) Grèce: date printed "4 août 1923" out of sequence, read as 1923-08-14 (`period_fr` keeps the printed date)
  - sgt1924 p.165 (f1155) Grèce: "9 février 1921" printed 10 between 20 and 20 (isolated jump)
  - sgt1925 p.149 (f173) Grande-Bretagne: "3 août 1922" (55) printed after "4 août 1922" (56.50): dates not increasing
  - sgt1925 p.160 (f184) Grande-Bretagne: "5 décembre 1925" (127) printed after "5 décembre 1925" (128): dates not increasing
  - sgt1925 p.162 (f186) Danemark: "6 juin 1919" (1.50) printed after "10 juin 1919" (1.52): dates not increasing
  - sgt1925 p.168 (f192) Danemark: date printed "28 février 1924" out of sequence, read as 1924-04-28 (`period_fr` keeps the printed date)
  - sgt1925 p.168 (f192) Danemark: date printed "8 juillet 1925" out of sequence, read as 1925-08-08 (`period_fr` keeps the printed date)
  - sgt1925 p.166 (f190) Norvège: "13 juillet 1922" (2.25) printed after "18 juillet 1922" (2.20): dates not increasing
  - sgt1925 p.167 (f191) Norvège: date printed "28 février 1924" out of sequence, read as 1924-04-28 (`period_fr` keeps the printed date)
  - sgt1925 p.171 (f195) Suisse: "7 mars 1922" (120) printed after "22 mars 1922" (125): dates not increasing
  - sgt1925 p.170 (f194) Grèce: "6 novembre 1915" (8) printed after "8 novembre 1915" (11): dates not increasing
  - sgt1925 p.171 (f195) Grèce: "6 août 1923" (value cell prints only ») printed after "6 août 1923" (0.32): dates not increasing
  - sgt1925 p.171 (f195) Grèce: date printed "4 août 1923" out of sequence, read as 1923-08-14 (`period_fr` keeps the printed date)
  - sgt1925 p.171 (f195) Grèce: "9 février 1921" printed 10 between 20 and 20 (isolated jump)
  - sgt1926 p.159 (f723) Grande-Bretagne: "3 août 1922" (55) printed after "4 août 1922" (56.50): dates not increasing
  - sgt1926 p.170 (f734) Grande-Bretagne: "5 décembre 1925" (127) printed after "5 décembre 1925" (128): dates not increasing
  - sgt1926 p.176 (f740) Danemark: "6 juin 1919" (1.50) printed after "10 juin 1919" (1.52): dates not increasing
  - sgt1926 p.182 (f746) Danemark: date printed "28 février 1924" out of sequence, read as 1924-04-28 (`period_fr` keeps the printed date)
  - sgt1926 p.182 (f746) Danemark: date printed "8 juillet 1925" out of sequence, read as 1925-08-08 (`period_fr` keeps the printed date)
  - sgt1926 p.180 (f744) Norvège: "13 juillet 1922" (2.25) printed after "18 juillet 1922" (2.20): dates not increasing
  - sgt1926 p.181 (f745) Norvège: date printed "28 février 1924" out of sequence, read as 1924-04-28 (`period_fr` keeps the printed date)
  - sgt1926 p.186 (f750) Suisse: "7 mars 1922" (120) printed after "22 mars 1922" (125): dates not increasing
  - sgt1926 p.185 (f749) Grèce: "6 novembre 1915" (8) printed after "8 novembre 1915" (11): dates not increasing
  - sgt1926 p.186 (f750) Grèce: "6 août 1923" (value cell prints only ») printed after "6 août 1923" (0.32): dates not increasing
  - sgt1926 p.186 (f750) Grèce: date printed "4 août 1923" out of sequence, read as 1923-08-14 (`period_fr` keeps the printed date)
  - sgt1926 p.186 (f750) Grèce: "9 février 1921" printed 10 between 20 and 20 (isolated jump)
  - sgt1927 p.157 (f185) Grande-Bretagne: "3 août 1922" (55) printed after "4 août 1922" (56.50): dates not increasing
  - sgt1927 p.168 (f196) Grande-Bretagne: "5 décembre 1925" (127) printed after "5 décembre 1925" (128): dates not increasing
  - sgt1927 p.174 (f202) Danemark: "6 juin 1919" (1.50) printed after "10 juin 1919" (1.52): dates not increasing
  - sgt1927 p.179 (f207) Danemark: date printed "28 février 1924" out of sequence, read as 1924-02-27 (`period_fr` keeps the printed date)
  - sgt1927 p.179 (f207) Danemark: date printed "27 février 1924" out of sequence, read as 1924-02-28 (`period_fr` keeps the printed date)
  - sgt1927 p.180 (f208) Danemark: date printed "28 février 1924" out of sequence, read as 1924-04-28 (`period_fr` keeps the printed date)
  - sgt1927 p.180 (f208) Danemark: date printed "8 juillet 1925" out of sequence, read as 1925-08-08 (`period_fr` keeps the printed date)
  - sgt1927 p.178 (f206) Norvège: "13 juillet 1922" (2.25) printed after "18 juillet 1922" (2.20): dates not increasing
  - sgt1927 p.179 (f207) Norvège: date printed "28 février 1924" out of sequence, read as 1924-04-28 (`period_fr` keeps the printed date)
  - sgt1927 p.184 (f212) Suisse: "7 mars 1922" (120) printed after "22 mars 1922" (125): dates not increasing
  - sgt1927 p.183 (f211) Grèce: "6 novembre 1915" (8) printed after "8 novembre 1915" (11): dates not increasing
  - sgt1927 p.184 (f212) Grèce: "6 août 1923" (value cell prints only ») printed after "6 août 1923" (0.32): dates not increasing
  - sgt1927 p.184 (f212) Grèce: date printed "4 août 1923" out of sequence, read as 1923-08-14 (`period_fr` keeps the printed date)
  - sgt1927 p.184 (f212) Grèce: "9 février 1921" printed 10 between 20 and 20 (isolated jump)
  - sgt1928 p.157 (f709) Grande-Bretagne: "3 août 1922" (55) printed after "4 août 1922" (56.50): dates not increasing
  - sgt1928 p.168 (f720) Grande-Bretagne: "5 décembre 1925" (127) printed after "5 décembre 1925" (128): dates not increasing
  - sgt1928 p.159 (f711) Pays-Bas: date printed "13 septembre 1923" out of sequence, read as 1923-09-06 (`period_fr` keeps the printed date)
  - sgt1928 p.159 (f711) Pays-Bas: date printed "6 septembre 1923" out of sequence, read as 1923-09-13 (`period_fr` keeps the printed date)
  - sgt1928 p.174 (f726) Danemark: "6 juin 1919" (1.50) printed after "10 juin 1919" (1.52): dates not increasing
  - sgt1928 p.179 (f731) Danemark: date printed "28 février 1924" out of sequence, read as 1924-02-27 (`period_fr` keeps the printed date)
  - sgt1928 p.179 (f731) Danemark: date printed "27 février 1924" out of sequence, read as 1924-02-28 (`period_fr` keeps the printed date)
  - sgt1928 p.180 (f732) Danemark: date printed "28 février 1924" out of sequence, read as 1924-04-28 (`period_fr` keeps the printed date)
  - sgt1928 p.180 (f732) Danemark: date printed "8 juillet 1925" out of sequence, read as 1925-08-08 (`period_fr` keeps the printed date)
  - sgt1928 p.178 (f730) Norvège: "13 juillet 1922" (2.25) printed after "18 juillet 1922" (2.20): dates not increasing
  - sgt1928 p.179 (f731) Norvège: date printed "28 février 1924" out of sequence, read as 1924-04-28 (`period_fr` keeps the printed date)
  - sgt1928 p.184 (f736) Suisse: "7 mars 1922" (120) printed after "22 mars 1922" (125): dates not increasing
  - sgt1928 p.183 (f735) Grèce: "6 novembre 1915" (8) printed after "8 novembre 1915" (11): dates not increasing
  - sgt1928 p.184 (f736) Grèce: "6 août 1923" (value cell prints only ») printed after "6 août 1923" (0.32): dates not increasing
  - sgt1928 p.184 (f736) Grèce: date printed "4 août 1923" out of sequence, read as 1923-08-14 (`period_fr` keeps the printed date)
  - sgt1928 p.184 (f736) Grèce: "9 février 1921" printed 10 between 20 and 20 (isolated jump)
  - sgt1929 p.159 (f187) Grande-Bretagne: "3 août 1922" (55) printed after "4 août 1922" (56.50): dates not increasing
  - sgt1929 p.170 (f198) Grande-Bretagne: "5 décembre 1925" (127) printed after "5 décembre 1925" (128): dates not increasing
  - sgt1929 p.161 (f189) Pays-Bas: date printed "13 septembre 1923" out of sequence, read as 1923-09-06 (`period_fr` keeps the printed date)
  - sgt1929 p.161 (f189) Pays-Bas: date printed "6 septembre 1923" out of sequence, read as 1923-09-08 (`period_fr` keeps the printed date)
  - sgt1929 p.161 (f189) Pays-Bas: date printed "8 septembre 1923" out of sequence, read as 1923-09-13 (`period_fr` keeps the printed date)
  - sgt1929 p.176 (f204) Danemark: "6 juin 1919" (1.50) printed after "10 juin 1919" (1.52): dates not increasing
  - sgt1929 p.181 (f209) Danemark: date printed "28 février 1924" out of sequence, read as 1924-02-27 (`period_fr` keeps the printed date)
  - sgt1929 p.181 (f209) Danemark: date printed "27 février 1924" out of sequence, read as 1924-02-28 (`period_fr` keeps the printed date)
  - sgt1929 p.182 (f210) Danemark: date printed "28 février 1924" out of sequence, read as 1924-04-28 (`period_fr` keeps the printed date)
  - sgt1929 p.182 (f210) Danemark: date printed "8 juillet 1925" out of sequence, read as 1925-08-08 (`period_fr` keeps the printed date)
  - sgt1929 p.180 (f208) Norvège: "13 juillet 1922" (2.25) printed after "18 juillet 1922" (2.20): dates not increasing
  - sgt1929 p.181 (f209) Norvège: date printed "28 février 1924" out of sequence, read as 1924-04-28 (`period_fr` keeps the printed date)
  - sgt1929 p.186 (f214) Suisse: "7 mars 1922" (120) printed after "22 mars 1922" (125): dates not increasing
  - sgt1929 p.185 (f213) Grèce: "6 novembre 1915" (8) printed after "8 novembre 1915" (11): dates not increasing
  - sgt1929 p.186 (f214) Grèce: "6 août 1923" (value cell prints only ») printed after "6 août 1923" (0.32): dates not increasing
  - sgt1929 p.186 (f214) Grèce: date printed "4 août 1923" out of sequence, read as 1923-08-14 (`period_fr` keeps the printed date)
  - sgt1929 p.186 (f214) Grèce: "9 février 1921" printed 10 between 20 and 20 (isolated jump)
  - sgt1930 p.163 (f721) Grande-Bretagne: "3 août 1922" (55) printed after "4 août 1922" (56.50): dates not increasing
  - sgt1930 p.174 (f732) Grande-Bretagne: "5 décembre 1925" (127) printed after "5 décembre 1925" (128): dates not increasing
  - sgt1930 p.165 (f723) Pays-Bas: date printed "13 septembre 1923" out of sequence, read as 1923-09-06 (`period_fr` keeps the printed date)
  - sgt1930 p.165 (f723) Pays-Bas: date printed "6 septembre 1923" out of sequence, read as 1923-09-08 (`period_fr` keeps the printed date)
  - sgt1930 p.165 (f723) Pays-Bas: date printed "8 septembre 1923" out of sequence, read as 1923-09-13 (`period_fr` keeps the printed date)
  - sgt1930 p.180 (f738) Danemark: "6 juin 1919" (1.50) printed after "10 juin 1919" (1.52): dates not increasing
  - sgt1930 p.185 (f743) Danemark: date printed "28 février 1924" out of sequence, read as 1924-02-27 (`period_fr` keeps the printed date)
  - sgt1930 p.185 (f743) Danemark: date printed "27 février 1924" out of sequence, read as 1924-02-28 (`period_fr` keeps the printed date)
  - sgt1930 p.186 (f744) Danemark: date printed "28 février 1924" out of sequence, read as 1924-04-28 (`period_fr` keeps the printed date)
  - sgt1930 p.186 (f744) Danemark: date printed "8 juillet 1925" out of sequence, read as 1925-08-08 (`period_fr` keeps the printed date)
  - sgt1930 p.181 (f739) Suède: date printed "20 juin 1920" out of sequence, read as 1920-06-13 (`period_fr` keeps the printed date)
  - sgt1930 p.181 (f739) Suède: date printed "13 juin 1920" out of sequence, read as 1920-06-20 (`period_fr` keeps the printed date)
  - sgt1930 p.184 (f742) Norvège: "13 juillet 1922" (2.25) printed after "18 juillet 1922" (2.20): dates not increasing
  - sgt1930 p.185 (f743) Norvège: date printed "28 février 1924" out of sequence, read as 1924-04-28 (`period_fr` keeps the printed date)
  - sgt1930 p.190 (f748) Suisse: "7 mars 1922" (120) printed after "22 mars 1922" (125): dates not increasing
  - sgt1930 p.189 (f747) Grèce: "6 novembre 1915" (8) printed after "8 novembre 1915" (11): dates not increasing
  - sgt1930 p.190 (f748) Grèce: "6 août 1923" (value cell prints only ») printed after "6 août 1923" (0.32): dates not increasing
  - sgt1930 p.190 (f748) Grèce: date printed "4 août 1923" out of sequence, read as 1923-08-14 (`period_fr` keeps the printed date)
  - sgt1930 p.190 (f748) Grèce: "9 février 1921" printed 10 between 20 and 20 (isolated jump)

- Validity periods: `date_to` is derived from the next later date, so the stored periods are continuous and do not overlap by construction, except where a date is printed twice (both rows keep an empty `date_to`). Intervals longer than a year between two consecutive dates of a country (not gaps in the transcription: the next date printed is that far):
  - États-Unis d'Amérique: 1917-07-05 to 1918-08-30
  - États-Unis d'Amérique: 1928-07-16 to 1929-10-10
  - Pays-Bas: 1927-05-05 to 1928-07-16
  - Pays-Bas: 1928-07-16 to 1929-10-10
  - Danemark: 1927-05-05 to 1928-07-16
  - Suède: 1927-05-06 to 1928-07-16
  - Suède: 1928-07-16 to 1929-10-10
  - Norvège: 1928-07-16 to 1929-10-10
  - Suisse: 1927-05-06 to 1928-07-16
  - Suisse: 1928-07-16 to 1929-10-10
  - Grèce: 1915-12-02 to 1917-10-09 (Service suspendu du mois d'octobre 1916 au mois de juillet 1917)
  - Grèce: 1917-10-09 to 1918-12-31

- Overlapping printings: 24654 dates compared with another edition printing the same country-year; 18 value differences; 0 dates printed in one edition but not in the other.

| country | date | edition | printed (page) | stored from | printed (page) |
|---|---|---|---|---|---|
| États-Unis d'Amérique | 1923-11-09 | sgt1923 | 48 (p. 148) | sgt1930 | 18 (p. 166) |
| États-Unis d'Amérique | 1923-11-09 | sgt1924 | 48 (p. 150) | sgt1930 | 18 (p. 166) |
| Suède | 1920-06-20 | sgt1922 | 2.83 (p. 142) | sgt1930 | 2.82 (p. 181) |
| Suède | 1921-01-25 | sgt1923 | 20 (p. 153) | sgt1930 | 3.20 (p. 182) |
| Suède | 1921-01-25 | sgt1924 | 20 (p. 159) | sgt1930 | 3.20 (p. 182) |
| Norvège | 1924-02-20 | sgt1924 | 3.15 (p. 162) | sgt1930 |  (p. 185) |
| Norvège | 1924-08-13 | sgt1924 | 2.55 (p. 163) | sgt1930 | 2.25 (p. 186) |
| Norvège | 1924-02-20 | sgt1925 | 3.15 (p. 167) | sgt1930 |  (p. 185) |
| Norvège | 1924-08-13 | sgt1925 | 2.55 (p. 168) | sgt1930 | 2.25 (p. 186) |
| Norvège | 1924-02-20 | sgt1926 | 3.15 (p. 181) | sgt1930 |  (p. 185) |
| Norvège | 1924-08-13 | sgt1926 | 2.55 (p. 182) | sgt1930 | 2.25 (p. 186) |
| Norvège | 1924-02-20 | sgt1927 | 3.15 (p. 179) | sgt1930 |  (p. 185) |
| Norvège | 1924-08-13 | sgt1927 | 2.55 (p. 180) | sgt1930 | 2.25 (p. 186) |
| Norvège | 1924-02-20 | sgt1928 | 3.15 (p. 179) | sgt1930 |  (p. 185) |
| Norvège | 1924-08-13 | sgt1928 | 2.55 (p. 180) | sgt1930 | 2.25 (p. 186) |
| Norvège | 1924-02-20 | sgt1929 | 3.15 (p. 181) | sgt1930 |  (p. 185) |
| Norvège | 1924-08-13 | sgt1929 | 2.55 (p. 182) | sgt1930 | 2.25 (p. 186) |
| Grèce | 1921-05-08 | sgt1922 | 0.95 (p. 147) | sgt1930 | 0.59 (p. 190) |

- Values taken from another edition's printing (`reprint_corrected`):
  - sgt1930 p.185 Norvège 20 février 1924: printed "?", value 3.15 taken from sgt1929 p.181 (reprint_corrected)
  - sgt1930 p.186 Norvège 13 août 1924: printed "2.25", value 2.55 taken from sgt1929 p.182 (reprint_corrected)

- Years not printed in the *Années* column (a dash where the year changes), inferred from the order of the dates:
  - sgt1923 p.155 (f657) Danemark: 1923
  - sgt1923 p.155 (f657) Suède: 1923
  - sgt1923 p.155 (f657) Norvège: 1923
  - sgt1923 p.158 (f660) Grèce: 1923
  - sgt1924 p.161 (f1151) Danemark: 1923
  - sgt1924 p.161 (f1151) Suède: 1923
  - sgt1924 p.161 (f1151) Norvège: 1923
  - sgt1924 p.163 (f1153) Danemark: 1924
  - sgt1924 p.165 (f1155) Grèce: 1923
  - sgt1925 p.159 (f183) Grande-Bretagne: 1925
  - sgt1925 p.160 (f184) Grande-Bretagne: 1925
  - sgt1925 p.161 (f185) Grande-Bretagne: 1925
  - sgt1925 p.166 (f190) Danemark: 1923
  - sgt1925 p.166 (f190) Suède: 1923
  - sgt1925 p.166 (f190) Norvège: 1923
  - sgt1925 p.168 (f192) Danemark: 1924
  - sgt1925 p.171 (f195) Grèce: 1923
  - sgt1926 p.169 (f733) Grande-Bretagne: 1925
  - sgt1926 p.180 (f744) Danemark: 1923
  - sgt1926 p.180 (f744) Suède: 1923
  - sgt1926 p.180 (f744) Norvège: 1923
  - sgt1926 p.182 (f746) Danemark: 1924
  - sgt1926 p.186 (f750) Grèce: 1923
  - sgt1927 p.167 (f195) Grande-Bretagne: 1925
  - sgt1927 p.178 (f206) Danemark: 1923
  - sgt1927 p.178 (f206) Suède: 1923
  - sgt1927 p.178 (f206) Norvège: 1923
  - sgt1927 p.180 (f208) Danemark: 1924
  - sgt1927 p.184 (f212) Grèce: 1923
  - sgt1928 p.167 (f719) Grande-Bretagne: 1925
  - sgt1928 p.178 (f730) Danemark: 1923
  - sgt1928 p.178 (f730) Suède: 1923
  - sgt1928 p.178 (f730) Norvège: 1923
  - sgt1928 p.180 (f732) Danemark: 1924
  - sgt1928 p.184 (f736) Grèce: 1923
  - sgt1929 p.169 (f197) Grande-Bretagne: 1925
  - sgt1929 p.180 (f208) Danemark: 1923
  - sgt1929 p.180 (f208) Suède: 1923
  - sgt1929 p.180 (f208) Norvège: 1923
  - sgt1929 p.182 (f210) Danemark: 1924
  - sgt1929 p.186 (f214) Grèce: 1923
  - sgt1930 p.173 (f731) Grande-Bretagne: 1925
  - sgt1930 p.184 (f742) Danemark: 1923
  - sgt1930 p.184 (f742) Suède: 1923
  - sgt1930 p.184 (f742) Norvège: 1923
  - sgt1930 p.186 (f744) Danemark: 1924
  - sgt1930 p.190 (f748) Grèce: 1923

## Doubts

- sgt1923 p.158 (f660), Grèce, 15 January to 8 October 1923: the value column is printed without the leading dash and drifts upwards against the dates (by about two thirds of a line at the foot). There are 36 dates and 36 value cells (one of them a bare "»"), so dates and values were paired in order. sgt1924 p.165 (f1155) reprints these entries with values and dates aligned line by line and gives the same pairing for every date.
- Grèce, 8 May 1921: sgt1922 prints 0.95, sgt1923 0.59 (digits transposed in one of them; the next values are 0.80, 0.95, 0.90); sgt1924 repeats 0.59. The latest printing is stored, as for every other difference.
- États-Unis, 9 November 1923: sgt1923 and sgt1924 print "48 »" between 17.50 and 18.50; sgt1925-sgt1930 print 18, which is stored.
- Danemark, July 1926 (sgt1926-sgt1930): two value lines, 10 80 and 11 », are printed with no date between "24 juillet" and "31 juillet" (probably the 28 and 29 juillet printed for the other countries). Having no date, they are not stored.
- Norvège, 20 February 1924 (sgt1930 p.185): the value is printed "3 5" (a digit missing); 3.15 is taken from sgt1929, which agrees with sgt1924-sgt1928. Norvège, 13 August 1924: sgt1930 prints 2.25 and sgt1924-sgt1929 print 2.55 (between 2.65 and 2.60); 2.55 is taken from sgt1929. Both are flagged reprint_corrected.
- Dates printed out of order (13/6/8 September 1923 for Pays-Bas in sgt1928-sgt1930, 20/13 June 1920 for Suède in sgt1930, 28/27 February 1924 for Danemark in sgt1927-sgt1930, "28 février" for 28 avril 1924, "8 juillet" for 8 août 1925) are paired with their values as printed and read in date sequence. The earlier printings give the same date-value pairs in order. `period_fr` keeps the printed date.
- The 1923 sub-column of the Swiss table (sgt1930 p.191) has values that drift upwards against the dates. Dates and values (67 of each) were paired in order, and every other printing gives the same pairs.

- Flagged cells: not_applicable: 2, reprint_corrected: 2.
  - sgt1930 p.185 Norvège 20 février 1924: 3.15 (reprint_corrected)
  - sgt1930 p.186 Norvège 13 août 1924: 2.55 (reprint_corrected)
  - sgt1930 p.190 Grèce 27 avril 1921: NA (not_applicable; Cours norm.)
  - sgt1930 p.190 Grèce 6 août 1923: NA (not_applicable; value cell prints only »)

## Image versus OCR

Every entry of every transcribed printing was read on native-resolution crops of the page image (strips of about 40 lines at full resolution, zoomed crops for doubtful digits); every section is marked `img: all`. The Gallica word OCR reads most rates but few dates; it was used only as a cross-check (`extract_posts_exchange.py qa`). Cells flagged `ocr_corrected`: 0.
