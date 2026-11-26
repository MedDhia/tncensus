#' Harmonized Tunisian Census Panel, 2014--2024
#'
#' Delegation-level data harmonizing the 2014 and 2024 Tunisian RGPH.
#' Contains 45 socioeconomic indicators with `_2014`, `_2024`, and
#' `_change` suffixes. All percentages on a 0--100 scale.
#'
#' @format A data frame with 281 rows and 144 columns. Nine identifier
#'   columns (governorate, delegation names in French and Arabic, region,
#'   coordinates, match flag) plus 45 indicators x 3 suffixes = 135
#'   indicator columns. See \code{\link{codebook}} for variable details.
#'
#' @source Institut National de la Statistique (INS), Republic of Tunisia,
#'   compiled in \code{replication_package_ben_salah_al_2024}
#'   (Ben Salah et al., 2024 (\doi{10.1016/j.jce.2024.09.002})).
#'   RGPH 2014 and RGPH 2024.
#'
#' @examples
#' data(census_panel)
#' dim(census_panel)
#' aggregate(unemployment_rate_change ~ region_2024,
#'           data = census_panel, FUN = mean, na.rm = TRUE)
"census_panel"


#' Delegation Name Crosswalk, 2014--2024
#'
#' Maps 263 delegation names from the 2014 RGPH to their 2024 equivalents
#' (193 exact matches, 70 fuzzy matches within governorates).
#'
#' @format A data frame with 263 rows and 5 columns:
#' \describe{
#'   \item{delegation_2014}{Delegation name, 2014 spelling.}
#'   \item{gov_2014}{Governorate name, 2014 spelling.}
#'   \item{delegation_2024}{Delegation name, 2024 spelling.}
#'   \item{gov_2024}{Governorate name, 2024 spelling.}
#'   \item{match_type}{\code{"exact"} or \code{"fuzzy"}.}
#' }
#'
#' @source Constructed from delegation lists in the 2014 and 2024 RGPH
#'   files (INS Tunisia).
#'
#' @examples
#' data(delegation_crosswalk)
#' table(delegation_crosswalk$match_type)
"delegation_crosswalk"


#' Codebook: Variable-Level Metadata
#'
#' Documents all 45 harmonized indicators in \code{\link{census_panel}}.
#'
#' @format A data frame with 45 rows and 5 columns:
#' \describe{
#'   \item{variable}{Harmonized variable stem (without `_2014`/`_2024`/`_change`).}
#'   \item{domain}{Thematic domain.}
#'   \item{label}{Human-readable description.}
#'   \item{unit}{"percentage (0-100)" or "count".}
#'   \item{note}{Denominator, data gaps, or comparability caveats.}
#' }
#'
#' @source Constructed during harmonization. See
#'   \code{system.file("extdata", "harmonization_log.md", package = "tncensus")}
#'
#' @examples
#' data(codebook)
#' unique(codebook$domain)
"codebook"

