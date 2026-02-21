# Data Dictionary

******************************************

**df_A**: Dataframe for training and testing

*   Based on 2010 Census data for all files ending in _C
    *  _C: United States Census Bureau Annual County Resident Population Estimates by Age, Sex, Race, and Hispanic Origin: April 1, 2010 to July 1, 2019 (CC-EST2019-ALLDATA)
*   All others as specified
    *  _N: CDC WONDER Natality 2007-2024
    *  _P: Harvard Dataverse County Presidential Election Returns 2000-2024


| Column Name              | Data Type | Description                                                                                          |
|--------------------------|-----------|------------------------------------------------------------------------------------------------------|
| fips                     | object    | Federal Information Processing Standard (FIPS) code uniquely identifying a U.S. county               |
| TOT_POP_1519_C           | int64     | Total population count of individuals aged 15–19 in the county                                       |
| TOT_POP_2024_C           | int64     | Total population count of individuals aged 20–24 in the county                                       |
| TOT_POP_2529_C           | int64     | Total population count of individuals aged 25–29 in the county                                       |
| TOT_POP_3034_C           | int64     | Total population count of individuals aged 30–34 in the county                                       |
| TOT_POP_3539_C           | int64     | Total population count of individuals aged 35–39 in the county                                       |
| TOT_FEMALE_1519_C        | int64     | Total female population count aged 15–19 in the county                                               |
| TOT_FEMALE_2024_C        | int64     | Total female population count aged 20–24 in the county                                               |
| TOT_FEMALE_2529_C        | int64     | Total female population count aged 25–29 in the county                                               |
| TOT_FEMALE_3034_C        | int64     | Total female population count aged 30–34 in the county                                               |
| TOT_FEMALE_3539_C        | int64     | Total female population count aged 35–39 in the county                                               |
| WA_FEMALE_1519_C         | int64     | Female population count aged 15–19 identifying as White alone in the county                          |
| WA_FEMALE_2024_C         | int64     | Female population count aged 20–24 identifying as White alone in the county                          |
| WA_FEMALE_2529_C         | int64     | Female population count aged 25–29 identifying as White alone in the county                          |
| WA_FEMALE_3034_C         | int64     | Female population count aged 30–34 identifying as White alone in the county                          |
| WA_FEMALE_3539_C         | int64     | Female population count aged 35–39 identifying as White alone in the county                          |
| BA_FEMALE_1519_C         | int64     | Female population count aged 15–19 identifying as Black or African American alone                    |
| BA_FEMALE_2024_C         | int64     | Female population count aged 20–24 identifying as Black or African American alone                    |
| BA_FEMALE_2529_C         | int64     | Female population count aged 25–29 identifying as Black or African American alone                    |
| BA_FEMALE_3034_C         | int64     | Female population count aged 30–34 identifying as Black or African American alone                    |
| BA_FEMALE_3539_C         | int64     | Female population count aged 35–39 identifying as Black or African American alone                    |
| H_FEMALE_1519_C          | int64     | Female population count aged 15–19 identifying as Hispanic or Latino (any race)                      |
| H_FEMALE_2024_C          | int64     | Female population count aged 20–24 identifying as Hispanic or Latino (any race)                      |
| H_FEMALE_2529_C          | int64     | Female population count aged 25–29 identifying as Hispanic or Latino (any race)                      |
| H_FEMALE_3034_C          | int64     | Female population count aged 30–34 identifying as Hispanic or Latino (any race)                      |
| H_FEMALE_3539_C          | int64     | Female population count aged 35–39 identifying as Hispanic or Latino (any race)                      |
| NHWA_FEMALE_1519_C | int64 | Female population count aged 15–19 identifying as Non-Hispanic White alone in the county |
| NHWA_FEMALE_2024_C | int64 | Female population count aged 20–24 identifying as Non-Hispanic White alone in the county |
| NHWA_FEMALE_2529_C | int64 | Female population count aged 25–29 identifying as Non-Hispanic White alone in the county |
| NHWA_FEMALE_3034_C | int64 | Female population count aged 30–34 identifying as Non-Hispanic White alone in the county |
| NHWA_FEMALE_3539_C | int64 | Female population count aged 35–39 identifying as Non-Hispanic White alone in the county |
| NHBA_FEMALE_1519_C | int64 | Female population count aged 15–19 identifying as Non-Hispanic Black or African American alone in the county |
| NHBA_FEMALE_2024_C | int64 | Female population count aged 20–24 identifying as Non-Hispanic Black or African American alone in the county |
| NHBA_FEMALE_2529_C | int64 | Female population count aged 25–29 identifying as Non-Hispanic Black or African American alone in the county |
| NHBA_FEMALE_3034_C | int64 | Female population count aged 30–34 identifying as Non-Hispanic Black or African American alone in the county |
| NHBA_FEMALE_3539_C | int64 | Female population count aged 35–39 identifying as Non-Hispanic Black or African American alone in the county |
| dem2010_P                | float64   | Proportion of votes cast for the Democratic candidate in the 2008 / 2012 elections (averaged)        |
| birth_rate_2010_N        | float64   | Birth rate in the county for year 2010, expressed as births per population unit (births per 1000)                      |
| births_2010_N            | float64   | Total number of recorded births in the county during calendar year 2010                              |
| birth_rate_2020_N        | float64   | Birth rate in the county for year 2020, expressed as births per population unit (births per 1000)                      |
| births_2020_N            | float64   | Total number of recorded births in the county during calendar year 2020                              |

