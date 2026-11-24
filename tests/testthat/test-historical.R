test_that("rgph2004 has expected structure and counts", {
  expect_s3_class(rgph2004, "data.frame")
  expect_equal(nrow(rgph2004), 289L)
  expect_equal(ncol(rgph2004), 54L)
  expect_equal(sum(rgph2004$level == "delegation"), 264L)
  expect_equal(sum(rgph2004$level == "governorate"), 24L)
  expect_equal(sum(rgph2004$level == "national"), 1L)
})

test_that("rgph1984_education has expected structure", {
  expect_s3_class(rgph1984_education, "data.frame")
  expect_equal(ncol(rgph1984_education), 6L)
  expect_gt(nrow(rgph1984_education), 50000L)
  expect_setequal(unique(rgph1984_education$sex), c("male", "female"))
  expect_setequal(
    unique(rgph1984_education$table),
    c("literacy", "education_level", "school_attendance")
  )
})

test_that("historical_education covers 7 census waves", {
  expect_s3_class(historical_education, "data.frame")
  expect_equal(nrow(historical_education), 7L)
  expect_equal(historical_education$year, c(1956L, 1966L, 1975L, 1984L, 1994L, 2004L, 2014L))
})

test_that("delegation_codes_ins maps 264 delegations", {
  expect_s3_class(delegation_codes_ins, "data.frame")
  expect_equal(nrow(delegation_codes_ins), 264L)
  expect_true(all(c("delegation_id", "delegation_id_1984", "delegation_id_salb_un") %in% names(delegation_codes_ins)))
})

test_that("rgph1966_illiteracy has 14 rows", {
  expect_s3_class(rgph1966_illiteracy, "data.frame")
  expect_equal(nrow(rgph1966_illiteracy), 14L)
})

test_that("colonial census datasets have expected dimensions", {
  expect_equal(nrow(colonial_tunisian_pop), 871L)
  expect_equal(nrow(colonial_european_pop), 525L)
  expect_equal(nrow(colonial_age_caidat_1931), 37L)
  expect_equal(nrow(colonial_age_controle_civil_1931), 21L)
})

test_that("geo harmonization datasets have expected dimensions", {
  expect_equal(nrow(historical_geonames), 1276L)
  expect_true(all(c("locality_name_source", "locality_name_modern", "lat", "lon") %in% names(historical_geonames)))
  expect_equal(nrow(delegation_matrix_2014), 264L)
  expect_equal(nrow(delegation_matrix_1984), 198L)
  expect_equal(nrow(delegation_matrix_merged), 217L)
})
