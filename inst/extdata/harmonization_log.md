# Census Harmonization Log: RGPH 2014 × RGPH 2024

## 1. Source Files

| File | Census | Level | Rows | Columns |
|------|--------|-------|------|---------|
| `RGPH_2014_merged_FINAL.csv` | 2014 | Delegation | 264 | 169 |
| `delegations.csv` | 2024 | Delegation | 279 | 959 |
| `gouvernorats.csv` | 2024 | Governorate | 24 | 1,059 |
| `secteurs.csv` | 2024 | Sector | 5,544 | 430 |
| `national.csv` | 2024 | National | 1 | 1,069 |

**How the 2024 census year was identified**: The `date_construction` variable includes the bin `2015_2024`, which could not exist in a 2014 instrument. The 2014 file self-identifies via its filename and matches the 2014 analysis (.tex file) exactly.

---

## 2. Unit of Analysis

Harmonization was performed at the **delegation level**, which is the finest administrative unit available in both censuses. The 2024 data also provides sector-level (sub-delegation) data (5,544 sectors), but this granularity does not exist in the 2014 merged file.

---

## 3. Geographic Crosswalk

### 3.1 Governorate matching

24 governorates exist in both censuses. Two required name normalization:

| 2014 name | 2024 name | Resolution |
|-----------|-----------|------------|
| ELKEF | Le kef | Case + spelling variant |
| MANNOUBA | Manouba | Spelling variant (double-n vs single-n) |

### 3.2 Delegation matching

**Matching procedure**: Three-pass approach.

1. **Exact match after normalization** (lowercase, strip accents, remove hyphens/punctuation, collapse whitespace): 193 matches.
2. **Fuzzy match within same governorate** (Python `difflib.get_close_matches`, cutoff=0.70): 70 additional matches.
3. **Manual residual check**: 1 delegation unresolvable by algorithm.

**Result**: 263 of 264 delegations matched (99.6%).

### 3.3 Unmatched delegation (2014)

| Delegation | Governorate | Reason |
|------------|-------------|--------|
| Ezzouhour | KASSERINE | Split into two in 2024: `Ezzouhour-kasserine` (Kasserine) and `Ezzouhour-tunis` (Tunis). The 2014 Ezzouhour was a Kasserine delegation; the fuzzy matcher could not resolve the disambiguation suffix. Could be manually assigned to `Ezzouhour-kasserine`. |

### 3.4 New delegations in 2024 (17)

These delegations exist in 2024 but have no 2014 counterpart. They represent administrative boundary changes (splits, reclassifications, or new creations) between the two censuses.

| Delegation | Governorate | Likely origin |
|------------|-------------|---------------|
| Ain Jeloula | Kairouan | New or split |
| Beni Mhira | Tataouine | New or split |
| Chebba | Mahdia | May have been part of another delegation in 2014 |
| Dkhilet Toujen | Gabès | New or split from El Hamma |
| El Bradaa | Mahdia | New or split |
| El Hamma Ouest | Gabès | Split from El Hamma |
| El Hichria | Sidi Bouzid | New or split |
| Essaida | Sidi Bouzid | New or split |
| Etouiref | Le Kef | New or split |
| Hammat Ejrid | Tozeur | New or split |
| Menzel M'hiri | Kairouan | New or split |
| Ouedhref | Gabès | New or split |
| Rejiche | Mahdia | New or split |
| Rjim Maatoug | Kébili | New or split |
| Sidi Boubaker | Gafsa | New or split |
| Zanouche | Gafsa | New or split |
| Ezzouhour-tunis | Tunis | Split from Ezzouhour (Kasserine ambiguity) |

**Decision**: These 17 delegations are included in the output with 2024 values only and `matched=False`. No imputation of 2014 values was attempted.

### 3.5 Notable fuzzy matches

Some delegation name differences between censuses were substantive enough to require fuzzy matching. Examples:

| 2014 name | 2024 name | Issue |
|-----------|-----------|-------|
| Benbla | Bembla | Typo in 2014 |
| Kairaouan Nord | Kairouan nord | Typo + case |
| Djbel Djloud | Djebel djelloud | Vowel omission |
| Mdjez Elbeb | Medjez el bab | Vowel omission |
| Werdanine | El Ouerdanine | Added prefix |
| Cité Ettathamen | Cite ettadhamen | Transliteration variant |
| Kalaât Khesba | Kalaat khasbah | Transliteration variant |
| La Nouvelle matmata | Nouvelle matmata | Dropped article |
| Sayada- Lamta- Bouhjar | Sayada-lamta bou-hja | Spacing + truncation |
| Zaouia Ksiba Thrayet | Zaouia - ksiba - thr | Truncation in 2024 |

