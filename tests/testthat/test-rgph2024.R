test_that("delegations: 279 rows, clean English columns", {
  del <- load_delegations()
  expect_equal(nrow(del), 279)
  expect_true("delegation_name" %in% names(del))
  expect_equal(names(del)[1], "governorate_code")
  expect_true(ncol(del) >= 900)
})
test_that("governorates: 24 rows", {
  expect_equal(nrow(load_governorates()), 24)
})
test_that("national: 1 row", {
  expect_equal(nrow(load_national()), 1)
})
test_that("sectors: errors without download", {
  expect_error(load_sectors(cache_dir = tempfile()), "download_sectors")
})
test_that("caching", {
  expect_identical(load_delegations(), load_delegations())
})
test_that("get_governorate by code", {
  expect_equal(get_governorate(11)$governorate_name, "Tunis")
})
test_that("get_governorate by name", {
  expect_equal(nrow(get_governorate(name = "Sfax")), 1)
})
test_that("get_delegation by code", {
  expect_equal(nrow(get_delegation(1151)), 1)
})
test_that("get_region", {
  co <- get_region("Centre Ouest")
  expect_true(nrow(co) > 0)
  expect_true(all(co$region == "Centre Ouest"))
})
test_that("coordinates in Tunisia", {
  del <- load_delegations()
  expect_true(all(del$lat > 30 & del$lat < 38))
  expect_true(all(del$lon > 7 & del$lon < 12))
  expect_true(!any(is.na(del$lat)))
})
test_that("list_indicators", {
  expect_true("employment" %in% list_indicators())
})
test_that("search_indicator", {
  expect_true(length(search_indicator("delegations", "unemployment")) > 0)
})
test_that("rgph2024_codebook", {
  cb <- rgph2024_codebook()
  expect_true(is.data.frame(cb))
  expect_true(nrow(cb) >= 46)
  expect_true(all(rgph2024_codebook("education")$domain == "education"))
})
test_that("gini known cases", {
  expect_equal(gini(rep(1, 100)), 0)
  expect_true(gini(c(rep(0, 99), 100)) > 0.98)
  expect_true(is.na(gini(c(NA, NA))))
})
test_that("gini real data", {
  del <- load_delegations()
  expect_true(gini(del[["utility_connections.total.natural_gas"]]) > 0.5)
  expect_true(gini(del[["utility_connections.total.STEG"]]) < 0.05)
})
test_that("theil additivity", {
  del <- load_delegations()
  r <- theil_decompose(del[["utility_connections.total.SONEDE"]], del[["region"]])
  expect_true(abs(r$total - r$between - r$within) < 0.01)
  expect_true(nrow(r$group_detail) == 6)
})
test_that("hierarchy consistency", {
  gov_codes <- unique(load_governorates()$governorate_code)
  del_gov <- unique(load_delegations()$governorate_code)
  expect_true(all(del_gov %in% gov_codes))
})
test_that("all 6 regions present", {
  regions <- unique(load_delegations()$region)
  expected <- c("Nord Est", "Nord Ouest", "Centre Est",
                "Centre Ouest", "Sud Est", "Sud Ouest")
  expect_true(all(expected %in% regions))
})
