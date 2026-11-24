#' Load Variable Metadata for Tunisian Censuses
#'
#' Searchable codebook helper modeled after \code{tidycensus::load_variables()}.
#' Returns a data frame of available variable names, human-readable labels,
#' and thematic concepts for a given census year or the harmonized panel.
#'
#' @param year Integer or character. Census year (\code{2024}, \code{2014},
#'   \code{2004}, or \code{1984}). Ignored when \code{dataset = "panel"}.
#' @param dataset Character. Which dataset to inspect: \code{"auto"} (default,
#'   selects based on \code{year}), \code{"panel"} (harmonized 2014-2024
#'   delegation panel), \code{"rgph2024"}, \code{"rgph2014"}, \code{"rgph2004"},
#'   or \code{"rgph1984"}.
#'
#' @return A \code{data.frame} with columns \code{name}, \code{label},
#'   \code{concept}, \code{year}, and \code{dataset}.
#'
#' @examples
#' # Browse 2024 variables
#' v24 <- load_variables(2024)
#' head(v24)
#'
#' # Search for water or internet variables in 2024
#' subset(v24, grepl("SONEDE|internet", name, ignore.case = TRUE))
#'
#' # Browse harmonized 2014-2024 panel variables
#' v_panel <- load_variables(dataset = "panel")
#' head(v_panel)
#'
#' @export
load_variables <- function(
    year = 2024,
    dataset = c("auto", "panel", "rgph2024", "rgph2014", "rgph2004", "rgph1984")
) {
  dataset <- match.arg(dataset)
  if (dataset == "auto") {
    yr_chr <- as.character(year)[1L]
    dataset <- switch(
      yr_chr,
      "2024" = "rgph2024",
      "2014" = "rgph2014",
      "2004" = "rgph2004",
      "1984" = "rgph1984",
      "panel" = "panel",
      stop("Unsupported year: ", year, ". Choose 2024, 2014, 2004, 1984, or dataset = 'panel'.",
           call. = FALSE)
    )
  }

  if (dataset == "panel") {
    env <- new.env(parent = emptyenv())
    utils::data("codebook", package = "tncensus", envir = env)
    cb <- env$codebook
    return(data.frame(
      name = cb$variable,
      label = cb$label,
      concept = cb$domain,
      year = "2014-2024",
      dataset = "panel",
      stringsAsFactors = FALSE
    ))
  }

  if (dataset == "rgph2024") {
    del <- load_delegations()
    geo_cols <- c(
      "governorate_code", "governorate_name", "governorate_ar", "region",
      "delegation_code", "delegation_name", "delegation_ar",
      "lat", "lon", "delegation_id_salb_un"
    )
    ind_cols <- setdiff(names(del), geo_cols)
    themes <- sub("\\..*$", "", ind_cols)
    cb24 <- rgph2024_codebook()
    idx <- match(themes, cb24$indicator)
    labels <- ifelse(
      is.na(idx),
      ind_cols,
      paste0(cb24$description[idx], " [", sub("^[^.]+\\.", "", ind_cols), "]")
    )
    concepts <- ifelse(is.na(idx), themes, cb24$domain[idx])
    return(data.frame(
      name = ind_cols,
      label = labels,
      concept = concepts,
      year = "2024",
      dataset = "rgph2024",
      stringsAsFactors = FALSE
    ))
  }

  if (dataset == "rgph2014") {
    cb14 <- rgph_codebook()
    geo_cols <- c("governorate", "delegation_ar", "delegation_name")
    cb14 <- cb14[!(cb14$variable %in% geo_cols), , drop = FALSE]
    return(data.frame(
      name = cb14$variable,
      label = cb14$label,
      concept = cb14$domain,
      year = "2014",
      dataset = "rgph2014",
      stringsAsFactors = FALSE
    ))
  }

  if (dataset == "rgph2004") {
    env <- new.env(parent = emptyenv())
    utils::data("rgph2004", package = "tncensus", envir = env)
    df04 <- env$rgph2004
    geo_cols <- c("id", "delegation_id", "delegation_name", "delegation_name_ar", "governorate_id")
    ind_cols <- setdiff(names(df04), geo_cols)
    return(data.frame(
      name = ind_cols,
      label = gsub("_", " ", ind_cols),
      concept = "RGPH 2004",
      year = "2004",
      dataset = "rgph2004",
      stringsAsFactors = FALSE
    ))
  }

  # rgph1984
  data.frame(
    name = c("literacy_rate", "enrollment_rate", "no_schooling", "primary", "secondary", "higher"),
    label = c(
      "Literacy rate by age and sex",
      "School enrollment rate by age and sex",
      "Share with no schooling",
      "Share with primary education",
      "Share with secondary education",
      "Share with higher education"
    ),
    concept = "Education (1984)",
    year = "1984",
    dataset = "rgph1984",
    stringsAsFactors = FALSE
  )
}


