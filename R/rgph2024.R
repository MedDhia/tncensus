#' Load Tunisia 2024 Census Data
#'
#' Load 2024 RGPH data at one of four administrative levels. Delegation,
#' governorate, and national data are bundled with the package.
#' Sector-level data must be downloaded once via
#' \code{\link{download_sectors}}.
#'
#' @return A \code{data.frame}. Column names use dot-separated English
#'   indicator paths (e.g., \code{"utility_connections.total.SONEDE"}).
#'
#' @examples
#' del <- load_delegations()
#' nrow(del)
#' head(names(del), 10)
#'
#' @name load_data
#' @importFrom arrow read_parquet
#' @importFrom utils read.csv download.file
NULL

.pkg_env <- new.env(parent = emptyenv())

.load_bundled <- function(name) {
  path <- system.file("extdata", "rgph2024", paste0(name, ".parquet"),
                      package = "tncensus", mustWork = TRUE)
  as.data.frame(arrow::read_parquet(path))
}

#' @rdname load_data
#' @export
load_delegations <- function() {
  if (is.null(.pkg_env$delegations))
    .pkg_env$delegations <- .load_bundled("delegations")
  .pkg_env$delegations
}

#' @rdname load_data
#' @export
load_governorates <- function() {
  if (is.null(.pkg_env$governorates))
    .pkg_env$governorates <- .load_bundled("governorates")
  .pkg_env$governorates
}

#' @rdname load_data
#' @export
load_national <- function() {
  if (is.null(.pkg_env$national))
    .pkg_env$national <- .load_bundled("national")
  .pkg_env$national
}

#' @param cache_dir Character. Directory where \code{secteurs.csv.gz} is cached.
#' @rdname load_data
#' @export
load_sectors <- function(cache_dir = tools::R_user_dir("tncensus", which = "cache")) {
  path <- file.path(cache_dir, "secteurs.csv.gz")
  if (!file.exists(path)) {
    stop("Sector data not found. Run download_sectors() first.",
         call. = FALSE)
  }
  if (is.null(.pkg_env$sectors) || !identical(.pkg_env$sectors_path, path)) {
    con <- gzfile(path, open = "rt")
    on.exit(close(con))
    .pkg_env$sectors <- utils::read.csv(
      con, check.names = FALSE, stringsAsFactors = FALSE
    )
    .pkg_env$sectors_path <- path
  }
  .pkg_env$sectors
}

#' Download 2024 Sector-Level Data
#'
#' Downloads the 2024 RGPH sector dataset (6.5 MB compressed) to the package
#' cache directory. Only needed once; subsequent calls to
#' \code{\link{load_sectors}} use the cached file.
#'
#' @param url Character. URL to download from.
#' @param force Logical. Re-download even if already cached.
#' @param quiet Logical. Suppress progress output.
#'
#' @return The local file path (invisibly).
#'
#' @examples
#' \donttest{
#' download_sectors()
#' sec <- load_sectors()
#' nrow(sec)
#' }
#'
#' @export
download_sectors <- function(
    url = "https://data.mohameddhiahammami.com/secteurs.csv.gz",
    force = FALSE,
    quiet = FALSE
) {
  cache_dir <- tools::R_user_dir("tncensus", which = "cache")
  if (!dir.exists(cache_dir)) dir.create(cache_dir, recursive = TRUE)
  dest <- file.path(cache_dir, "secteurs.csv.gz")
  if (file.exists(dest) && !force) {
    message("Already downloaded: ", dest)
    return(invisible(dest))
  }
  message("Downloading sector data (6.5 MB)...")
  utils::download.file(url, dest, mode = "wb", quiet = quiet)
  message("Saved to: ", dest)
  .pkg_env$sectors <- NULL
  invisible(dest)
}


#' Access 2024 RGPH Administrative Units
#'
#' Filter 2024 RGPH data by administrative code, name, or region.
#'
#' @param code Integer or character administrative code.
#' @param name Character substring to match (case-insensitive) against the
#'   unit name column.
#' @param region Character. Exact region name (e.g., \code{"Centre Ouest"}).
#'
#' @return A \code{data.frame} containing the matching rows.
#'
#' @examples
#' get_governorate(11)
#' get_governorate(name = "Sfax")
#' get_delegation(1151)
#' nrow(get_region("Centre Ouest"))
#'
#' @name accessors
NULL

#' @rdname accessors
#' @export
get_governorate <- function(code = NULL, name = NULL) {
  df <- load_governorates()
  if (!is.null(code)) df <- df[df$governorate_code == as.integer(code), , drop = FALSE]
  if (!is.null(name)) df <- df[grepl(tolower(name), tolower(df$governorate_name), fixed = TRUE), , drop = FALSE]
  df
}