---

## 4. Variable Harmonization

### 4.1 Scale difference

**Critical finding**: The 2014 dataset stores all percentages on a 0–100 scale (e.g., unemployment = 16.31). The 2024 dataset stores them as proportions on a 0–1 scale (e.g., unemployment = 0.1965).

**Decision**: All 2024 proportion values were multiplied by 100 to match the 2014 convention. The migration balance variable (`solde_migratoire`) was left unscaled as it represents a raw count difference, not a percentage.

### 4.2 Variable naming conventions

| Census | Convention | Example |
|--------|-----------|---------|
| 2014 | English-style flat names | `pct_taux_chomage` |
| 2024 | French hierarchical dot-notation with urban/rural/total breakdowns | `emploi.taux_chomage.Total` |

**Decision**: Created harmonized English variable names (e.g., `unemployment_rate`) with `_2014` and `_2024` suffixes. The original variable names from each census are documented in the crosswalk.

### 4.3 Urban/rural disaggregation

The 2024 census provides urban/rural/total breakdowns for nearly every variable. The 2014 merged file contains only the total. **Decision**: Only `total` values were extracted from 2024 to ensure comparability. The urban/rural detail in 2024 is available in the raw file for future analysis.

### 4.4 Harmonized variable mapping (45 variables)

#### Marital Status (4 variables)

| Harmonized name | 2014 column | 2024 column | Notes |
|----------------|-------------|-------------|-------|
| pct_never_married | pct_celibataire | etat_matrimonial.total.Total.Célibataire | Comparable |
| pct_married | pct_marie | etat_matrimonial.total.Total.Marié(e) | Comparable |
| pct_widowed | pct_veuf | etat_matrimonial.total.Total.Veuf(ve) | Comparable |
| pct_divorced | pct_divorce | etat_matrimonial.total.Total.Divorcé(e) | Comparable |

#### Education Level (4 variables)

| Harmonized name | 2014 column | 2024 column | Notes |
|----------------|-------------|-------------|-------|
| pct_no_education | pct_neant_educ | niveau_instruction.total.Total.Néant.Total | Population 10+; comparable |
| pct_primary_ed | pct_primaire_educ | niveau_instruction.total.Total.Primaire.Total | Comparable |
| pct_secondary_ed | pct_secondaire_educ | niveau_instruction.total.Total.Secondaire.Total | Comparable |
| pct_higher_ed | pct_superieur_educ | niveau_instruction.total.Total.Supérieur.Total | Comparable |

#### Literacy & Schooling (2 variables)

| Harmonized name | 2014 column | 2024 column | Notes |
|----------------|-------------|-------------|-------|
| pct_illiterate_10plus | pct_analphabete_10plus | analphabetisme.all.Total.Total.Total | Comparable (pop 10+) |
| pct_enrollment_6_14 | pct_scolarisation_6_14 | scolarisation_6_14.total.Total | Same age bracket |

#### Employment (3 variables)

| Harmonized name | 2014 column | 2024 column | Notes |
|----------------|-------------|-------------|-------|
| unemployment_rate | pct_taux_chomage | emploi.taux_chomage.Total | ILO definition both years |
| employment_rate | pct_taux_emploi | emploi.taux_emploi.Total | Comparable |
| participation_rate | pct_taux_activite | emploi.taux_participation.Total | Comparable |

#### Infrastructure (4 variables)

| Harmonized name | 2014 column | 2024 column | Notes |
|----------------|-------------|-------------|-------|
| pct_sonede_water | pct_eau_potable_sonede | raccordement.total.SONEDE | Both = % connected to SONEDE network |
| pct_steg_electricity | pct_electricite_steg | raccordement.total.STEG | Both = % connected to STEG grid |
| pct_natural_gas | pct_gaz_naturel_log | raccordement.total.Gaz naturel | Comparable |
| pct_onas_sanitation | pct_assainissement | eaux_usees.total.ONAS | Both = % connected to ONAS sewerage |

#### Housing Type (4 variables)

| Harmonized name | 2014 column | 2024 column | Notes |
|----------------|-------------|-------------|-------|
| pct_villa | pct_villa_duplex | type_logement.total.villa ou étage de villa | Comparable |
| pct_apartment | pct_appartement | type_logement.total.appartement | Comparable |
| pct_dar_arbi | pct_dar_arbi | type_logement.total.dar arbi | Comparable |
| pct_rudimentary_housing | pct_rudimentaire | type_logement.total.logement rudimentaire | Comparable |