#' Query Tunisian Census Data in Tidy or Wide Format
#'
#' Unified query interface modeled after \code{tidycensus::get_decennial()} and
#' \code{tidycensus::get_acs()}. Retrieves Tunisian census indicators at the
#' requested administrative geography, optionally filters by governorate or
#' region, reshapes to tidy (long) or wide format, and optionally attaches
#' \code{sf} polygon geometries.
#'
#' @param geography Character. Administrative level: \code{"delegation"}
#'   (default), \code{"governorate"}, \code{"region"}, \code{"national"}, or
#'   \code{"sector"} (requires prior \code{\link{download_sectors}()}). Plural
#'   forms (e.g., \code{"delegations"}) are also accepted.
#' @param variables Character vector of variable names to retrieve. Named
#'   vectors (e.g., \code{c(water = "utility_connections.total.SONEDE")}) rename
#'   variables in the output, just like \pkg{tidycensus}. Use
#'   \code{\link{load_variables}()} to discover variable names. If \code{NULL},
#'   returns all indicator variables for the selected dataset.
#' @param year Integer or integer vector. Supports \code{2024} (default),
#'   \code{2014}, \code{2004}, or \code{c(2014, 2024)} (queries the harmonized
#'   \code{census_panel} using base indicator names such as
#'   \code{"pct_higher_ed"} or \code{"unemployment_rate"}).
#' @param governorate Optional character vector. Filter results to specific
#'   governorate name(s) or code(s) (case-insensitive partial match).
#' @param region Optional character vector. Filter results to specific region
#'   name(s) (case-insensitive partial match).
#' @param output Character. \code{"tidy"} (default, long format with
#'   \code{GEOID}, \code{NAME}, \code{variable}, \code{value}, \code{year}) or
#'   \code{"wide"} (one column per variable).
#' @param geometry Logical. If \code{TRUE}, attaches polygon geometries via
#'   \code{\link{load_geojson}()} and returns an \code{sf} object. Requires the
#'   \pkg{sf} package. Defaults to \code{FALSE}.
#' @param keep_geo_vars Logical. If \code{TRUE} and \code{geometry = TRUE},
#'   retains all multilingual GeoJSON metadata columns. Defaults to \code{FALSE}.
#'
#' @return A \code{data.frame} (or \code{sf} spatial data frame if
#'   \code{geometry = TRUE}).
#'
#' @examples
#' # Tidy query for 2024 delegation utility access
#' df <- get_tn_census(
#'   geography = "delegation",
#'   variables = c(
#'     sonede = "utility_connections.total.SONEDE",
#'     gas = "utility_connections.total.natural_gas"
#'   ),
#'   year = 2024,
#'   governorate = "Tunis"
#' )
#' head(df)
#'
#' # Multi-year panel query (2014 & 2024) in wide format
#' panel_df <- get_tn_census(
#'   geography = "delegation",
#'   variables = c("pct_higher_ed", "unemployment_rate"),
#'   year = c(2014, 2024),
#'   output = "wide"
#' )
#' head(panel_df)
#'
#' @export
get_tn_census <- function(
    geography = c("delegation", "governorate", "region", "national", "sector"),
    variables = NULL,
    year = 2024,
    governorate = NULL,
    region = NULL,
    output = c("tidy", "wide"),
    geometry = FALSE,
    keep_geo_vars = FALSE
) {
  # Normalize plural aliases
  geography <- tolower(as.character(geography[1L]))
  geography <- sub("s$", "", geography)
  geography <- match.arg(geography, c("delegation", "governorate", "region", "national", "sector"))
  output <- match.arg(output)

  if (geometry && geography == "sector") {
    stop("GeoJSON geometries are not bundled for sector level.", call. = FALSE)
  }
  if (geometry && !requireNamespace("sf", quietly = TRUE)) {
    stop("Package 'sf' is required when geometry = TRUE. Install with install.packages('sf').",
         call. = FALSE)
  }

  # Handle multi-year panel query (e.g. year = c(2014, 2024))
  if (length(year) > 1L) {
    if (!all(year %in% c(2014, 2024))) {
      stop("Multi-year queries currently support year = c(2014, 2024) via census_panel.", call. = FALSE)
    }
    if (geography != "delegation") {
      stop("Harmonized 2014-2024 panel queries only support geography = 'delegation'.", call. = FALSE)
    }
    return(.query_panel(
      variables = variables, years = sort(unique(year)),
      governorate = governorate, region = region,
      output = output, geometry = geometry, keep_geo_vars = keep_geo_vars
    ))
  }

  yr <- as.integer(year[1L])
  if (yr == 2024L) {
    res <- .query_2024(geography, variables, governorate, region, output)
  } else if (yr == 2014L) {
    res <- .query_2014(geography, variables, governorate, output)
  } else if (yr == 2004L) {
    res <- .query_2004(geography, variables, governorate, output)
  } else {
    stop("Unsupported year: ", year, ". Choose 2024, 2014, 2004, or c(2014, 2024).", call. = FALSE)
  }

  if (geometry) {
    res <- .attach_geometry(res, geography = geography, keep_geo_vars = keep_geo_vars)
  }
  res
}


