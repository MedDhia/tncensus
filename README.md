# tncensus

<!-- badges: start -->
[![CRAN status](https://www.r-pkg.org/badges/version/tncensus)](https://CRAN.R-project.org/package=tncensus)
[![R-CMD-check](https://github.com/MedDhia/tncensus/actions/workflows/R-CMD-check.yaml/badge.svg)](https://github.com/MedDhia/tncensus/actions/workflows/R-CMD-check.yaml)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
<!-- badges: end -->

Harmonized delegation-level data from Tunisia's 2014 and 2024 General
Population and Housing Censuses (RGPH).

## Installation

``` r
# From CRAN (when available):
install.packages("tncensus")

# Development version from GitHub:
# install.packages("pak")
pak::pak("MedDhia/tncensus")
```

## Quick start

``` r
library(tncensus)
data("census_panel")
data("codebook")

head(census_panel[, 1:12])
codebook[codebook$domain == "Employment", ]

# Largest unemployment increases
census_panel[order(-census_panel$unemployment_rate_change),
  c("governorate", "delegation_fr_2014",
    "unemployment_rate_2014", "unemployment_rate_2024",
    "unemployment_rate_change")][1:10, ]
```

## Datasets

| Dataset | Rows | Cols | Description |
|---------|------|------|-------------|
| `census_panel` | 281 | 144 | `_2014`, `_2024`, `_change` for 45 indicators |
| `delegation_crosswalk` | 263 | 5 | Name mapping between census waves |
| `codebook` | 45 | 5 | Variable metadata |

## Before CRAN submission

Generate `.rda` files for lazy loading (requires R):

``` bash
Rscript data-raw/build_rda.R
R CMD build .
R CMD check tncensus_0.1.0.tar.gz --as-cran
```

## Data source

Institut National de la Statistique (INS), Republic of Tunisia.
RGPH 2014 and RGPH 2024.

## License

CC BY 4.0. Attribution to INS Tunisia required.

## Related packages

Part of a suite of R packages for Tunisian census data:

- [rgph2014tn](https://github.com/MedDhia/rgph2014tn) — raw 2014 RGPH data
- [rgph2024tn](https://github.com/MedDhia/rgph2024tn) — raw 2024 RGPH data
- **tncensus** (this package) — harmonized 2014-2024 panel

More at <https://mohameddhiahammami.com/data>
