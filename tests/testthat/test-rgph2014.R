# ---- rgph_master dataset ----

test_that("rgph_master has expected dimensions", {
  expect_equal(nrow(rgph_master), 264L)
  expect_equal(ncol(rgph_master), 169L)
})

test_that("rgph_master is a data.frame", {
  expect_s3_class(rgph_master, "data.frame")
})

test_that("rgph_master has correct geographic columns", {
  geo_cols <- c("governorate", "delegation_ar", "delegation_name")
  expect_true(all(geo_cols %in% names(rgph_master)))
  expect_type(rgph_master$governorate, "character")
  expect_type(rgph_master$delegation_ar, "character")
  expect_type(rgph_master$delegation_name, "character")
})

test_that("rgph_master has 24 governorates", {
  expect_equal(length(unique(rgph_master$governorate)), 24L)
})

test_that("population is positive", {
  expect_true(all(rgph_master$population > 0, na.rm = TRUE))
})

test_that("percentages are in 0-100 range", {
  pct_cols <- grep("^pct_", names(rgph_master), value = TRUE)
  for (col in pct_cols) {
    vals <- rgph_master[[col]]
    vals <- vals[!is.na(vals)]
    if (length(vals) > 0) {
      expect_true(all(vals >= 0 & vals <= 100),
                  info = paste0("Column ", col, " has values outside 0-100"))
    }
  }
})

test_that("no duplicate delegations within a governorate", {
  combos <- paste(rgph_master$governorate, rgph_master$delegation_name)
  expect_equal(length(combos), length(unique(combos)))
})

# ---- Helper functions ----

test_that("rgph_sheets returns 28 sheet names", {
  sheets <- rgph_sheets()
  expect_type(sheets, "character")
  expect_equal(length(sheets), 28L)
  expect_true("master_merged" %in% sheets)
})

test_that("rgph_load_sheet returns a data.frame", {
  df <- rgph_load_sheet("master_merged")
  expect_s3_class(df, "data.frame")
  expect_gt(nrow(df), 0L)
})

test_that("rgph_load_sheet errors on invalid sheet", {
  expect_error(rgph_load_sheet("nonexistent_sheet"),
               "not found")
})

test_that("rgph_codebook returns a data.frame with expected columns", {
  cb <- rgph_codebook()
  expect_s3_class(cb, "data.frame")
  expect_true(all(c("variable", "label", "domain", "unit", "denominator")
                   %in% names(cb)))
})

test_that("codebook covers all variables in rgph_master", {
  cb <- rgph_codebook()
  master_vars <- names(rgph_master)
  expect_true(all(master_vars %in% cb$variable),
              info = paste("Missing from codebook:",
                           paste(setdiff(master_vars, cb$variable),
                                 collapse = ", ")))
})
