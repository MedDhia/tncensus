#!/usr/bin/env Rscript
## ------------------------------------------------------------------
## Build .rda files for tncensus
##
## Usage: open the tncensus project in RStudio, then either:
##   source("data-raw/build_rda.R")
## or just select all and run.
##
## Requires: working directory set to the package root (tncensus/).
##           RStudio does this automatically when you open the project.
## ------------------------------------------------------------------

if (!file.exists("DESCRIPTION")) {
  stop(
    "Working directory is not the package root.\n",
    "  Current directory: ", getwd(), "\n",
    "  Please setwd() to the tncensus/ folder first, e.g.:\n",
    "    setwd('~/path/to/tncensus')\n",
    "  Then run:  source('data-raw/build_rda.R')"
  )
}

message("Building .rda files for tncensus...")
message("Working directory: ", getwd())

## Read CSVs
census_panel <- read.csv("data/census_panel.csv",
  stringsAsFactors = FALSE, encoding = "UTF-8", check.names = FALSE)
census_panel$matched <- as.logical(census_panel$matched)
chr <- vapply(census_panel, is.character, logical(1))
census_panel[chr] <- lapply(census_panel[chr], function(x) {
  x <- trimws(x); x[x == ""] <- NA_character_; x
})

delegation_crosswalk <- read.csv("data/delegation_crosswalk.csv",
  stringsAsFactors = FALSE, encoding = "UTF-8")

codebook <- read.csv("data/codebook.csv",
  stringsAsFactors = FALSE, encoding = "UTF-8")

## Save as .rda with xz compression
save(census_panel, file = "data/census_panel.rda", compress = "xz")
save(delegation_crosswalk, file = "data/delegation_crosswalk.rda",
     compress = "xz")
save(codebook, file = "data/codebook.rda", compress = "xz")

## Remove CSVs from data/ (replaced by .rda)
file.remove("data/census_panel.csv", "data/delegation_crosswalk.csv",
            "data/codebook.csv")

## Patch DESCRIPTION to add LazyData
desc <- readLines("DESCRIPTION")
if (!any(grepl("^LazyData:", desc))) {
  idx <- grep("^Encoding:", desc)
  desc <- append(desc, c("LazyData: true", "LazyDataCompression: xz"),
                 after = idx)
  writeLines(desc, "DESCRIPTION")
  message("Added LazyData: true to DESCRIPTION")
}

message("\nDone.")
message("  census_panel:         ", nrow(census_panel), " x ",
        ncol(census_panel))
message("  delegation_crosswalk: ", nrow(delegation_crosswalk), " x ",
        ncol(delegation_crosswalk))
message("  codebook:             ", nrow(codebook), " x ", ncol(codebook))
message("\nNext:")
message("  R CMD build .")
message("  R CMD check tncensus_0.1.0.tar.gz --as-cran")
