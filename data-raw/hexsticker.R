# Generate tncensus hex sticker (Clean Statistical / tidycensus-inspired Style)
library(ggplot2)
library(sf)
library(hexSticker)

make_circle <- function(cx, cy, r, n = 300) {
  theta <- seq(0, 2 * pi, length.out = n)
  data.frame(x = cx + r * cos(theta), y = cy + r * sin(theta))
}

make_crescent_sf <- function(cx, cy, r_out, dx, r_in) {
  c_out <- make_circle(cx, cy, r_out, 300)
  c_in  <- make_circle(cx + dx, cy, r_in, 300)
  p_out <- st_polygon(list(as.matrix(rbind(c_out, c_out[1, ]))))
  p_in  <- st_polygon(list(as.matrix(rbind(c_in, c_in[1, ]))))
  st_difference(p_out, p_in)
}

make_star <- function(cx, cy, r_outer, r_inner, angle_offset = pi) {
  angles <- seq(0, 2 * pi, length.out = 11)[-11] + angle_offset
  radii <- rep(c(r_outer, r_inner), 5)
  data.frame(x = cx + radii * cos(angles), y = cy + radii * sin(angles))
}

# Clean 5-bar census distribution (tall, balanced proportions)
bars <- data.frame(
  x = 1:5,
  y = c(0.95, 1.55, 2.25, 2.85, 1.85),
  fill = c("#0d9488", "#14b8a6", "#2dd4bf", "#38bdf8", "#7dd3fc")
)

# Subtle crescent & star in the upper-left negative space
crescent_sf <- st_sfc(make_crescent_sf(1.25, 2.45, 0.42, 0.12, 0.335))
star_df <- make_star(1.41, 2.45, 0.15, 0.06, angle_offset = pi)

p <- ggplot() +
  # Subtle horizontal reference grid lines
  annotate("segment", x = 0.5, xend = 5.5, y = 0.75, yend = 0.75,
           color = "#1e293b", linewidth = 0.3) +
  annotate("segment", x = 0.5, xend = 5.5, y = 1.50, yend = 1.50,
           color = "#1e293b", linewidth = 0.3) +
  annotate("segment", x = 0.5, xend = 5.5, y = 2.25, yend = 2.25,
           color = "#1e293b", linewidth = 0.3) +
  annotate("segment", x = 0.5, xend = 5.5, y = 3.00, yend = 3.00,
           color = "#1e293b", linewidth = 0.3) +
  # Statistical bars
  geom_col(data = bars, aes(x = x, y = y, fill = fill), width = 0.62) +
  scale_fill_identity() +
  # Baseline
  annotate("segment", x = 0.45, xend = 5.55, y = 0, yend = 0,
           color = "#64748b", linewidth = 0.45) +
  # Subtle crescent & star mark
  geom_sf(data = crescent_sf, fill = "#e2e8f0", color = NA) +
  geom_polygon(data = star_df, aes(x = x, y = y), fill = "#e2e8f0") +
  coord_sf(xlim = c(0.4, 5.6), ylim = c(-0.10, 3.15), datum = NA) +
  theme_void() +
  theme(
    plot.background = element_rect(fill = "transparent", color = NA),
    panel.background = element_rect(fill = "transparent", color = NA)
  )

dir.create("man/figures", recursive = TRUE, showWarnings = FALSE)

sticker(
  p,
  package = "tncensus",
  p_size = 22,
  p_y = 1.44,
  p_color = "#f8fafc",
  p_fontface = "bold",
  s_x = 1.0,
  s_y = 0.78,
  s_width = 1.15,
  s_height = 0.95,
  h_fill = "#0f172a",
  h_color = "#2dd4bf",
  h_size = 1.8,
  filename = "man/figures/logo.png",
  dpi = 300
)