#' Merged Delegation-Level Census Data (RGPH 2014)
#'
#' A pre-merged dataset containing 264 delegations (second administrative
#' level) nested within 24 governorates, with 169 variables from the 2014
#' Tunisian census. This is the total population, both sexes, communal
#' milieu slice. Each row is one delegation.
#'
#' @format A \code{data.frame} with 264 rows and 169 columns:
#'
#' \describe{
#'
#'   \strong{--- Geographic identifiers (3 variables) ---}
#'   \item{\code{governorate}}{Governorate name (24 unique). Character.}
#'   \item{\code{delegation_ar}}{Delegation name in Arabic. Character.}
#'   \item{\code{delegation_fr}}{Delegation name in French. Character.}
#'
#'   \strong{--- Demography: marital status (5 variables) ---}
#'   \item{\code{pop_15plus}}{Population aged 15 and above. Integer.}
#'   \item{\code{pct_celibataire}}{Percent never married (of pop 15+). Numeric.}
#'   \item{\code{pct_marie}}{Percent married (of pop 15+). Numeric.}
#'   \item{\code{pct_veuf}}{Percent widowed (of pop 15+). Numeric.}
#'   \item{\code{pct_divorce}}{Percent divorced (of pop 15+). Numeric.}
#'
#'   \strong{--- Demography: age structure (10 variables) ---}
#'   \item{\code{population}}{Total delegation population. Integer.}
#'   \item{\code{pct_0_4}}{Percent aged 0-4. Numeric.}
#'   \item{\code{pct_5_9}}{Percent aged 5-9. Numeric.}
#'   \item{\code{pct_10_14}}{Percent aged 10-14. Numeric.}
#'   \item{\code{pct_15_19}}{Percent aged 15-19. Numeric.}
#'   \item{\code{pct_20_29}}{Percent aged 20-29. Numeric.}
#'   \item{\code{pct_30_39}}{Percent aged 30-39. Numeric.}
#'   \item{\code{pct_40_49}}{Percent aged 40-49. Numeric.}
#'   \item{\code{pct_50_59}}{Percent aged 50-59. Numeric.}
#'   \item{\code{pct_60plus}}{Percent aged 60 and over. Numeric.}
#'
#'   \strong{--- Education (10 variables) ---}
#'   \item{\code{pop_10plus_educ}}{Population aged 10+ (education denominator). Integer.}
#'   \item{\code{pct_neant_educ}}{Percent with no formal education (of pop 10+). Numeric.}
#'   \item{\code{pct_primaire_educ}}{Percent with primary education (of pop 10+). Numeric.}
#'   \item{\code{pct_secondaire_educ}}{Percent with secondary education (of pop 10+). Numeric.}
#'   \item{\code{pct_superieur_educ}}{Percent with higher education (of pop 10+). Numeric.}
#'   \item{\code{pct_analphabete_10plus}}{Illiteracy rate among pop 10+. Numeric.}
#'   \item{\code{pct_analph_jeunes_15_29}}{Youth illiteracy rate ages 15-29. Numeric.}
#'   \item{\code{pct_scolarisation_6_14}}{School enrollment rate ages 6-14. Numeric.}
#'   \item{\code{pct_scol_superieur_19_24}}{Higher education enrollment rate ages 19-24. Numeric.}
#'   \item{\code{pct_internet_10plus}}{Internet usage rate among pop 10+. Numeric.}
#'
#'   \strong{--- Employment: labour force (6 variables) ---}
#'   \item{\code{pop_15plus_econ}}{Population 15+ (economic activity denominator). Integer.}
#'   \item{\code{pct_actifs_occupes}}{Number of employed persons. Integer.}
#'   \item{\code{pct_chomeurs}}{Number of unemployed persons. Integer.}
#'   \item{\code{pct_taux_activite}}{Labour force participation rate. Integer.}
#'   \item{\code{pct_taux_emploi}}{Employment rate (of pop 15+). Numeric.}
#'   \item{\code{pct_taux_chomage}}{Unemployment rate (of active pop). Numeric.}
#'
#'   \strong{--- Employment: employed by education (5 variables) ---}
#'   \item{\code{occupes_15plus}}{Employed persons aged 15+. Integer.}
#'   \item{\code{pct_occ_neant}}{Percent of employed with no education. Numeric.}
#'   \item{\code{pct_occ_primaire}}{Percent of employed with primary education. Numeric.}
#'   \item{\code{pct_occ_secondaire}}{Percent of employed with secondary education. Numeric.}
#'   \item{\code{pct_occ_superieur}}{Percent of employed with higher education. Numeric.}
#'
#'   \strong{--- Employment: employed by sector (10 variables) ---}
#'   \item{\code{occupes_sect}}{Total employed by sector (denominator). Numeric.}
#'   \item{\code{pct_agriculture}}{Percent in agriculture. Numeric.}
#'   \item{\code{pct_mines_energie}}{Percent in mining and energy. Numeric.}
#'   \item{\code{pct_industrie}}{Percent in manufacturing. Numeric.}
#'   \item{\code{pct_batiment}}{Percent in construction. Numeric.}
#'   \item{\code{pct_commerce}}{Percent in commerce and trade. Numeric.}
#'   \item{\code{pct_transport}}{Percent in transport. Numeric.}
#'   \item{\code{pct_educ_sante_admin}}{Percent in education, health, and admin. Numeric.}
#'   \item{\code{pct_autres_services}}{Percent in other services. Numeric.}
#'   \item{\code{pct_non_declare_sect}}{Percent in undeclared sector. Numeric.}
#'
#'   \strong{--- Employment: unemployed by education (6 variables) ---}
#'   \item{\code{chomeurs_15plus}}{Unemployed persons aged 15+. Integer.}
#'   \item{\code{pct_chom_neant}}{Percent of unemployed with no education. Numeric.}
#'   \item{\code{pct_chom_primaire}}{Percent of unemployed with primary education. Numeric.}
#'   \item{\code{pct_chom_secondaire}}{Percent of unemployed with secondary education. Numeric.}
#'   \item{\code{pct_chom_superieur}}{Percent of unemployed with higher education. Numeric.}
#'   \item{\code{taux_chomage_diplomes_sup}}{Unemployment rate among higher ed graduates. Numeric.}
#'
#'   \strong{--- Employment: unemployed by age (10 variables) ---}
#'   \item{\code{chomeurs_age_total}}{Total unemployed by age (denominator). Numeric.}
#'   \item{\code{pct_chom_15_19}}{Percent of unemployed aged 15-19. Numeric.}
#'   \item{\code{pct_chom_20_24}}{Percent of unemployed aged 20-24. Numeric.}
#'   \item{\code{pct_chom_25_29}}{Percent of unemployed aged 25-29. Numeric.}
#'   \item{\code{pct_chom_30_34}}{Percent of unemployed aged 30-34. Numeric.}
#'   \item{\code{pct_chom_35_39}}{Percent of unemployed aged 35-39. Numeric.}
#'   \item{\code{pct_chom_40_44}}{Percent of unemployed aged 40-44. Numeric.}
#'   \item{\code{pct_chom_45_49}}{Percent of unemployed aged 45-49. Numeric.}
#'   \item{\code{pct_chom_50_59}}{Percent of unemployed aged 50-59. Numeric.}
#'   \item{\code{pct_chom_60plus}}{Percent of unemployed aged 60+. Numeric.}
#'
#'   \strong{--- International migration (9 variables) ---}
#'   \item{\code{immigrants}}{Number of international immigrants. Numeric.}
#'   \item{\code{emigrants}}{Number of international emigrants. Numeric.}
#'   \item{\code{solde_migratoire}}{Net migration balance. Numeric.}
#'   \item{\code{pct_mig_emploi}}{Percent migrating for employment. Numeric.}
#'   \item{\code{pct_mig_logement}}{Percent migrating for housing. Numeric.}
#'   \item{\code{pct_mig_mariage}}{Percent migrating for marriage. Numeric.}
#'   \item{\code{pct_mig_famille}}{Percent migrating for family. Numeric.}
#'   \item{\code{pct_mig_etudes}}{Percent migrating for studies. Numeric.}
#'   \item{\code{pct_mig_autres}}{Percent migrating for other reasons. Numeric.}
#'
#'   \strong{--- Internal migration (10 variables) ---}
#'   \item{\code{mig_inter_V2}}{Internal in-migrants. Numeric.}
#'   \item{\code{mig_inter_V3}}{Internal out-migrants. Numeric.}
#'   \item{\code{mig_inter_V4}}{Non-migrants. Numeric.}
#'   \item{\code{mig_inter_V5}}{Net internal migration balance. Numeric.}
#'   \item{\code{mig_inter_V6}}{Internal migration percent for employment. Numeric.}
#'   \item{\code{mig_inter_V7}}{Internal migration percent for housing. Numeric.}
#'   \item{\code{mig_inter_V8}}{Internal migration percent for marriage. Numeric.}
#'   \item{\code{mig_inter_V9}}{Internal migration percent for family. Numeric.}
#'   \item{\code{mig_inter_V10}}{Internal migration percent for studies. Numeric.}
#'   \item{\code{mig_inter_V11}}{Internal migration percent for other reasons. Numeric.}
#'
#'   \strong{--- Household: water access (5 variables) ---}
#'   \item{\code{pct_plus_1km_eau}}{Percent of households > 1 km from water. Numeric.}
#'   \item{\code{pct_source_non_ctrl}}{Percent using uncontrolled water source. Numeric.}
#'   \item{\code{pct_autre_source}}{Percent using other water source. Numeric.}
#'   \item{\code{pct_source_publique}}{Percent using public water source. Numeric.}
#'   \item{\code{pct_eau_robinet}}{Percent with piped tap water. Numeric.}
#'
#'   \strong{--- Household: energy (5 variables) ---}
#'   \item{\code{pct_gaz_chauffage}}{Percent using gas for heating. Numeric.}
#'   \item{\code{pct_gaz_eau_chaude}}{Percent using gas for hot water. Numeric.}
#'   \item{\code{pct_gaz_cuisine}}{Percent using gas for cooking. Numeric.}
#'   \item{\code{pct_autre_eclairage}}{Percent with non-electric lighting. Numeric.}
#'   \item{\code{pct_electricite}}{Percent with electricity access. Numeric.}
#'
#'   \strong{--- Household: tenure (6 variables) ---}
#'   \item{\code{pct_prop_autre}}{Percent other property tenure. Numeric.}
#'   \item{\code{pct_prop_achat}}{Percent purchased property. Numeric.}
#'   \item{\code{pct_prop_auto_constr}}{Percent self-built property. Numeric.}
#'   \item{\code{pct_occup_autre}}{Percent other occupancy type. Numeric.}
#'   \item{\code{pct_locataire}}{Percent renting. Numeric.}
#'   \item{\code{pct_proprietaire}}{Percent homeowners. Numeric.}
#'
#'   \strong{--- Household: entertainment (5 variables) ---}
#'   \item{\code{pct_bibliotheque}}{Percent with home library. Numeric.}
#'   \item{\code{pct_parabole}}{Percent with satellite dish. Numeric.}
#'   \item{\code{pct_tv}}{Percent with television. Numeric.}
#'   \item{\code{pct_radio}}{Percent with radio. Numeric.}
#'   \item{\code{pct_voiture}}{Percent with car. Numeric.}
#'
#'   \strong{--- Household: equipment (6 variables) ---}
#'   \item{\code{pct_chauffage_central}}{Percent with central heating. Numeric.}
#'   \item{\code{pct_climatiseur}}{Percent with air conditioning. Numeric.}
#'   \item{\code{pct_lave_vaisselle}}{Percent with dishwasher. Numeric.}
#'   \item{\code{pct_machine_laver}}{Percent with washing machine. Numeric.}
#'   \item{\code{pct_cuisiniere}}{Percent with stove or oven. Numeric.}
#'   \item{\code{pct_refrigerateur}}{Percent with refrigerator. Numeric.}
#'
#'   \strong{--- Household: communication (4 variables) ---}
#'   \item{\code{pct_internet_menage}}{Percent with household internet. Numeric.}
#'   \item{\code{pct_ordinateur}}{Percent with computer. Numeric.}
#'   \item{\code{pct_tel_portable}}{Percent with mobile phone. Numeric.}
#'   \item{\code{pct_tel_fixe}}{Percent with landline phone. Numeric.}
#'
#'   \strong{--- Housing: dwelling type (5 variables) ---}
#'   \item{\code{pct_rudimentaire}}{Percent rudimentary dwellings. Numeric.}
#'   \item{\code{pct_appartement}}{Percent apartments. Numeric.}
#'   \item{\code{pct_villa_duplex}}{Percent villas or duplexes. Numeric.}
#'   \item{\code{pct_jumele}}{Percent semi-detached houses. Numeric.}
#'   \item{\code{pct_dar_arbi}}{Percent traditional houses (dar arbi). Numeric.}
#'
#'   \strong{--- Housing: number of rooms (5 variables) ---}
#'   \item{\code{pct_5pieces_plus}}{Percent with 5+ rooms. Numeric.}
#'   \item{\code{pct_4pieces}}{Percent with 4 rooms. Numeric.}
#'   \item{\code{pct_3pieces}}{Percent with 3 rooms. Numeric.}
#'   \item{\code{pct_2pieces}}{Percent with 2 rooms. Numeric.}
#'   \item{\code{pct_1piece}}{Percent with 1 room. Numeric.}
#'
#'   \strong{--- Housing: floor area (5 variables) ---}
#'   \item{\code{pct_plus_200m2}}{Percent with area over 200 m2. Numeric.}
#'   \item{\code{pct_150_199m2}}{Percent with area 150-199 m2. Numeric.}
#'   \item{\code{pct_100_149m2}}{Percent with area 100-149 m2. Numeric.}
#'   \item{\code{pct_50_99m2}}{Percent with area 50-99 m2. Numeric.}
#'   \item{\code{pct_moins_50m2}}{Percent with area under 50 m2. Numeric.}
#'
#'   \strong{--- Housing: occupancy status (5 variables) ---}
#'   \item{\code{pct_en_construction}}{Percent under construction. Numeric.}
#'   \item{\code{pct_abandonne}}{Percent abandoned. Numeric.}
#'   \item{\code{pct_vacant}}{Percent vacant. Numeric.}
#'   \item{\code{pct_secondaire_log}}{Percent secondary or vacation homes. Numeric.}
#'   \item{\code{pct_occupe}}{Percent occupied. Numeric.}
#'
#'   \strong{--- Housing: infrastructure (4 variables) ---}
#'   \item{\code{pct_assainissement}}{Percent with sewerage connection. Numeric.}
#'   \item{\code{pct_eau_potable_sonede}}{Percent with SONEDE drinking water. Numeric.}
#'   \item{\code{pct_gaz_naturel_log}}{Percent with natural gas connection. Numeric.}
#'   \item{\code{pct_electricite_steg}}{Percent with STEG electricity. Numeric.}
#'
#'   \strong{--- Housing: facilities (6 variables) ---}
#'   \item{\code{nb_sans_cuisine}}{Dwellings without kitchen (count). Numeric.}
#'   \item{\code{nb_sans_toilette}}{Dwellings without toilet (count). Numeric.}
#'   \item{\code{nb_sans_sdb}}{Dwellings without bathroom (count). Numeric.}
#'   \item{\code{pct_avec_cuisine}}{Percent with kitchen. Numeric.}
#'   \item{\code{pct_avec_toilette}}{Percent with toilet. Numeric.}
#'   \item{\code{pct_avec_sdb}}{Percent with bathroom. Numeric.}
#'
#'   \strong{--- Distance to services: primary schools (6 variables) ---}
#'   \item{\code{pct_ecole_plus2km}}{Percent over 2 km from primary school. Numeric.}
#'   \item{\code{pct_ecole_1_2km}}{Percent 1-2 km from primary school. Numeric.}
#'   \item{\code{pct_ecole_moins1km}}{Percent under 1 km from primary school. Numeric.}
#'   \item{\code{pct_jardin_plus2km}}{Percent over 2 km from kindergarten. Numeric.}
#'   \item{\code{pct_jardin_1_2km}}{Percent 1-2 km from kindergarten. Numeric.}
#'   \item{\code{pct_jardin_moins1km}}{Percent under 1 km from kindergarten. Numeric.}
#'
#'   \strong{--- Distance to services: secondary schools (6 variables) ---}
#'   \item{\code{pct_lycee_plus2km}}{Percent over 2 km from lycee. Numeric.}
#'   \item{\code{pct_lycee_1_2km}}{Percent 1-2 km from lycee. Numeric.}
#'   \item{\code{pct_lycee_moins1km}}{Percent under 1 km from lycee. Numeric.}
#'   \item{\code{pct_college_plus2km}}{Percent over 2 km from middle school. Numeric.}
#'   \item{\code{pct_college_1_2km}}{Percent 1-2 km from middle school. Numeric.}
#'   \item{\code{pct_college_moins1km}}{Percent under 1 km from middle school. Numeric.}
#'
#'   \strong{--- Distance to services: health (6 variables) ---}
#'   \item{\code{pct_hopital_plus2km}}{Percent over 2 km from hospital. Numeric.}
#'   \item{\code{pct_hopital_1_2km}}{Percent 1-2 km from hospital. Numeric.}
#'   \item{\code{pct_hopital_moins1km}}{Percent under 1 km from hospital. Numeric.}
#'   \item{\code{pct_dispensaire_plus2km}}{Percent over 2 km from dispensary. Numeric.}
#'   \item{\code{pct_dispensaire_1_2km}}{Percent 1-2 km from dispensary. Numeric.}
#'   \item{\code{pct_dispensaire_moins1km}}{Percent under 1 km from dispensary. Numeric.}
#'
#'   \strong{--- Distance to services: sports and youth (6 variables) ---}
#'   \item{\code{pct_sport_plus2km}}{Percent over 2 km from sports facility. Numeric.}
#'   \item{\code{pct_sport_1_2km}}{Percent 1-2 km from sports facility. Numeric.}
#'   \item{\code{pct_sport_moins1km}}{Percent under 1 km from sports facility. Numeric.}
#'   \item{\code{pct_jeunes_plus2km}}{Percent over 2 km from youth center. Numeric.}
#'   \item{\code{pct_jeunes_1_2km}}{Percent 1-2 km from youth center. Numeric.}
#'   \item{\code{pct_jeunes_moins1km}}{Percent under 1 km from youth center. Numeric.}
#' }
#'
#' @source Institut National de la Statistique (INS), Republic of Tunisia,
#'   compiled in \code{replication_package_ben_salah_al_2024}
#'   (Ben Salah et al., 2024 (\doi{10.1016/j.jce.2024.09.002})).
#'   Recensement General de la Population et de l'Habitat 2014.
#'   \url{https://www.ins.tn/}
#'
#' @examples
#' # Basic exploration
#' data(rgph_master)
#' dim(rgph_master)
#' head(rgph_master[, 1:6])
#'
#' # Governorate-level summaries
#' tapply(rgph_master$unemployment_rate, rgph_master$governorate, mean,
#'        na.rm = TRUE)
#'
#' # Correlation between water infrastructure and school enrollment
#' with(rgph_master,
#'   cor(pct_sonede_water, pct_enrollment_6_14,
#'       use = "complete.obs"))
"rgph_master"


