#' List Available 2014 RGPH Data Sheets
#'
#' Returns a character vector of all disaggregated 2014 RGPH data sheet names
#' available in the package. These correspond to the original Excel worksheets
#' from the INS publication and can be loaded with \code{\link{rgph_load_sheet}}.
#'
#' @return A character vector of sheet names.
#'
#' @export
#'
#' @examples
#' rgph_sheets()
rgph_sheets <- function() {
  c(
    "master_merged", "demo1", "demo2", "educ1", "educ2",
    "emploi1", "emploi2", "emploi2_1", "emploi3", "emploi3_1",
    "mig_ext", "mig_inter",
    "menage_water", "menage_energy", "menage_tenure",
    "menage_entertainment", "menage_equipment", "menage_communication",
    "log_type", "log_rooms", "log_area", "log_occupation",
    "log_infrastructure", "log_facilities",
    "log_dist_primary", "log_dist_college", "log_dist_health",
    "log_dist_sports"
  )
}


#' Load a Disaggregated 2014 RGPH Data Sheet
#'
#' Loads one of the 28 available 2014 RGPH data sheets as a \code{data.frame}.
#' These sheets include disaggregations by sex (\code{male}, \code{female},
#' \code{total}), milieu (\code{communal}, \code{non_communal}, \code{total}),
#' and geographic level that are not present in the pre-merged
#' \code{\link{rgph_master}} dataset.
#'
#' @param sheet Character string. Name of the sheet to load. Use
#'   \code{\link{rgph_sheets}()} to see all available names.
#'
#' @return A \code{data.frame}.
#'
#' @details
#' The sheets are stored as Zstandard-compressed Apache Parquet files in
#' \code{inst/extdata/rgph2014} and are read with
#' \code{\link[arrow]{read_parquet}}. Sheet names match the original Excel
#' worksheet names.
#'
#' @export
#' @importFrom arrow read_parquet
#'
#' @examples
#' # Load demographic data disaggregated by sex and milieu
#' demo <- rgph_load_sheet("demo1")
#' head(demo)
#'
#' # Load employment data
#' emp <- rgph_load_sheet("emploi1")
#' dim(emp)
rgph_load_sheet <- function(sheet) {
  available <- rgph_sheets()
  if (!sheet %in% available) {
    stop(
      sprintf(
        "Sheet '%s' not found. Use rgph_sheets() to see available sheets.",
        sheet
      ),
      call. = FALSE
    )
  }
  path <- system.file(
    "extdata", "rgph2014", paste0(sheet, ".parquet"),
    package = "tncensus"
  )
  if (path == "") {
    stop(
      sprintf(
        "Data file for sheet '%s' not found in package installation.",
        sheet
      ),
      call. = FALSE
    )
  }
  as.data.frame(arrow::read_parquet(path))
}


#' 2014 RGPH Variable Codebook
#'
#' Returns a \code{data.frame} documenting every variable in
#' \code{\link{rgph_master}}, including the variable name, a
#' human-readable label in English, the thematic domain, the unit of
#' measurement, and a note on the denominator population where applicable.
#'
#' @return A \code{data.frame} with columns \code{variable}, \code{label},
#'   \code{domain}, \code{unit}, and \code{denominator}.
#'
#' @export
#'
#' @examples
#' cb <- rgph_codebook()
#' head(cb, 10)
#'
#' # Find all employment variables
#' cb[cb$domain == "employment", ]
rgph_codebook <- function() {
  path <- system.file(
    "extdata", "rgph2014", "codebook.parquet",
    package = "tncensus"
  )
  if (path == "") {
    stop("Codebook file not found in package installation.", call. = FALSE)
  }
  as.data.frame(arrow::read_parquet(path))
}