#' @rdname accessors
#' @export
get_delegation <- function(code = NULL, name = NULL) {
  df <- load_delegations()
  if (!is.null(code)) df <- df[df$delegation_code == as.integer(code), , drop = FALSE]
  if (!is.null(name)) df <- df[grepl(tolower(name), tolower(df$delegation_name), fixed = TRUE), , drop = FALSE]
  df
}

#' @rdname accessors
#' @export
get_sector <- function(code = NULL, name = NULL) {
  df <- load_sectors()
  if (!is.null(code)) df <- df[df$sector_code == as.integer(code), , drop = FALSE]
  if (!is.null(name)) df <- df[grepl(tolower(name), tolower(df$sector_name), fixed = TRUE), , drop = FALSE]
  df
}

#' @rdname accessors
#' @export
get_region <- function(region) {
  df <- load_delegations()
  df[df$region == region, , drop = FALSE]
}


.geo_cols <- c(
  "governorate_code", "governorate_name", "governorate_ar", "region",
  "district_name", "department_code", "delegation_code", "delegation_name",
  "delegation_ar", "delegation_id_salb_un", "sector_code", "sector_name",
  "sector_ar", "milieu", "lat", "lon", "delegation_lat", "delegation_lon",
  "entity"
)

.get_loader <- function(level) {
  level <- match.arg(level, c("delegations", "governorates", "sectors", "national"))
  switch(level,
    delegations  = load_delegations,
    governorates = load_governorates,
    sectors      = load_sectors,
    national     = load_national
  )
}

#' Search and List 2024 RGPH Indicators
#'
#' Discover indicator prefixes and full column names in the 2024 RGPH datasets.
#'
#' @param level Character. Administrative level: \code{"delegations"},
#'   \code{"governorates"}, \code{"sectors"}, or \code{"national"}.
#' @param pattern Character. Case-insensitive regular expression pattern to
#'   match against column names.
#'
#' @return A character vector of indicator prefixes (\code{list_indicators})
#'   or matching column names (\code{search_indicator}).
#'
#' @examples
#' head(list_indicators(), 10)
#' head(search_indicator("delegations", "unemployment"), 10)
#'
#' @name search
NULL

#' @rdname search
#' @export
list_indicators <- function(level = "delegations") {
  df <- .get_loader(level)()
  sort(unique(sub("\\..*$", "", setdiff(names(df), .geo_cols))))
}

#' @rdname search
#' @export
search_indicator <- function(level = "delegations", pattern = "") {
  df <- .get_loader(level)()
  grep(pattern, names(df), value = TRUE, ignore.case = TRUE)
}

#' 2024 RGPH Indicator Codebook
#'
#' Returns a \code{data.frame} documenting the 50 thematic indicators in the
#' 2024 RGPH datasets, their domain, description, and deepest available
#' administrative level.
#'
#' @param domain Optional character string to filter by thematic domain
#'   (e.g., \code{"education"}, \code{"housing"}, \code{"employment"}).
#'
#' @return A \code{data.frame} (invisibly) with columns \code{indicator},
#'   \code{domain}, \code{description}, and \code{deepest_level}.
#'
#' @examples
#' cb <- rgph2024_codebook()
#' head(cb)
#' rgph2024_codebook("education")
#'
#' @export
rgph2024_codebook <- function(domain = NULL) {
  cb <- data.frame(
    indicator = c(
      "education_level", "illiteracy", "school_attendance",
      "school_attendance_3_17", "enrollment_6_14",
      "children_education_10_17", "marital_status", "children_age_sex",
      "housing_type", "construction_period", "rooms_housing",
      "rooms_used", "floor_area", "bathroom", "kitchen",
      "toilet", "toilet_flush", "housing_occupancy",
      "household_tenure", "property_acquisition", "utility_connections",
      "lighting", "water_source", "drinking_water",
      "water_distance", "wastewater", "waste_disposal",
      "heating_energy", "water_heating_energy", "cooking_energy",
      "household_equipment", "ict_access", "internet_usage_sex",
      "computer_usage_sex", "internet_usage_sex_ed",
      "computer_usage_sex_ed", "health_coverage_type",
      "child_health_coverage", "social_security_affiliation",
      "disability", "difficulty", "disability_severity",
      "difficulty_severity", "prevalence", "disability_card",
      "employment", "employment_districts", "internal_migration",
      "external_migration", "elderly"),
    domain = c(
      rep("education", 6), rep("demography", 2), rep("housing", 12),
      rep("infrastructure", 10), rep("assets", 6), rep("health", 3),
      rep("disability", 6), rep("employment", 5)),
    description = c(
      "Educational attainment (10+)", "Illiteracy rate (10+)",
      "School attendance (3-24)", "School attendance by sex (3-17)",
      "Net enrollment (6-14)", "Children education (10-17)",
      "Marital status by sex", "Children by age and sex",
      "Housing type", "Construction period", "Rooms (housing)",
      "Rooms used", "Surface area", "Bathroom availability", "Kitchen",
      "Toilet availability", "Toilet flush", "Housing occupancy",
      "Tenure type", "Property acquisition", "Utility connections",
      "Lighting source", "Water source", "Drinking water",
      "Distance to water", "Wastewater disposal", "Waste disposal",
      "Home heating energy", "Water heating energy", "Cooking energy",
      "Equipment ownership", "ICT access", "Internet by sex",
      "Computer by sex", "Internet by sex+education",
      "Computer by sex+education", "Health coverage by type",
      "Child health coverage (0-17)", "Social security (18+)",
      "Disability by type (WG)", "Difficulty by type (WG)",
      "Disability severity", "Difficulty severity", "Prevalence rates",
      "Disability card", "Employment rates", "Employment by district",
      "Internal migration", "External migration",
      "Elderly indicators (60+)"),
    deepest_level = c(
      rep("sector", 6), rep("sector", 2), rep("sector", 12),
      rep("sector", 10), "sector", rep("governorate", 5),
      rep("sector", 3), rep("sector", 6),
      "delegation", "national", "delegation", "delegation", "sector"),
    stringsAsFactors = FALSE
  )
  if (!is.null(domain)) cb <- cb[cb$domain == domain, , drop = FALSE]
  invisible(cb)
}