#' Tunisia 2004 Census Data (RGPH 2004)
#'
#' Delegation-, governorate-, and national-level results from the 2004
#' General Population and Housing Census of Tunisia (RGPH), conducted by
#' the Institut National de la Statistique (INS). Covers population by sex,
#' school enrollment (ages 6-14 and 19-24), educational attainment (ages 10+),
#' illiteracy, labour force participation, unemployment rates, and unemployed
#' counts by education, disaggregated by total, men, and women.
#'
#' @format A \code{data.frame} with 289 rows (264 delegations, 24 governorate
#'   totals, and 1 national total) and 54 columns, including identifiers
#'   (\code{id}, \code{delegation_id}, \code{delegation_name},
#'   \code{delegation_name_ar}, \code{governorate_id}, \code{level}) and
#'   48 demographic, education, and labour-market indicators.
#'
#' @source Institut National de la Statistique (INS), Republic of Tunisia,
#'   compiled in \code{replication_package_ben_salah_al_2024}
#'   (Ben Salah et al., 2024 (\doi{10.1016/j.jce.2024.09.002})).
#'   Recensement General de la Population et de l'Habitat 2004, compiled in
#'   \code{replication_package_ben_salah_al_2024} (Ben Salah et al., 2024 (\doi{10.1016/j.jce.2024.09.002})).
#'
#' @examples
#' data(rgph2004)
#' table(rgph2004$level)
#' del04 <- rgph2004[rgph2004$level == "delegation", ]
#' summary(del04$pct_unemployment_2004)
"rgph2004"


