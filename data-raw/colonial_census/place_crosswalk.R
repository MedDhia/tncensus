# Save the place-name crosswalk as the colonial_place_crosswalk dataset.
# Build the CSV first:  python3 data-raw/colonial_census/place_crosswalk.py
# Then, from the repository root:  Rscript data-raw/colonial_census/place_crosswalk.R
colonial_place_crosswalk <- utils::read.csv(
  "data-raw/colonial_census/place_crosswalk.csv",
  colClasses = "character", na.strings = "", encoding = "UTF-8"
)
for (col in names(colonial_place_crosswalk)) {
  colonial_place_crosswalk[[col]] <- enc2utf8(colonial_place_crosswalk[[col]])
}
colonial_place_crosswalk$n_candidates <- as.integer(colonial_place_crosswalk$n_candidates)
colonial_place_crosswalk$locality_id_2024 <- as.integer(colonial_place_crosswalk$locality_id_2024)
colonial_place_crosswalk$lat <- as.numeric(colonial_place_crosswalk$lat)
colonial_place_crosswalk$lon <- as.numeric(colonial_place_crosswalk$lon)
save(colonial_place_crosswalk, file = "data/colonial_place_crosswalk.rda", compress = "xz")
