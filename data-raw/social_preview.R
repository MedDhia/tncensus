# Generate an artsy, data-art 1280x640 GitHub social preview
library(ggplot2)
library(sf)
library(magick)

del_sf <- st_read("inst/extdata/geo/delegations.geojson", quiet = TRUE)
del24  <- as.data.frame(arrow::read_parquet("inst/extdata/rgph2024/delegations.parquet"))

# Join a real 2024 indicator (internet usage or electricity/education) for luminous choropleth
m <- match(del_sf$delegation_code, del24$delegation_code)
val <- del24[["internet_usage_sex.total.total"]][m]
if (is.null(val) || all(is.na(val))) val <- del_sf$center_lat
val[is.na(val)] <- median(val, na.rm = TRUE)
del_sf$val <- val

# Flowing translucent statistical wave ribbons across the canvas
x_seq <- seq(-3, 13, length.out = 500)
waves <- do.call(rbind, lapply(1:6, function(i) {
  data.frame(
    x = x_seq,
    y = 32.8 + 0.55 * sin(x_seq * 0.45 + i * 0.55) + (i - 3.5) * 0.38,
    grp = factor(i)
  )
}))

# Subtle concentric astrolabe arcs centered behind the Tunisia map
make_arc <- function(cx, cy, r, a1 = 0, a2 = 2 * pi, n = 200) {
  th <- seq(a1, a2, length.out = n)
  data.frame(x = cx + r * cos(th), y = cy + r * sin(th))
}
arc1 <- make_arc(9.5, 34.0, 3.2)
arc2 <- make_arc(9.5, 34.0, 4.4)

art_plot <- ggplot() +
  # Flowing statistical wave lines
  geom_path(data = waves, aes(x = x, y = y, group = grp),
            color = "#2dd4bf", alpha = 0.08, linewidth = 0.6) +
  # Subtle geometric rings around the map
  geom_path(data = arc1, aes(x = x, y = y),
            color = "#38bdf8", alpha = 0.14, linewidth = 0.35, linetype = "dashed") +
  geom_path(data = arc2, aes(x = x, y = y),
            color = "#2dd4bf", alpha = 0.10, linewidth = 0.30) +
  # Luminous 264-delegation choropleth of Tunisia on the right
  geom_sf(data = del_sf, aes(fill = val),
          color = "#070b14", linewidth = 0.14, alpha = 0.92, show.legend = FALSE) +
  scale_fill_viridis_c(option = "mako", begin = 0.22, end = 0.92) +
  coord_sf(xlim = c(-3.8, 12.2), ylim = c(29.8, 37.8), expand = FALSE, datum = NA) +
  theme_void() +
  theme(
    plot.background  = element_rect(fill = "#070b14", color = NA),
    panel.background = element_rect(fill = "#070b14", color = NA)
  )

tmp_bg <- tempfile(fileext = ".png")
ggsave(tmp_bg, art_plot, width = 1280 / 96, height = 640 / 96, dpi = 96, bg = "#070b14")

canvas <- image_read(tmp_bg)

# Composite the tncensus hex sticker on the left
logo <- image_read("man/figures/logo.png") |>
  image_scale("x320")
canvas <- canvas |>
  image_composite(logo, offset = "+65+160") |>
  image_annotate(
    "tncensus",
    size = 86,
    weight = 700,
    color = "#f8fafc",
    location = "+415+205",
    font = "Helvetica"
  ) |>
  image_annotate(
    "Tunisian Census Data  ·  1891–2024",
    size = 28,
    weight = 500,
    color = "#2dd4bf",
    location = "+419+312",
    font = "Helvetica"
  ) |>
  image_annotate(
    "Colonial Archives to Modern RGPH  ·  GeoJSON & Parquet",
    size = 19,
    color = "#94a3b8",
    location = "+419+362",
    font = "Helvetica"
  ) |>
  image_annotate(
    "github.com/MedDhia/tncensus",
    size = 18,
    color = "#475569",
    location = "+419+422",
    font = "Helvetica"
  )

image_write(canvas, "man/figures/social-preview.png", format = "png")
unlink(tmp_bg)
cat("Saved artsy man/figures/social-preview.png (1280x640)\n")