#### Housing Tenure (2 variables)

| Harmonized name | 2014 column | 2024 column | Notes |
|----------------|-------------|-------------|-------|
| pct_homeowner | pct_proprietaire | occupation_menage.total.propriétaire | Comparable |
| pct_renter | pct_locataire | occupation_menage.total.locataire | Comparable |

#### Household Equipment (5 variables)

| Harmonized name | 2014 column | 2024 column | Notes |
|----------------|-------------|-------------|-------|
| pct_car | pct_voiture | biens_equipement.total.Voiture | Comparable |
| pct_fridge | pct_refrigerateur | biens_equipement.total.Frigidaire | Comparable |
| pct_washing_machine | pct_machine_laver | biens_equipement.total.Machine à laver | Comparable |
| pct_ac | pct_climatiseur | biens_equipement.total.Climatiseur local ou central | Comparable |
| pct_radio | pct_radio | biens_equipement.total.Radio | Comparable |

#### ICT Access (4 variables)

| Harmonized name | 2014 column | 2024 column | Notes |
|----------------|-------------|-------------|-------|
| pct_internet_hh | pct_internet_menage | acces_tic.total.Accès Internet | **2024 MISSING at delegation level** |
| pct_computer | pct_ordinateur | acces_tic.total.Ordinateur | **2024 MISSING at delegation level** |
| pct_mobile | pct_tel_portable | acces_tic.total.Téléphone Portable | **2024 MISSING at delegation level** |
| pct_landline | pct_tel_fixe | acces_tic.total.Téléphone Fixe | **2024 MISSING at delegation level** |

**Warning**: ICT variables exist in the 2024 gouvernorat-level file but NOT in the delegation-level file. All 2024 values for these 4 variables are NaN. If needed, governorate-level values could be imputed downward, but this was not done.

#### Housing Size (5 variables)

| Harmonized name | 2014 column | 2024 column | Notes |
|----------------|-------------|-------------|-------|
| pct_under_50m2 | pct_moins_50m2 | superficie.total.moins 50m2 | Comparable |
| pct_50_99m2 | pct_50_99m2 | superficie.total.50_99m2 | Comparable |
| pct_100_149m2 | pct_100_149m2 | superficie.total.100_149m2 | Comparable |
| pct_150_199m2 | pct_150_199m2 | superficie.total.150_199m2 | Comparable |
| pct_200m2_plus | pct_plus_200m2 | superficie.total.200m2 et plus | Comparable |

#### Room Count (5 variables)

| Harmonized name | 2014 column | 2024 column | Notes |
|----------------|-------------|-------------|-------|
| pct_1_room | pct_1piece | pieces_logement.total.une piéce | Comparable |
| pct_2_rooms | pct_2pieces | pieces_logement.total.deux piéces | Comparable |
| pct_3_rooms | pct_3pieces | pieces_logement.total.trois piéces | Comparable |
| pct_4_rooms | pct_4pieces | pieces_logement.total.quatre piéces | Comparable |
| pct_5_rooms_plus | pct_5pieces_plus | pieces_logement.total.cinq piéces et plus | Comparable |

#### Housing Occupancy (2 variables)

| Harmonized name | 2014 column | 2024 column | Notes |
|----------------|-------------|-------------|-------|
| pct_occupied_housing | pct_occupe | occupation_logement.total.logements occupés | Comparable |
| pct_vacant_housing | pct_vacant | occupation_logement.total.logements vacants | Comparable |

#### Migration (1 variable)

| Harmonized name | 2014 column | 2024 column | Notes |
|----------------|-------------|-------------|-------|
| internal_migration_balance | solde_migratoire | migration_interne.solde_migratoire | Raw count; NOT rescaled. 2014 `solde_migratoire` may combine internal+external; 2024 separates them. Use with caution. |

---

## 5. Variables NOT Harmonized

### 5.1 In 2014 but absent from 2024 delegation file