#' @noRd
.rename_and_select_vars <- function(df, id_cols, variables) {
  avail <- setdiff(names(df), id_cols)
  if (is.null(variables)) {
    selected <- avail
    var_labels <- avail
  } else {
    missing_vars <- setdiff(unname(variables), names(df))
    if (length(missing_vars) > 0L) {
      stop(
        "Variable(s) not found: ", paste(missing_vars, collapse = ", "),
        ". Use load_variables() to see valid names.",
        call. = FALSE
      )
    }
    selected <- unname(variables)
    nms <- names(variables)
    var_labels <- if (is.null(nms)) selected else ifelse(nzchar(nms), nms, selected)
  }
  out <- df[, c(id_cols, selected), drop = FALSE]
  names(out)[seq(length(id_cols) + 1L, ncol(out))] <- var_labels
  list(data = out, vars = var_labels)
}

#' @noRd
.to_tidy <- function(df, id_cols, var_cols, year_val) {
  if (length(var_cols) == 0L) return(df)
  long_list <- lapply(var_cols, function(v) {
    sub_df <- df[, id_cols, drop = FALSE]
    sub_df$variable <- v
    sub_df$value <- suppressWarnings(as.numeric(df[[v]]))
    sub_df$year <- year_val
    sub_df
  })
  res <- do.call(rbind, long_list)
  rownames(res) <- NULL
  res
}

#' @noRd
.normalize_region_pattern <- function(region) {
  # Map French/English region aliases so either works seamlessly
  aliases <- c(
    "Nord Est" = "North East", "North East" = "Nord Est",
    "Nord Ouest" = "North West", "North West" = "Nord Ouest",
    "Centre Est" = "Centre East", "Centre East" = "Centre Est",
    "Centre Ouest" = "Centre West", "Centre West" = "Centre Ouest",
    "Sud Est" = "South East", "South East" = "Sud Est",
    "Sud Ouest" = "South West", "South West" = "Sud Ouest"
  )
  expanded <- unique(c(region, aliases[region]))
  expanded <- expanded[!is.na(expanded)]
  paste(expanded, collapse = "|")
}

#' @noRd
.filter_geo <- function(df, governorate = NULL, region = NULL, gov_col = "governorate", reg_col = "region") {
  if (!is.null(governorate) && gov_col %in% names(df)) {
    pat <- paste(governorate, collapse = "|")
    keep <- grepl(pat, as.character(df[[gov_col]]), ignore.case = TRUE)
    if ("governorate_code" %in% names(df)) {
      keep <- keep | (as.character(df[["governorate_code"]]) %in% as.character(governorate))
    }
    df <- df[keep, , drop = FALSE]
  }
  if (!is.null(region) && reg_col %in% names(df)) {
    pat <- .normalize_region_pattern(region)
    keep <- grepl(pat, as.character(df[[reg_col]]), ignore.case = TRUE)
    df <- df[keep, , drop = FALSE]
  }
  df
}

