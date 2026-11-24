#' @keywords internal
#' @aliases tncensus-package
"_PACKAGE"

.onAttach <- function(libname, pkgname) {
  packageStartupMessage(
    "tncensus ", utils::packageVersion("tncensus"), "\n",
    "Tunisia Census Data: Harmonized 2014-2024 Panel + Full RGPH 2014 & RGPH 2024"
  )
}
