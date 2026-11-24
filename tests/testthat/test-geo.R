test_that("load_geojson loads all four administrative levels", {
  skip_if_not_installed("sf")

  nat <- load_geojson("national")
  reg <- load_geojson("regions")
  gov <- load_geojson("governorates")
  del <- load_geojson("delegations")

  expect_s3_class(nat, "sf")
  expect_equal(nrow(nat), 1L)
  expect_equal(nrow(reg), 6L)
  expect_equal(nrow(gov), 24L)
  expect_equal(nrow(del), 264L)
  expect_true(all(c("delegation_code", "delegation_name", "delegation_name_ar", "delegation_name_alt", "governorate_code") %in% names(del)))
  expect_true("country_name_ar" %in% names(nat))
  expect_true("region_name_ar" %in% names(reg))
  expect_true("governorate_name_ar" %in% names(gov))
})