******************************************

**df_X**: Dataframe for training and testing, including engineered columns

*   Non _X columns identical to df_A
*   _X columns as engineered

| Column Name | Data Type | Description |
|-------------|-----------|-------------|
| fips | int64 | Federal Information Processing Standard (FIPS) code uniquely identifying a U.S. county |
| TOT_POP_1519_C | int64 | Total population count of individuals aged 15–19 in the county |
| TOT_POP_2024_C | int64 | Total population count of individuals aged 20–24 in the county |
| TOT_POP_2529_C | int64 | Total population count of individuals aged 25–29 in the county |
| TOT_POP_3034_C | int64 | Total population count of individuals aged 30–34 in the county |
| TOT_POP_3539_C | int64 | Total population count of individuals aged 35–39 in the county |
| TOT_FEMALE_1519_C        | int64     | Total female population count aged 15–19 in the county                                               |
| TOT_FEMALE_2024_C        | int64     | Total female population count aged 20–24 in the county                                               |
| TOT_FEMALE_2529_C        | int64     | Total female population count aged 25–29 in the county                                               |
| TOT_FEMALE_3034_C        | int64     | Total female population count aged 30–34 in the county                                               |
| TOT_FEMALE_3539_C        | int64     | Total female population count aged 35–39 in the county                                               |
| WA_FEMALE_1519_C         | int64     | Female population count aged 15–19 identifying as White alone in the county                          |
| WA_FEMALE_2024_C         | int64     | Female population count aged 20–24 identifying as White alone in the county                          |
| WA_FEMALE_2529_C         | int64     | Female population count aged 25–29 identifying as White alone in the county                          |
| WA_FEMALE_3034_C         | int64     | Female population count aged 30–34 identifying as White alone in the county                          |
| WA_FEMALE_3539_C         | int64     | Female population count aged 35–39 identifying as White alone in the county                          |
| BA_FEMALE_1519_C         | int64     | Female population count aged 15–19 identifying as Black or African American alone                    |
| BA_FEMALE_2024_C         | int64     | Female population count aged 20–24 identifying as Black or African American alone                    |
| BA_FEMALE_2529_C         | int64     | Female population count aged 25–29 identifying as Black or African American alone                    |
| BA_FEMALE_3034_C         | int64     | Female population count aged 30–34 identifying as Black or African American alone                    |
| BA_FEMALE_3539_C         | int64     | Female population count aged 35–39 identifying as Black or African American alone                    |
| H_FEMALE_1519_C          | int64     | Female population count aged 15–19 identifying as Hispanic or Latino (any race)                      |
| H_FEMALE_2024_C          | int64     | Female population count aged 20–24 identifying as Hispanic or Latino (any race)                      |
| H_FEMALE_2529_C          | int64     | Female population count aged 25–29 identifying as Hispanic or Latino (any race)                      |
| H_FEMALE_3034_C          | int64     | Female population count aged 30–34 identifying as Hispanic or Latino (any race)                      |
| H_FEMALE_3539_C          | int64     | Female population count aged 35–39 identifying as Hispanic or Latino (any race)                      |
| NHWA_FEMALE_1519_C | int64 | Female population count aged 15–19 identifying as Non-Hispanic White alone in the county |
| NHWA_FEMALE_2024_C | int64 | Female population count aged 20–24 identifying as Non-Hispanic White alone in the county |
| NHWA_FEMALE_2529_C | int64 | Female population count aged 25–29 identifying as Non-Hispanic White alone in the county |
| NHWA_FEMALE_3034_C | int64 | Female population count aged 30–34 identifying as Non-Hispanic White alone in the county |
| NHWA_FEMALE_3539_C | int64 | Female population count aged 35–39 identifying as Non-Hispanic White alone in the county |
| NHBA_FEMALE_1519_C | int64 | Female population count aged 15–19 identifying as Non-Hispanic Black or African American alone in the county |
| NHBA_FEMALE_2024_C | int64 | Female population count aged 20–24 identifying as Non-Hispanic Black or African American alone in the county |
| NHBA_FEMALE_2529_C | int64 | Female population count aged 25–29 identifying as Non-Hispanic Black or African American alone in the county |
| NHBA_FEMALE_3034_C | int64 | Female population count aged 30–34 identifying as Non-Hispanic Black or African American alone in the county |
| NHBA_FEMALE_3539_C | int64 | Female population count aged 35–39 identifying as Non-Hispanic Black or African American alone in the county |
| dem2010_P                | float64   | Proportion of votes cast for the Democratic candidate in the 2008 / 2012 elections (averaged)        |
| birth_rate_2010_N        | float64   | Birth rate in the county for year 2010, expressed as births per population unit (births per 1000)                      |
| births_2010_N            | float64   | Total number of recorded births in the county during calendar year 2010                              |
| birth_rate_2020_N        | float64   | Birth rate in the county for year 2020, expressed as births per population unit (births per 1000)                      |
| births_2020_N            | float64   | Total number of recorded births in the county during calendar year 2020                              |
| NHWA_FEMALE_2034_share_X | float64 | Share of females aged 20–34 identifying as Non-Hispanic White in the county; engineered demographic proportion used for majority classification |
| NHBA_FEMALE_2034_share_X | float64 | Share of females aged 20–34 identifying as Non-Hispanic Black in the county; engineered demographic proportion used for majority classification |
| H_FEMALE_2034_share_X | float64 | Share of females aged 20–34 identifying as Hispanic in the county; engineered demographic proportion used for majority classification |
| race_category_X | object | Engineered categorical variable classifying the county as White, Black, Hispanic, or Mixed based on 60% demographic majority thresholds |
| regime_X | object | Engineered categorical variable combining demographic majority classification and political grouping into a demographic-political regime |
| pol_group_X | object | Engineered categorical variable classifying counties as Democratic, Republican, or Competitive based on Democratic vote share thresholds |
| reg_Minority_majority_X | bool | One-hot encoded indicator for counties classified as Minority_majority regime |
| reg_Mixed_Competitive_X | bool | One-hot encoded indicator for counties classified as Mixed_Competitive regime |
| reg_Mixed_Democratic_X | bool | One-hot encoded indicator for counties classified as Mixed_Democratic regime |
| reg_Mixed_Republican_X | bool | One-hot encoded indicator for counties classified as Mixed_Republican regime |
| reg_White_Competitive_X | bool | One-hot encoded indicator for counties classified as White_Competitive regime |
| reg_White_Democratic_X | bool | One-hot encoded indicator for counties classified as White_Democratic regime |
| reg_White_Republican_X | bool | One-hot encoded indicator for counties classified as White_Republican regime |

