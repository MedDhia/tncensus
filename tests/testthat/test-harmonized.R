test_that("census_panel has expected dimensions", {
  expect_s3_class(census_panel, "data.frame")
  expect_equal(nrow(census_panel), 281L)
  expect_equal(ncol(census_panel), 144L)
})

test_that("delegation_crosswalk has expected dimensions and match types", {
  expect_s3_class(delegation_crosswalk, "data.frame")
  expect_equal(nrow(delegation_crosswalk), 263L)
  expect_equal(ncol(delegation_crosswalk), 5L)
  expect_true(all(delegation_crosswalk$match_type %in% c("exact", "fuzzy")))
})

test_that("harmonized codebook documents all 45 indicators", {
  expect_s3_class(codebook, "data.frame")
  expect_equal(nrow(codebook), 45L)
  expect_true(all(c("variable", "domain", "label", "unit", "note") %in% names(codebook)))
})