#' @noRd
.query_2024 <- function(geography, variables, governorate, region, output) {
  if (geography == "delegation") {
    raw <- load_delegations()
    raw <- .filter_geo(raw, governorate, region, gov_col = "governorate_name", reg_col = "region")
    raw$GEOID <- as.character(raw$delegation_code)
    raw$NAME <- raw$delegation_name
    raw$NAME_AR <- raw$delegation_ar
    raw$governorate <- raw$governorate_name
    id_cols <- c("GEOID", "NAME", "NAME_AR", "governorate", "region")
  } else if (geography == "governorate") {
    raw <- load_governorates()
    raw <- .filter_geo(raw, governorate, region, gov_col = "governorate_name", reg_col = "region")
    raw$GEOID <- as.character(raw$governorate_code)
    raw$NAME <- raw$governorate_name
    raw$NAME_AR <- raw$governorate_ar
    id_cols <- c("GEOID", "NAME", "NAME_AR", "region")
  } else if (geography == "region") {
    gov <- load_governorates()
    gov <- .filter_geo(gov, governorate = NULL, region = region, reg_col = "region")
    num_cols <- setdiff(names(gov), c("governorate_code", "governorate_name", "governorate_ar", "region", "district_name", "department_code", "lat", "lon"))
    if (!is.null(variables)) num_cols <- intersect(num_cols, unname(variables))
    agg_list <- lapply(split(gov, gov$region), function(sub_g) {
      vals <- lapply(num_cols, function(col) mean(as.numeric(sub_g[[col]]), na.rm = TRUE))
      names(vals) <- num_cols
      row <- data.frame(GEOID = sub_g$region[1L], NAME = sub_g$region[1L], stringsAsFactors = FALSE)
      cbind(row, as.data.frame(vals, check.names = FALSE, stringsAsFactors = FALSE))
    })
    raw <- do.call(rbind, agg_list)
    rownames(raw) <- NULL
    id_cols <- c("GEOID", "NAME")
  } else if (geography == "national") {
    raw <- load_national()
    raw$GEOID <- "TN"
    raw$NAME <- "Tunisia"
    id_cols <- c("GEOID", "NAME")
  } else {
    raw <- load_sectors()
    raw <- .filter_geo(raw, governorate, region, gov_col = "governorate_name", reg_col = "region")
    raw$GEOID <- as.character(raw$sector_code)
    raw$NAME <- raw$sector_name
    raw$governorate <- raw$governorate_name
    id_cols <- intersect(c("GEOID", "NAME", "delegation_name", "governorate", "region"), names(raw))
  }

  geo_exclude <- unique(c(
    id_cols, "governorate_code", "governorate_name", "governorate_ar",
    "delegation_code", "delegation_name", "delegation_ar", "sector_code", "sector_name",
    "lat", "lon", "delegation_id_salb_un", "district_name", "department_code"
  ))
  sel <- .rename_and_select_vars(raw[, c(id_cols, setdiff(names(raw), geo_exclude)), drop = FALSE], id_cols, variables)
  if (output == "wide") {
    sel$data$year <- 2024L
    return(sel$data)
  }
  .to_tidy(sel$data, id_cols, sel$vars, 2024L)
}

#' @noRd
.query_2014 <- function(geography, variables, governorate, output) {
  if (geography != "delegation") {
    stop("RGPH 2014 master table is only available at geography = 'delegation'.", call. = FALSE)
  }
  env <- new.env(parent = emptyenv())
  utils::data("rgph_master", package = "tncensus", envir = env)
  raw <- env$rgph_master
  raw <- .filter_geo(raw, governorate = governorate, gov_col = "governorate")
  raw$GEOID <- raw$delegation_name
  raw$NAME <- raw$delegation_name
  raw$NAME_AR <- raw$delegation_ar
  id_cols <- c("GEOID", "NAME", "NAME_AR", "governorate")
  clean_df <- raw[, c(id_cols, setdiff(names(raw), c(id_cols, "delegation_ar", "delegation_name"))), drop = FALSE]
  sel <- .rename_and_select_vars(clean_df, id_cols, variables)
  if (output == "wide") {
    sel$data$year <- 2014L
    return(sel$data)
  }
  .to_tidy(sel$data, id_cols, sel$vars, 2014L)
}