#' Tunisia 1984 Census Education Data (RGPH 1984)
#'
#' Tidy delegation-level education tables from the 1984 General Population
#' and Housing Census of Tunisia (RGPH), disaggregated by delegation, sex,
#' indicator table, category, and age group.
#'
#' @format A \code{data.frame} with 55,720 rows and 6 columns:
#' \describe{
#'   \item{delegation_id}{INS delegation code (integer).}
#'   \item{sex}{\code{"male"} or \code{"female"}.}
#'   \item{table}{\code{"literacy"}, \code{"education_level"}, or
#'     \code{"school_attendance"}.}
#'   \item{category}{Response category label (e.g., literacy language,
#'     education level, or attendance status).}
#'   \item{age_group}{Age bracket (e.g., \code{"10-14 ans"}).}
#'   \item{count}{Population count (numeric).}
#' }
#'
#' @source Institut National de la Statistique (INS), Republic of Tunisia,
#'   compiled in \code{replication_package_ben_salah_al_2024}
#'   (Ben Salah et al., 2024 (\doi{10.1016/j.jce.2024.09.002})).
#'   Recensement General de la Population et de l'Habitat 1984, compiled in
#'   \code{replication_package_ben_salah_al_2024} (Ben Salah et al., 2024 (\doi{10.1016/j.jce.2024.09.002})).
#'
#' @examples
#' data(rgph1984_education)
#' table(rgph1984_education$table, rgph1984_education$sex)
"rgph1984_education"


