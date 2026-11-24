test_that("load_variables returns metadata for all supported waves", {
  v24 <- load_variables(2024)
  expect_s3_class(v24, "data.frame")
  expect_true(all(c("name", "label", "concept", "year", "dataset") %in% names(v24)))
  expect_gt(nrow(v24), 100)

  v14 <- load_variables(2014)
  expect_gt(nrow(v14), 100)

  v04 <- load_variables(2004)
  expect_gt(nrow(v04), 30)

  v_panel <- load_variables(dataset = "panel")
  expect_equal(nrow(v_panel), 45)

  expect_error(load_variables(1999))
})

test_that("get_tn_census works in tidy and wide modes with named variables", {
  df_tidy <- get_tn_census(
    geography = "delegation",
    variables = c(
      sonede = "utility_connections.total.SONEDE",
      gas = "utility_connections.total.natural_gas"
    ),
    year = 2024,
    governorate = "Tunis",
    output = "tidy"
  )
  expect_s3_class(df_tidy, "data.frame")
  expect_true(all(c("GEOID", "NAME", "variable", "value", "year") %in% names(df_tidy)))
  expect_setequal(unique(df_tidy$variable), c("sonede", "gas"))
  expect_true(all(df_tidy$year == 2024L))
  expect_gt(nrow(df_tidy), 20)

  df_wide <- get_tn_census(
    geography = "governorate",
    variables = c(sonede = "utility_connections.total.SONEDE"),
    year = 2024,
    output = "wide"
  )
  expect_equal(nrow(df_wide), 24)
  expect_true("sonede" %in% names(df_wide))
})

test_that("get_tn_census supports multi-year panel queries", {
  panel_tidy <- get_tn_census(
    geography = "delegation",
    variables = c(higher_ed = "pct_higher_ed"),
    year = c(2014, 2024),
    output = "tidy"
  )
  expect_setequal(unique(panel_tidy$year), c(2014L, 2024L))
  expect_equal(unique(panel_tidy$variable), "higher_ed")
})

test_that("get_tn_census attaches sf geometry when geometry = TRUE", {
  skip_if_not_installed("sf")
  gov_sf <- get_tn_census(
    geography = "governorate",
    variables = c(sonede = "utility_connections.total.SONEDE"),
    year = 2024,
    geometry = TRUE
  )
  expect_s3_class(gov_sf, "sf")
  expect_equal(nrow(gov_sf), 24)
})

test_that("tigris-style boundary helpers filter cleanly", {
  skip_if_not_installed("sf")
  expect_equal(nrow(tn_national()), 1)
  expect_equal(nrow(tn_regions()), 6)
  expect_equal(nrow(tn_governorates()), 24)
  expect_equal(nrow(tn_governorates(region = "Nord Est")), 7)
  tunis_del <- tn_delegations(governorate = "Tunis")
  expect_gt(nrow(tunis_del), 15)
  expect_true(all(tunis_del$governorate_name == "Tunis"))
})
