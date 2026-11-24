#' List Tables from the 1906 and 1931 Colonial Census Publications
#'
#' Returns an index of the tables transcribed from two census publications
#' digitized on Gallica (BnF): the 1906 census of the European civilian
#' population of Tunisia and the 1931 census of the indigenous (Muslim and
#' Jewish) population. Each table can be loaded with
#' \code{\link{load_colonial_census}}.
#'
#' @return A \code{data.frame} with one row per table and columns
#'   \code{table} (name to pass to \code{load_colonial_census()}),
#'   \code{census} (\code{"eur1906"} or \code{"ind1931"}), \code{table_id}
#'   (table number or letter as printed), \code{title_fr}, \code{title_en},
#'   \code{pages} (printed pages), \code{gallica_ark}, \code{n_rows}, and
#'   \code{value_type} (\code{"count"}, \code{"percent"}, or
#'   \code{"rate"}).
#'
#' @seealso \code{\link{load_colonial_census}}
#' @export
#'
#' @examples
#' idx <- colonial_census_tables()
#' idx[, c("table", "title_en", "n_rows")]
colonial_census_tables <- function() {
  path <- system.file("extdata", "colonial", "index.parquet",
                      package = "tncensus")
  if (path == "") {
    stop("Colonial census index not found in package installation.",
         call. = FALSE)
  }
  as.data.frame(arrow::read_parquet(path))
}


#' Load a Table from the 1906 or 1931 Colonial Census Publications
#'
#' Loads one table transcribed from the original publications of the 1906
#' census of the European civilian population of Tunisia (\emph{Dénombrement
#' de la population européenne civile en Tunisie au 16 décembre 1906}) or the
#' 1931 census of the indigenous population (\emph{Dénombrement de la
#' population civile indigène (musulmane et israélite) en Tunisie au 22 mars
#' 1931}), as digitized on Gallica.
#'
#' @param table Character string. Name of the table. Use
#'   \code{\link{colonial_census_tables}()} to list the available tables.
#'
#' @return A tidy \code{data.frame} with one row per cell of the printed
#'   table. Every table has the columns \code{census}, \code{table_id},
#'   \code{source_page} (printed page), \code{gallica_view} (Gallica page
#'   view, for checking a value against the scan), \code{value} and
#'   \code{flag}. Geography columns (\code{controle_civil}, \code{annexe},
#'   \code{caidat}, \code{cheikhat}, \code{locality}, \code{commune}) keep the
#'   place names as printed. Dimension columns (e.g. \code{nationality},
#'   \code{religion}, \code{sex}) hold English codes, each paired with a
#'   \code{*_fr} column holding the printed French label.
#'
#' @details
#' The tables were rebuilt from Gallica's word-level OCR and checked against
#' every printed row and column total; values that the OCR misread were
#' corrected from the page images. \code{flag} is empty for values taken
#' directly from the OCR, \code{"ocr_corrected"} for values corrected from
#' the scan, \code{"illegible"} for values that could not be read (left
#' \code{NA}), \code{"total_mismatch"} where the printed values do not
#' add up to the printed total (the printed value is kept),
#' \code{"derived_from_totals"} for cells lost in the binding and derived
#' from the printed totals, and \code{"not_applicable"} for questions not
#' asked of a group (left \code{NA}). Printed subtotals and totals are not stored as
#' rows. A printed \code{»} is recorded as 0.
#'
#' Place names are not harmonized with modern delegations; see
#' \code{\link{historical_geonames}} for a crosswalk of historical names.
#' Some figures overlap \code{\link{colonial_european_pop}},
#' \code{\link{colonial_tunisian_pop}} and
#' \code{\link{colonial_age_caidat_1931}}, which come from a different
#' transcription (Ben Salah et al., 2024).
#'
#' The tables are stored as Zstandard-compressed Apache Parquet files in
#' \code{inst/extdata/colonial}. The transcription scripts and per-table
#' notes are in \code{data-raw/colonial_census} in the package repository.
#'
#' @source Régence de Tunis, Direction de l'agriculture, du commerce et de la
#'   colonisation (1907). \emph{Dénombrement de la population européenne
#'   civile en Tunisie au 16 décembre 1906}. Tunis: Imprimerie moderne.
#'   Source gallica.bnf.fr / Bibliothèques de l'Université de Poitiers,
#'   \url{https://gallica.bnf.fr/ark:/12148/bd6t53563851}.
#'
#'   Tunisie, Direction générale de l'intérieur (1932). \emph{Dénombrement de
#'   la population civile indigène (musulmane et israélite) en Tunisie au 22
#'   mars 1931}. Tunis: Impr. J. Aloccio. Source gallica.bnf.fr /
#'   Bibliothèque nationale de France,
#'   \url{https://gallica.bnf.fr/ark:/12148/bpt6k994559s}.
#'
#' @seealso \code{\link{colonial_census_tables}}
#' @export
#' @importFrom arrow read_parquet
#'
#' @examples
#' # European population by nationality and locality, 1906
#' loc <- load_colonial_census("eur1906_t2_locality_nationality")
#' head(loc)
#'
#' # Indigenous population by cheikhat, 1931
#' ch <- load_colonial_census("ind1931_t3_cheikhat_nationality")
#' tapply(ch$value, ch$religion, sum)
load_colonial_census <- function(table) {
  idx <- colonial_census_tables()
  if (!is.character(table) || length(table) != 1L || !table %in% idx$table) {
    stop(
      sprintf(
        "Table '%s' not found. Use colonial_census_tables() to list tables.",
        paste(table, collapse = ", ")
      ),
      call. = FALSE
    )
  }
  path <- system.file("extdata", "colonial", paste0(table, ".parquet"),
                      package = "tncensus")
  if (path == "") {
    stop(sprintf("Data file for table '%s' not found.", table), call. = FALSE)
  }
  as.data.frame(arrow::read_parquet(path))
}