#' Historical National Literacy and School Enrollment (1956--2014)
#'
#' National-level literacy rate and 6-14 school enrollment rate across
#' seven Tunisian population censuses from 1956 to 2014.
#'
#' @format A \code{data.frame} with 7 rows and 3 columns:
#' \describe{
#'   \item{year}{Census year (1956, 1966, 1975, 1984, 1994, 2004, 2014).}
#'   \item{literacy_rate}{National literacy rate (percent).}
#'   \item{enrolment_rate_6_14}{School enrollment rate for ages 6-14
#'     (percent; \code{NA} for 1956 and 1966).}
#' }
#'
#' @source Institut National de la Statistique (INS), Republic of Tunisia,
#'   compiled in \code{replication_package_ben_salah_al_2024}
#'   (Ben Salah et al., 2024 (\doi{10.1016/j.jce.2024.09.002})).
#'
#' @examples
#' data(historical_education)
#' historical_education
"historical_education"


#' Master INS Delegation Code Crosswalk (1984--2024)
#'
#' Reference table of 264 Tunisian delegations linking 1984 INS delegation
#' codes, contemporary INS delegation codes, UN SALB identifiers, region
#' and governorate names, and geographic coordinates.
#'
#' @format A \code{data.frame} with 264 rows and 11 columns:
#'   \code{id}, \code{region_name}, \code{governorate_name},
#'   \code{delegation_name}, \code{delegation_id}, \code{delegation_id_merged},
#'   \code{delegation_id_salb_un}, \code{delegation_id_1984}, \code{lat},
#'   \code{lon}, and \code{comments}.
#'
#' @source Institut National de la Statistique (INS) and UN SALB.
#'
#' @examples
#' data(delegation_codes_ins)
#' head(delegation_codes_ins[, 1:6])
"delegation_codes_ins"


