#' Harmonized Tunisian Census Panel, 2014--2024
#'
#' Delegation-level data harmonizing the 2014 and 2024 Tunisian RGPH.
#' Contains 45 socioeconomic indicators with `_2014`, `_2024`, and
#' `_change` suffixes. All percentages on a 0--100 scale.
#'
#' @format A data frame with 281 rows and 144 columns. Nine identifier
#'   columns (governorate, delegation names in French and Arabic, region,
#'   coordinates, match flag) plus 45 indicators x 3 suffixes = 135
#'   indicator columns. See \code{\link{codebook}} for variable details.
#'
#' @source Institut National de la Statistique (INS), Republic of Tunisia.
#'   RGPH 2014 and RGPH 2024.
#'
#' @examples
#' data(census_panel)
#' dim(census_panel)
#' aggregate(unemployment_rate_change ~ region_2024,
#'           data = census_panel, FUN = mean, na.rm = TRUE)
"census_panel"


#' Delegation Name Crosswalk, 2014--2024
#'
#' Maps 263 delegation names from the 2014 RGPH to their 2024 equivalents
#' (193 exact matches, 70 fuzzy matches within governorates).
#'
#' @format A data frame with 263 rows and 5 columns:
#' \describe{
#'   \item{delegation_2014}{Delegation name, 2014 spelling.}
#'   \item{gov_2014}{Governorate name, 2014 spelling.}
#'   \item{delegation_2024}{Delegation name, 2024 spelling.}
#'   \item{gov_2024}{Governorate name, 2024 spelling.}
#'   \item{match_type}{\code{"exact"} or \code{"fuzzy"}.}
#' }
#'
#' @source Constructed from delegation lists in the 2014 and 2024 RGPH
#'   files (INS Tunisia).
#'
#' @examples
#' data(delegation_crosswalk)
#' table(delegation_crosswalk$match_type)
"delegation_crosswalk"


#' Codebook: Variable-Level Metadata
#'
#' Documents all 45 harmonized indicators in \code{\link{census_panel}}.
#'
#' @format A data frame with 45 rows and 5 columns:
#' \describe{
#'   \item{variable}{Harmonized variable stem (without `_2014`/`_2024`/`_change`).}
#'   \item{domain}{Thematic domain.}
#'   \item{label}{Human-readable description.}
#'   \item{unit}{"percentage (0-100)" or "count".}
#'   \item{note}{Denominator, data gaps, or comparability caveats.}
#' }
#'
#' @source Constructed during harmonization. See
#'   \code{system.file("extdata", "harmonization_log.md", package = "tncensus")}
#'
#' @examples
#' data(codebook)
#' unique(codebook$domain)
"codebook"
