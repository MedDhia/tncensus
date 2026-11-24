#' Load Tunisia Administrative Boundaries (GeoJSON)
#'
#' Loads simplified GeoJSON administrative boundary polygons for Tunisia at
#' the national, region, governorate, or delegation level as an \code{sf}
#' object. Requires the \pkg{sf} package.
#'
#' @param level Character. Administrative level: \code{"delegations"} (264
#'   features), \code{"governorates"} (24 features), \code{"regions"} (6
#'   features), or \code{"national"} (1 feature).
#'
#' @return An \code{sf} spatial data frame with English identifier columns
#'   (\code{delegation_code}, \code{governorate_code}, \code{region_code},
#'   etc.) and polygon geometries.
#'
#' @examples
#' if (requireNamespace("sf", quietly = TRUE)) {
#'   gov_sf <- load_geojson("governorates")
#'   nrow(gov_sf)
#' }
#'
#' @export
load_geojson <- function(level = c("delegations", "governorates", "regions", "national")) {
  level <- match.arg(level)
  if (!requireNamespace("sf", quietly = TRUE)) {
    stop(
      "Package 'sf' is required to load GeoJSON boundaries. ",
      "Install it with install.packages('sf').",
      call. = FALSE
    )
  }
  path <- system.file(
    "extdata", "geo", paste0(level, ".geojson"),
    package = "tncensus", mustWork = TRUE
  )
  sf::st_read(path, quiet = TRUE)
}