#' Tunisia 1966 Census Illiteracy and Enrollment by Governorate
#'
#' Governorate-level illiteracy rates and male school enrollment rates by
#' age bracket from the 1966 Tunisian population census.
#'
#' @format A \code{data.frame} with 14 rows and 8 columns:
#'   \code{id}, \code{year}, \code{governorate_name}, \code{pct_pop_illiterate},
#'   \code{enrolment_rate_male_6_9yo}, \code{enrolment_rate_male_10_14yo},
#'   \code{enrolment_rate_male_15_19yo}, and \code{comments}.
#'
#' @source Mahmoud Seklani (1974), La population de la Tunisie, CICRED,
#'   pp. 104-107 (based on INS 1966 Census).
#'
#' @examples
#' data(rgph1966_illiteracy)
#' rgph1966_illiteracy[, c("governorate_name", "pct_pop_illiterate")]
"rgph1966_illiteracy"


#' Tunisian Population Censuses, 1926--1956 (Locality Level)
#'
#' Historical locality-level counts of Tunisian Muslim and Jewish
#' populations across the 1926, 1931, 1936, 1946, and 1956 censuses, linked
#' to colonial caidats, controles civils, 1957 delegations, and modern
#' delegation IDs.
#'
#' @format A \code{data.frame} with 871 rows and 26 columns.
#'
#' @source French Protectorate population censuses of Tunisia (1926-1956),
#'   compiled in \code{replication_package_ben_salah_al_2024}
#'   (Ben Salah et al., 2024 (\doi{10.1016/j.jce.2024.09.002})).
#'
#' @examples
#' data(colonial_tunisian_pop)
#' dim(colonial_tunisian_pop)
"colonial_tunisian_pop"


