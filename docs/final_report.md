# Birth Rate Forecasting and Policy Insights

---

## Executive Summary

All over the world, developed nations are experiencing a birth rate crisis that threatens to destabilize and permanently alter their social and economic landscape. While nations such as South Korea, Japan and China have historically tended to receive the most press coverage, the situation is now beginning to be recognized as a serious problem in the United States as well.

This project analyzes U.S. census, presidential election, and natality data to identify socioeconomic and political factors that influence birth rates. Using historical data from 2010 and 2020, we have modeled how these variables affect birth rates over time and generated predictions for 2030. The results, available in a dynamic, interactive web model are intended to support data-informed decision-making for planning and policy development in both the public and private sector.

---

## Data

The data we required was readily available from public databases, including U.S. Census data, CDC natality data, and county-level presidential election results. Because our project focuses on the county level, the universal usage of the FIPS (Federal Information Processing Standards) code across these databases allowed us to join multiple datasets together efficiently.

The only significant challenge we overcame was the limited availability of data in counties with smaller populations. Ultimately we decided to focus solely on the larger counties, reasoning that accurate modeling and analysis on the more complete and stable data from these counties would produce the most significant outcome overall.

A key feature engineering step involved grouping counties into socio-political “regimes” based on demographic composition and political leanings. This allowed us to capture structural differences between counties that significantly improved the performance of our predictive model.

---

## Models

Our baseline model predicts future birth rates using the overall average birth rate across all counties. While this approach performs reasonably well due to the relatively narrow distribution of birth rates, it does not account for meaningful differences between counties. The baseline model resulted in an RMSE of 1.8811 and an MAE of 1.4564.

Our champion model incorporates both historical trends and structural differences between counties. By grouping counties into seven socio-political categories and modeling the relationship between 2010 and 2020 birth rates within these groups, the model is able to generate more precise 2030 predictions.

This approach resulted in a significantly improved RMSE of 0.7950 and an MAE of 0.6132, representing a substantial reduction in prediction error compared to the baseline model.

---

## User Testing

Our interactive tool built around the champion model allows users to select a county and observe historical and predicted birth rates for that county, with options to determine how much data is presented.

Based on numerous user testing sessions, we made four improvements that dramatically improved the usability of the tool and reduced the time required for users to locate and interpret relevant county data:

  - Provided introductory, explanatory language to help the user understand the purpose and usage of the tool
  - Added a clear, color-coded key on the state map to ensure that the selected county was clearly marked and county birth rates in the state were identifiable
  - Allowed for pre-selection of a particular state to minimize search time for the desired county
  - Included a pre-selection for socio-economic category to allow users to more narrowly focus their search

---

## Recommendations and Future Work

Our findings suggest that birth rate trends are not uniform across counties, but instead vary systematically based on demographic and socio-political characteristics. Stakeholders should prioritize targeted, region-specific policies rather than broad national approaches, focusing on areas where declining birth rates are most pronounced.

Given additional time, we would expand the model to incorporate additional variables such as economic indicators, housing costs, and healthcare access, which may further improve predictive accuracy. We would also seek direct feedback from policymakers and community stakeholders to refine the tool and better align it with real-world decision-making needs.