******************************************

**df_B**: Dataframe for applying model and projecting results

*   Based on 2020 Census data for all files ending in _C
    *  _C: United States Census Bureau Annual County Resident Population Estimates by Age, Sex, Race, and Hispanic Origin: April 1, 2020 to July 1, 2024 (CC-EST2024-ALLDATA)
*   All others as specified
    *  _N: CDC WONDER Natality 2007-2024
    *  _P: Harvard Dataverse County Presidential Election Returns 2000-2024


| Column Name              | Data Type | Description                                                                                          |
|--------------------------|-----------|------------------------------------------------------------------------------------------------------|
| fips                     | object    | Federal Information Processing Standard (FIPS) code uniquely identifying a U.S. county               |
| TOT_POP_1519_C           | int64     | Total population count of individuals aged 15–19 in the county                                       |
| TOT_POP_2024_C           | int64     | Total population count of individuals aged 20–24 in the county                                       |
| TOT_POP_2529_C           | int64     | Total population count of individuals aged 25–29 in the county                                       |
| TOT_POP_3034_C           | int64     | Total population count of individuals aged 30–34 in the county                                       |
| TOT_POP_3539_C           | int64     | Total population count of individuals aged 35–39 in the county                                       |
| TOT_FEMALE_1519_C        | int64     | Total female population count aged 15–19 in the county                                               |
| TOT_FEMALE_2024_C        | int64     | Total female population count aged 20–24 in the county                                               |
| TOT_FEMALE_2529_C        | int64     | Total female population count aged 25–29 in the county                                               |
| TOT_FEMALE_3034_C        | int64     | Total female population count aged 30–34 in the county                                               |
| TOT_FEMALE_3539_C        | int64     | Total female population count aged 35–39 in the county                                               |
| WA_FEMALE_1519_C         | int64     | Female population count aged 15–19 identifying as White alone in the county                          |
| WA_FEMALE_2024_C         | int64     | Female population count aged 20–24 identifying as White alone in the county                          |
| WA_FEMALE_2529_C         | int64     | Female population count aged 25–29 identifying as White alone in the county                          |
| WA_FEMALE_3034_C         | int64     | Female population count aged 30–34 identifying as White alone in the county                          |
| WA_FEMALE_3539_C         | int64     | Female population count aged 35–39 identifying as White alone in the county                          |
| BA_FEMALE_1519_C         | int64     | Female population count aged 15–19 identifying as Black or African American alone                    |
| BA_FEMALE_2024_C         | int64     | Female population count aged 20–24 identifying as Black or African American alone                    |
| BA_FEMALE_2529_C         | int64     | Female population count aged 25–29 identifying as Black or African American alone                    |
| BA_FEMALE_3034_C         | int64     | Female population count aged 30–34 identifying as Black or African American alone                    |
| BA_FEMALE_3539_C         | int64     | Female population count aged 35–39 identifying as Black or African American alone                    |
| H_FEMALE_1519_C          | int64     | Female population count aged 15–19 identifying as Hispanic or Latino (any race)                      |
| H_FEMALE_2024_C          | int64     | Female population count aged 20–24 identifying as Hispanic or Latino (any race)                      |
| H_FEMALE_2529_C          | int64     | Female population count aged 25–29 identifying as Hispanic or Latino (any race)                      |
| H_FEMALE_3034_C          | int64     | Female population count aged 30–34 identifying as Hispanic or Latino (any race)                      |
| H_FEMALE_3539_C          | int64     | Female population count aged 35–39 identifying as Hispanic or Latino (any race)                      |
| NHWA_FEMALE_1519_C | int64 | Female population count aged 15–19 identifying as Non-Hispanic White alone in the county |
| NHWA_FEMALE_2024_C | int64 | Female population count aged 20–24 identifying as Non-Hispanic White alone in the county |
| NHWA_FEMALE_2529_C | int64 | Female population count aged 25–29 identifying as Non-Hispanic White alone in the county |
| NHWA_FEMALE_3034_C | int64 | Female population count aged 30–34 identifying as Non-Hispanic White alone in the county |
| NHWA_FEMALE_3539_C | int64 | Female population count aged 35–39 identifying as Non-Hispanic White alone in the county |
| NHBA_FEMALE_1519_C | int64 | Female population count aged 15–19 identifying as Non-Hispanic Black or African American alone in the county |
| NHBA_FEMALE_2024_C | int64 | Female population count aged 20–24 identifying as Non-Hispanic Black or African American alone in the county |
| NHBA_FEMALE_2529_C | int64 | Female population count aged 25–29 identifying as Non-Hispanic Black or African American alone in the county |
| NHBA_FEMALE_3034_C | int64 | Female population count aged 30–34 identifying as Non-Hispanic Black or African American alone in the county |
| NHBA_FEMALE_3539_C | int64 | Female population count aged 35–39 identifying as Non-Hispanic Black or African American alone in the county |
| dem2020_P                | float64   | Proportion of votes cast for the Democratic candidate in the 2020 election                           |
| birth_rate_2020_N        | float64   | Birth rate in the county for year 2020, expressed as births per population unit (births per 1000)                     |
| births_2020_N            | float64   | Total number of recorded births in the county during calendar year 2020                              |