#' @noRd
.query_2004 <- function(geography, variables, governorate, output) {
  env <- new.env(parent = emptyenv())
  utils::data("rgph2004", package = "tncensus", envir = env)
  raw <- env$rgph2004
  if (geography == "delegation") {
    raw <- raw[!is.na(raw$delegation_id), , drop = FALSE]
    raw$GEOID <- as.character(raw$delegation_id)
    raw$NAME <- gsub("_", " ", raw$delegation_name)
    raw$NAME_AR <- gsub("_", " ", raw$delegation_name_ar)
    id_cols <- c("GEOID", "NAME", "NAME_AR")
  } else if (geography == "governorate") {
    raw <- raw[grepl("^Total_", raw$delegation_name), , drop = FALSE]
    raw$GEOID <- gsub("^Total_", "", raw$delegation_name)
    raw$NAME <- raw$GEOID
    id_cols <- c("GEOID", "NAME")
  } else if (geography == "national") {
    raw <- raw[raw$delegation_name == "Total", , drop = FALSE]
    raw$GEOID <- "TN"
    raw$NAME <- "Tunisia"
    id_cols <- c("GEOID", "NAME")
  } else {
    stop("RGPH 2004 supports geography = 'delegation', 'governorate', or 'national'.", call. = FALSE)
  }
  if (!is.null(governorate) && geography == "delegation") {
    pat <- paste(governorate, collapse = "|")
    raw <- raw[grepl(pat, as.character(raw$governorate_id), ignore.case = TRUE) |
                 grepl(pat, raw$NAME, ignore.case = TRUE), , drop = FALSE]
  }
  geo_exclude <- c("id", "delegation_id", "delegation_name", "delegation_name_ar", "governorate_id")
  clean_df <- raw[, c(id_cols, setdiff(names(raw), c(id_cols, geo_exclude))), drop = FALSE]
  sel <- .rename_and_select_vars(clean_df, id_cols, variables)
  if (output == "wide") {
    sel$data$year <- 2004L
    return(sel$data)
  }
  .to_tidy(sel$data, id_cols, sel$vars, 2004L)
}

#' @noRd
.query_panel <- function(variables, years, governorate, region, output, geometry, keep_geo_vars) {
  env <- new.env(parent = emptyenv())
  utils::data("census_panel", package = "tncensus", envir = env)
  raw <- env$census_panel
  raw <- .filter_geo(raw, governorate = governorate, region = region, gov_col = "gov_2024", reg_col = "region_2024")
  raw$GEOID <- ifelse(is.na(raw$delegation_fr_2024), raw$delegation_fr_2014, raw$delegation_fr_2024)
  raw$NAME <- raw$GEOID
  raw$NAME_AR <- raw$delegation_ar
  raw$governorate <- raw$gov_2024
  raw$region <- raw$region_2024
  id_cols <- c("GEOID", "NAME", "NAME_AR", "governorate", "region")

  if (is.null(variables)) {
    base_vars <- unique(sub("_(2014|2024|change)$", "", grep("_2024$", names(raw), value = TRUE)))
    base_vars <- setdiff(base_vars, c("delegation_fr", "gov", "region"))
    var_labels <- base_vars
  } else {
    base_vars <- unname(variables)
    nms <- names(variables)
    var_labels <- if (is.null(nms)) base_vars else ifelse(nzchar(nms), nms, base_vars)
  }

  year_frames <- lapply(years, function(yr) {
    cols_yr <- paste0(base_vars, "_", yr)
    missing_cols <- setdiff(cols_yr, names(raw))
    if (length(missing_cols) > 0L) {
      stop("Panel variable(s) not found: ", paste(missing_cols, collapse = ", "), call. = FALSE)
    }
    sub_df <- raw[, c(id_cols, cols_yr), drop = FALSE]
    names(sub_df)[seq(length(id_cols) + 1L, ncol(sub_df))] <- var_labels
    if (output == "wide") {
      sub_df$year <- as.integer(yr)
      return(sub_df)
    }
    .to_tidy(sub_df, id_cols, var_labels, as.integer(yr))
  })
  res <- do.call(rbind, year_frames)
  rownames(res) <- NULL

  if (geometry) {
    res <- .attach_geometry(res, geography = "delegation", keep_geo_vars = keep_geo_vars)
  }
  res
}

