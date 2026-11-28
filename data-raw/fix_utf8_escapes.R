# Decode literal UTF-8 byte escapes in the package's datasets (data/*.rda).
#
# Some text cells stored their UTF-8 bytes as escape text: "Béja" was stored as
# the 11-character string "B<c3><a9>ja". This rewrites each run of "<xx>"
# escapes as the bytes it spells, marks the result as UTF-8, and re-saves only
# the datasets that changed (same object name, xz compression).
#
# Run once from the repository root:  Rscript data-raw/fix_utf8_escapes.R
# The Parquet files in inst/extdata are fixed by data-raw/fix_utf8_escapes.py.

decode_escapes <- function(x) {
  hit <- !is.na(x) & grepl("<[0-9a-f]{2}>", x)
  if (!any(hit)) return(x)
  x[hit] <- vapply(x[hit], function(s) {
    m <- gregexpr("(<[0-9a-f]{2}>)+", s)
    runs <- regmatches(s, m)[[1]]
    dec <- vapply(runs, function(r) {
      hex <- regmatches(r, gregexpr("[0-9a-f]{2}", r))[[1]]
      out <- rawToChar(as.raw(strtoi(hex, 16L)))
      Encoding(out) <- "UTF-8"
      out
    }, character(1), USE.NAMES = FALSE)
    regmatches(s, m) <- list(dec)
    s
  }, character(1), USE.NAMES = FALSE)
  stopifnot(all(validUTF8(x[hit])))
  enc2utf8(x)
}

for (f in list.files("data", pattern = "\\.rda$", full.names = TRUE)) {
  env <- new.env()
  nm <- load(f, envir = env)
  changed <- 0L
  for (n in nm) {
    d <- get(n, envir = env)
    if (!is.data.frame(d)) next
    for (col in names(d)) {
      if (is.character(d[[col]])) {
        new <- decode_escapes(d[[col]])
        changed <- changed + sum(new != d[[col]], na.rm = TRUE)
        d[[col]] <- new
      }
    }
    assign(n, d, envir = env)
  }
  if (changed > 0L) {
    save(list = nm, envir = env, file = f, compress = "xz")
    cat(sprintf("%s: %d cells decoded\n", f, changed))
  }
}