| Domain | 2014 variables | Reason |
|--------|---------------|--------|
| Sector of employment | pct_agriculture, pct_industrie, pct_commerce, pct_batiment, pct_transport, pct_educ_sante_admin, pct_mines_energie, pct_autres_services | Not collected at delegation level in 2024 |
| Unemployment by education | pct_chom_neant, pct_chom_primaire, pct_chom_secondaire, pct_chom_superieur | Not available |
| Unemployment by age | pct_chom_15_19 through pct_chom_60plus | Not available |
| Graduate unemployment | taux_chomage_diplomes_sup | Not available |
| Distance to facilities | pct_ecole_plus2km, pct_hopital_plus2km, pct_dispensaire_plus2km, etc. | Not in 2024 delegation file |
| Higher ed enrollment | pct_scol_superieur_19_24 | Not available |
| Youth illiteracy | pct_analph_jeunes_15_29 | Not directly available (would need age-specific extraction) |
| Internet usage (individual) | pct_internet_10plus | Not at delegation level |
| Migration motives | pct_mig_emploi, pct_mig_logement, pct_mig_mariage, etc. | Not available |
| International migration | mig_inter_V2 through V11 | Structure changed |
| Population counts | pop_15plus, population, pop_10plus_educ, etc. | Not in 2024 delegation file as raw counts |

### 5.2 In 2024 but absent from 2014

| Domain | 2024 variables | Notes |
|--------|---------------|-------|
| Disability (WG measures) | handicap.*, difficulte.* | New module |
| Disability cards | carte_handicap.* | New module |
| Health coverage type | couverture_sanitaire_type.* (CNAM, AMG1, AMG2) | New breakdown |
| Elderly detail | personnes_agees.* | Detailed elderly module |
| Construction date | date_construction.* | New |
| Energy sources | energie_chauffage.*, energie_cuisson.*, energie_chauffage_eau.* | New breakdown |
| Waste management | dechets_menagers.* | New |
| Toilet type | toilette_logement.*, toilette_sache.* | New detail |
| Bathroom type | salle_de_bain.* | New |
| Water distance | distance_eau_potable.* | New |
| Drinking water source | eau_boisson.* | New |
| Water source type | eau_potable.* (6 categories) | More detailed than 2014 |
| Property acquisition mode | propriete_logement.* | New |
| Wastewater disposal | eaux_usees.* (4 categories) | More detailed |
| Children's health coverage | couverture_sanitaire_enfants.* | New |
| Smart TV | acces_tic.*.Smart TV | New item |
| Gender-disaggregated employment | emploi.taux_*.Masculin/Feminin | Available in 2024 only |

---

## 6. Known Limitations & Caveats

1. **Cross-sectional comparison, not panel**: These are two independent census cross-sections. Changes at the delegation level could reflect genuine socioeconomic shifts, boundary changes, or measurement differences.

2. **Boundary changes**: 17 new delegations in 2024 suggest administrative redistricting. Some 2014 delegations may have lost territory to new ones, making direct comparison imprecise even for matched units.

3. **ICT gap**: The 4 ICT variables (internet, computer, mobile, landline) are empty for 2024 at the delegation level. They are available at the governorate level in `gouvernorats.csv` and could be imputed if needed.

4. **Migration variable**: The 2014 `solde_migratoire` may conflate internal and external migration. The 2024 data cleanly separates `migration_interne` and `migration_externe`. Only `migration_interne.solde_migratoire` was mapped.

5. **Employment sector data**: The 2014 analysis relies heavily on agricultural employment share (`pct_agriculture`). This variable does not exist at the delegation level in the 2024 data, so the quasi-experimental findings from the Beamer presentation (Finding 2: Agriculture → Unemployment) cannot be replicated with 2024 data as delivered.

6. **Population denominators**: The 2014 file includes raw population counts (population, pop_15plus, etc.). The 2024 delegation file appears to contain only percentages/proportions, not counts. This limits the ability to compute population-weighted aggregations from 2024.

7. **Percentage base differences**: Some 2014 variables are computed over specific subpopulations (e.g., `pct_analphabete_10plus` = illiteracy among population 10+; `pct_celibataire` = among population 15+). The 2024 equivalents should use the same bases per INS methodology, but this could not be independently verified from the data alone.

---

## 7. Output Files

| File | Description | Rows | Columns |
|------|-------------|------|---------|
| `harmonized_census_2014_2024.csv` | Wide panel: one row per delegation, `_2014`/`_2024`/`_change` columns | 281 | 144 |
| `delegation_crosswalk_2014_2024.csv` | Name mapping between censuses | 263 | 5 |

### Column structure of harmonized file

- **Identifiers** (9 cols): governorate, delegation names (both years, Arabic), region, lat, lon, matched flag
- **Per variable** (3 cols each × 45 vars = 135 cols): `{variable}_2014`, `{variable}_2024`, `{variable}_change`
- Change = 2024 value − 2014 value (in percentage points)