#' @noRd
.attach_geometry <- function(df, geography, keep_geo_vars = FALSE) {
  level <- switch(
    geography,
    delegation = "delegations",
    governorate = "governorates",
    region = "regions",
    national = "national"
  )
  geo <- load_geojson(level)

  if (geography == "delegation") {
    # Match by delegation_code when numeric, otherwise by 2024/2014 French name
    if (all(grepl("^[0-9]+$", df$GEOID))) {
      geo_key <- "delegation_code"
      geo$delegation_code <- as.character(geo$delegation_code)
    } else {
      geo_key <- "delegation_name_2024"
    }
    if (!keep_geo_vars) {
      geo <- geo[, c(geo_key, "geometry")]
    }
    merged <- merge(geo, df, by.x = geo_key, by.y = "GEOID", all.y = TRUE)
    names(merged)[names(merged) == geo_key] <- "GEOID"
    return(merged)
  }

  if (geography == "governorate") {
    geo_key <- if (all(grepl("^[0-9]+$", df$GEOID))) "governorate_code" else "governorate_name"
    geo[[geo_key]] <- as.character(geo[[geo_key]])
    if (!keep_geo_vars) geo <- geo[, c(geo_key, "geometry")]
    merged <- merge(geo, df, by.x = geo_key, by.y = "GEOID", all.y = TRUE)
    names(merged)[names(merged) == geo_key] <- "GEOID"
    return(merged)
  }

  if (geography == "region") {
    if (!keep_geo_vars) geo <- geo[, c("region_name", "geometry")]
    merged <- merge(geo, df, by.x = "region_name", by.y = "GEOID", all.y = TRUE)
    names(merged)[names(merged) == "region_name"] <- "GEOID"
    return(merged)
  }

  # national
  if (!keep_geo_vars) geo <- geo[, c("iso3", "geometry")]
  cbind(geo[rep(1L, nrow(df)), , drop = FALSE], df)
}


# ==============================================================================
# tigris-style Administrative Boundary Helpers
# ==============================================================================

#' Load Tunisia National Boundary (tigris-style helper)
#'
#' Convenience wrapper around \code{\link{load_geojson}("national")} modeled
#' after \pkg{tigris} boundary functions.
#'
#' @return An \code{sf} spatial data frame with 1 polygon feature.
#' @export
#' @examples
#' if (requireNamespace("sf", quietly = TRUE)) {
#'   tn <- tn_national()
#' }
tn_national <- function() {
  load_geojson("national")
}

#' Load Tunisia Economic Regions Boundaries (tigris-style helper)
#'
#' Convenience wrapper around \code{\link{load_geojson}("regions")} modeled
#' after \pkg{tigris} boundary functions.
#'
#' @return An \code{sf} spatial data frame with 6 region polygon features.
#' @export
#' @examples
#' if (requireNamespace("sf", quietly = TRUE)) {
#'   reg <- tn_regions()
#' }
tn_regions <- function() {
  load_geojson("regions")
}

#' Load Tunisia Governorate Boundaries (tigris-style helper)
#'
#' Loads the 24 Tunisian governorates as an \code{sf} spatial data frame,
#' optionally filtered by region name or code (modeled after
#' \code{tigris::counties()}).
#'
#' @param region Optional character vector. Region name(s) or code(s) to
#'   filter by (case-insensitive partial match).
#'
#' @return An \code{sf} spatial data frame of governorate polygons.
#' @export
#' @examples
#' if (requireNamespace("sf", quietly = TRUE)) {
#'   gov_ne <- tn_governorates(region = "Nord Est")
#'   nrow(gov_ne)
#' }
tn_governorates <- function(region = NULL) {
  geo <- load_geojson("governorates")
  if (!is.null(region)) {
    pat <- .normalize_region_pattern(region)
    keep <- grepl(pat, geo$region_name, ignore.case = TRUE) |
      (as.character(geo$region_code) %in% as.character(region))
    geo <- geo[keep, , drop = FALSE]
  }
  geo
}

#' Load Tunisia Delegation Boundaries (tigris-style helper)
#'
#' Loads the 264 Tunisian delegations as an \code{sf} spatial data frame,
#' optionally filtered by governorate or region (modeled after
#' \code{tigris::tracts()}).
#'
#' @param governorate Optional character vector. Governorate name(s) or code(s)
#'   to filter by (case-insensitive partial match).
#' @param region Optional character vector. Region name(s) or code(s) to
#'   filter by (case-insensitive partial match).
#'
#' @return An \code{sf} spatial data frame of delegation polygons.
#' @export
#' @examples
#' if (requireNamespace("sf", quietly = TRUE)) {
#'   tunis_del <- tn_delegations(governorate = "Tunis")
#'   nrow(tunis_del)
#' }
tn_delegations <- function(governorate = NULL, region = NULL) {
  geo <- load_geojson("delegations")
  if (!is.null(governorate)) {
    pat <- paste(governorate, collapse = "|")
    keep <- grepl(pat, geo$governorate_name, ignore.case = TRUE) |
      (as.character(geo$governorate_code) %in% as.character(governorate))
    geo <- geo[keep, , drop = FALSE]
  }
  if (!is.null(region)) {
    pat <- .normalize_region_pattern(region)
    keep <- grepl(pat, geo$region_name, ignore.case = TRUE) |
      (as.character(geo$region_code) %in% as.character(region))
    geo <- geo[keep, , drop = FALSE]
  }
  geo
}
