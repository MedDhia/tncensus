test_that("colonial_census_tables() lists every shipped table", {
  idx <- colonial_census_tables()
  expect_s3_class(idx, "data.frame")
  expect_true(all(c("table", "census", "title_en", "n_rows") %in% names(idx)))
  expect_true(all(c("eur1906", "ind1931") %in% idx$census))
  expect_true(all(idx$census %in% c("eur1906", "ind1931", "sgt")))
  files <- sub("\\.parquet$", "",
               list.files(system.file("extdata", "colonial", package = "tncensus"),
                          pattern = "\\.parquet$"))
  expect_setequal(idx$table, setdiff(files, "index"))
})

test_that("every colonial table loads with the common columns", {
  idx <- colonial_census_tables()
  for (i in seq_len(nrow(idx))) {
    df <- load_colonial_census(idx$table[i])
    expect_equal(nrow(df), idx$n_rows[i], info = idx$table[i])
    expect_true(all(c("census", "table_id", "source_page", "gallica_view",
                      "value", "flag") %in% names(df)), info = idx$table[i])
    if (idx$census[i] == "sgt") {
      # yearbook tables: one Statistique generale edition per row
      expect_true(all(grepl("^sgt(19[0-9]{2})$", df$census)), info = idx$table[i])
      expect_true("gallica_ark" %in% names(df), info = idx$table[i])
    } else {
      expect_true(all(df$census == idx$census[i]), info = idx$table[i])
    }
    expect_true(all(is.na(df$flag) |
                      df$flag %in% c("ocr_corrected", "illegible",
                                     "total_mismatch",
                                     "derived_from_totals",
                                     "not_applicable",
                                     "reprint_corrected",
                                     "row_realigned")), info = idx$table[i])
  }
})

test_that("load_colonial_census() rejects unknown tables", {
  expect_error(load_colonial_census("nope"), "not found")
})

test_that("colonial_place_crosswalk covers every printed place name", {
  data(colonial_place_crosswalk, package = "tncensus", envir = environment())
  xw <- colonial_place_crosswalk
  expect_true(all(c("level", "name_printed", "controle_civil_std", "match",
                    "lat", "lon") %in% names(xw)))
  expect_true(all(xw$match %in% c(NA, "exact", "qualifier_stripped",
                                  "ambiguous", "conflict", "none")))
  linked <- xw$match %in% c("exact", "qualifier_stripped")
  expect_true(all(!is.na(xw$locality_id_2024[linked])))
  expect_true(all(is.na(xw$locality_id_2024[!linked])))
  # every cheikhat of the 1931 volume has a crosswalk row in its caidat
  ch <- unique(load_colonial_census("ind1931_t3_cheikhat_nationality")[
    , c("cheikhat", "caidat")])
  key_ch <- paste(ch$cheikhat, ch$caidat)
  key_xw <- with(subset(xw, level == "cheikhat"),
                 paste(name_printed, caidat_printed))
  expect_true(all(key_ch %in% key_xw))
  # canonical controles are a small closed set
  expect_lte(length(unique(xw$controle_civil_std[xw$level == "controle_civil"])), 23)
})