#' Gini Coefficient
#'
#' Computes the unweighted Gini coefficient of a numeric vector.
#'
#' @param x Numeric vector of non-negative values.
#' @param na.rm Logical. Should missing values be removed?
#'
#' @return A single numeric value between 0 and 1, or \code{NA_real_} if
#'   fewer than 2 non-missing values remain or the sum is zero.
#'
#' @examples
#' del <- load_delegations()
#' gini(del[["utility_connections.total.natural_gas"]])
#'
#' @export
gini <- function(x, na.rm = TRUE) {
  if (na.rm) x <- x[!is.na(x)]
  n <- length(x)
  if (n < 2L || sum(x) == 0) return(NA_real_)
  x <- sort(x)
  idx <- seq_len(n)
  (2 * sum(idx * x) - (n + 1L) * sum(x)) / (n * sum(x))
}

#' Theil Index Decomposition
#'
#' Computes the Theil T inequality index and decomposes it into between-group
#' and within-group components.
#'
#' @param x Numeric vector of positive values.
#' @param group Factor or character vector of group memberships.
#' @param na.rm Logical. Should observations with missing \code{x} or
#'   \code{group} be removed?
#'
#' @return A list with elements \code{total}, \code{between}, \code{within},
#'   \code{pct_between}, and \code{group_detail}.
#'
#' @examples
#' del <- load_delegations()
#' res <- theil_decompose(del[["utility_connections.total.SONEDE"]], del[["region"]])
#' res$pct_between
#'
#' @export
theil_decompose <- function(x, group, na.rm = TRUE) {
  if (na.rm) { keep <- !is.na(x) & !is.na(group); x <- x[keep]; group <- group[keep] }
  pos <- x > 0; x <- x[pos]; group <- group[pos]
  n <- length(x)
  if (n < 2L) return(list(total = NA_real_, between = NA_real_,
    within = NA_real_, pct_between = NA_real_, group_detail = NULL))
  mu <- mean(x)
  T_total <- mean((x / mu) * log(x / mu))
  grps <- split(x, group)
  T_between <- 0; T_within <- 0
  detail <- vector("list", length(grps))
  for (i in seq_along(grps)) {
    g <- grps[[i]]; n_g <- length(g); mu_g <- mean(g)
    y_g <- (n_g * mu_g) / (n * mu)
    T_between <- T_between + y_g * log(mu_g / mu)
    T_g <- if (n_g >= 2L) mean((g / mu_g) * log(g / mu_g)) else 0
    T_within <- T_within + y_g * T_g
    detail[[i]] <- data.frame(group = names(grps)[i], n = n_g,
      mean = mu_g, theil = T_g, weight = y_g, stringsAsFactors = FALSE)
  }
  list(total = T_total, between = T_between, within = T_within,
    pct_between = if (T_total > 0) T_between / T_total * 100 else NA_real_,
    group_detail = do.call(rbind, detail))
}
