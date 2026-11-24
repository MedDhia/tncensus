## Resubmission / Consolidation Note

Per CRAN reviewer feedback on `rgph2024tn` (asking to consolidate similar
Tunisian census packages into a single package and to replace `\dontrun{}`
with `\donttest{}` or unwrapped examples):

* Consolidated `rgph2014tn`, `rgph2024tn`, and `tncensus` into this single
  unified `tncensus` package (version 1.0.0).
* Replaced `\dontrun{}` in `download_secteurs()` with `\donttest{}`; all
  other examples are unwrapped and run in < 5 seconds.

## R CMD check results

0 errors | 0 warnings (with pandoc vignette build) | 1 note (New submission)