#' European Population Censuses in Tunisia, 1891--1936 (Locality Level)
#'
#' Historical locality-level counts of French, Italian, and total European
#' populations in Tunisia across nine censuses from 1891 to 1936.
#'
#' @format A \code{data.frame} with 525 rows and 24 columns.
#'
#' @source French Protectorate population censuses of Tunisia (1891-1936),
#'   compiled in \code{replication_package_ben_salah_al_2024}
#'   (Ben Salah et al., 2024 (\doi{10.1016/j.jce.2024.09.002})).
#'
#' @examples
#' data(colonial_european_pop)
#' dim(colonial_european_pop)
"colonial_european_pop"


#' 1931 Census Age Structure by Caidat
#'
#' Adult and child population counts by sex for Tunisian Muslim and Jewish
#' populations across 37 caidats in the 1931 census.
#'
#' @format A \code{data.frame} with 37 rows and 14 columns.
#'
#' @source French Protectorate population census of Tunisia (1931),
#'   compiled in \code{replication_package_ben_salah_al_2024}
#'   (Ben Salah et al., 2024 (\doi{10.1016/j.jce.2024.09.002})).
#'
#' @examples
#' data(colonial_age_caidat_1931)
#' head(colonial_age_caidat_1931[, 1:5])
"colonial_age_caidat_1931"


#' 1931 Census Age Structure by Controle Civil
#'
#' European, Muslim, and Jewish population counts and European age-group
#' breakdowns across 21 controles civils in the 1931 census.
#'
#' @format A \code{data.frame} with 21 rows and 15 columns.
#'
#' @source French Protectorate population census of Tunisia (1931),
#'   compiled in \code{replication_package_ben_salah_al_2024}
#'   (Ben Salah et al., 2024 (\doi{10.1016/j.jce.2024.09.002})).
#'
#' @examples
#' data(colonial_age_controle_civil_1931)
#' head(colonial_age_controle_civil_1931[, 1:5])
"colonial_age_controle_civil_1931"


#' Historical Tunisian Geonames and Place-Name Crosswalk (1891--2024)
#'
#' Harmonizes 1,276 historical and colonial-era locality names (e.g., French
#' Protectorate spellings) to modern Tunisian place names, GeoNames IDs,
#' 1926/1931 caidats, 1931 civil controls, 1956 delegations, and modern
#' coordinates.
#'
#' @format A \code{data.frame} with 1,276 rows and 14 columns:
#'   \code{locality_id_2024}, \code{census_record_id},
#'   \code{locality_name_source}, \code{locality_name_modern},
#'   \code{geonames_id}, \code{caidat_1926}, \code{caidat_1931},
#'   \code{civil_control_1931}, \code{delegation_1956}, \code{lat}, \code{lon},
#'   \code{sources_lat_lon}, \code{comments}, and \code{geo_precision}.
#'
#' @source Compiled in \code{replication_package_ben_salah_al_2024} by
#'   Ben Salah et al., 2024 (\doi{10.1016/j.jce.2024.09.002}).
#'
#' @examples
#' data(historical_geonames)
#' head(historical_geonames[, c("locality_name_source", "locality_name_modern", "lat", "lon")])
"historical_geonames"


#' 2014 Delegation Reference Matrix with Centroids
#'
#' Reference table of 264 Tunisian delegations in the 2014 census with
#' governorate codes, delegation names, and polygon centroid coordinates.
#'
#' @format A \code{data.frame} with 264 rows and 5 columns:
#'   \code{governorate_id}, \code{delegation_id}, \code{delegation_name},
#'   \code{lon_centroid}, and \code{lat_centroid}.
#'
#' @source Compiled in \code{replication_package_ben_salah_al_2024} by
#'   Ben Salah et al., 2024 (\doi{10.1016/j.jce.2024.09.002}).
#'
#' @examples
#' data(delegation_matrix_2014)
#' head(delegation_matrix_2014)
"delegation_matrix_2014"


#' 1984 Delegation Reference Matrix with Centroids
#'
#' Reference table of 198 Tunisian delegations in the 1984 census with
#' region/governorate names, delegation names, and centroid coordinates.
#'
#' @format A \code{data.frame} with 198 rows and 7 columns:
#'   \code{governorate_id}, \code{delegation_id}, \code{region_name},
#'   \code{governorate_name}, \code{delegation_name}, \code{lon_centroid},
#'   and \code{lat_centroid}.
#'
#' @source Compiled in \code{replication_package_ben_salah_al_2024} by
#'   Ben Salah et al., 2024 (\doi{10.1016/j.jce.2024.09.002}).
#'
#' @examples
#' data(delegation_matrix_1984)
#' head(delegation_matrix_1984)
"delegation_matrix_1984"


#' Time-Consistent Merged Delegation Matrix (1984--2014)
#'
#' Harmonized reference table of 217 time-consistent merged delegations
#' reconciling boundary splits between the 1984 and 2014 Tunisian censuses.
#'
#' @format A \code{data.frame} with 217 rows and 5 columns:
#'   \code{governorate_id}, \code{delegation_id}, \code{delegation_name},
#'   \code{lon_centroid}, and \code{lat_centroid}.
#'
#' @source Compiled in \code{replication_package_ben_salah_al_2024} by
#'   Ben Salah et al., 2024 (\doi{10.1016/j.jce.2024.09.002}).
#'
#' @examples
#' data(delegation_matrix_merged)
#' head(delegation_matrix_merged)
"delegation_matrix_merged"


#' Place-Name Crosswalk for the Colonial Census and Yearbook Tables
#'
#' One row for every place name printed in the tables returned by
#' \code{\link{load_colonial_census}}, with a canonical spelling, a canonical
#' contrôle civil (and caidat), and, where the match is unambiguous, a link to
#' the gazetteer \code{\link{historical_geonames}} (modern name, 2024 locality
#' id, coordinates). Join it to a table on the printed name and its context,
#' e.g. \code{locality} and \code{controle_civil}, or \code{cheikhat} and
#' \code{caidat}.
#'
#' @format A \code{data.frame} with 2,341 rows and 16 columns:
#' \describe{
#'   \item{level}{Column the name appears in: \code{"controle_civil"},
#'     \code{"annexe"}, \code{"caidat"}, \code{"commune"}, \code{"cheikhat"}
#'     or \code{"locality"}.}
#'   \item{name_printed}{The name exactly as stored in the tables.}
#'   \item{controle_civil_printed, caidat_printed}{The contrôle civil and
#'     caidat printed with it (context; \code{NA} if the table has none).}
#'   \item{name_std}{Canonical name: 1931 spellings for contrôles and caidats;
#'     for other places the printed name without qualifiers such as
#'     "(Ville)", "(Banlieue)" or "(partie rurale)".}
#'   \item{controle_civil_std, caidat_std}{Canonical contrôle civil and
#'     caidat. The southern military territories, printed as "Territoire(s) du
#'     Sud" or "Territoires militaires" and in 1931 by subdivision, are all
#'     \code{"Territoires militaires du Sud"}.}
#'   \item{note}{Composite or renamed units, 1906 annexes, subdivisions.}
#'   \item{match}{For communes, cheikhats and localities: \code{"exact"}
#'     (normalised names equal), \code{"qualifier_stripped"} (equal after
#'     dropping a printed qualifier), \code{"ambiguous"} (several gazetteer
#'     entries remain after narrowing by caidat or contrôle), \code{"conflict"}
#'     (one candidate, but the gazetteer places it in another contrôle civil;
#'     not linked), or \code{"none"}. \code{NA} for contrôles, annexes and
#'     caidats.}
#'   \item{n_candidates}{Number of gazetteer candidates for ambiguous and
#'     conflicting rows; 1 when linked; 0 otherwise.}
#'   \item{locality_id_2024, locality_name_modern, delegation_1956, lat,
#'     lon}{From \code{historical_geonames}, for linked rows.}
#'   \item{tables}{The tables the name appears in, separated by semicolons.}
#' }
#'
#' @details Names are compared after normalising accents, case, hyphens,
#'   apostrophes, Arabic articles and common transliteration variants
#'   (ou/u, dj/j, kh/k, ch/sh); no fuzzy matching is done. Of the 2,230
#'   commune, cheikhat and locality rows, 1,516 are linked (1,495 with
#'   coordinates). Links were checked against the gazetteer's own 1931
#'   contrôle civil, allowing for the 1906 annexes, the later contrôle of
#'   Zaghouan (carved out of Tunis) and the military territories.
#'
#' @source Built by \code{data-raw/colonial_census/place_crosswalk.py} from the
#'   tables in \code{inst/extdata/colonial} and
#'   \code{\link{historical_geonames}} (Ben Salah et al., 2024
#'   (\doi{10.1016/j.jce.2024.09.002})).
#'
#' @seealso \code{\link{load_colonial_census}}, \code{\link{historical_geonames}}
#'
#' @examples
#' data(colonial_place_crosswalk)
#' table(colonial_place_crosswalk$level, colonial_place_crosswalk$match,
#'       useNA = "ifany")
#'
#' # Map the 1931 cheikhats to coordinates
#' ch <- load_colonial_census("ind1931_t3_cheikhat_nationality")
#' xw <- subset(colonial_place_crosswalk, level == "cheikhat",
#'              c(name_printed, caidat_printed, lat, lon))
#' ch <- merge(ch, xw, by.x = c("cheikhat", "caidat"),
#'             by.y = c("name_printed", "caidat_printed"), all.x = TRUE)
#' mean(!is.na(ch$lat))
"colonial_place_crosswalk"
