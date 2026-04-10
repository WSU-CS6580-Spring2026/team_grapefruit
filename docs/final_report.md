# Birth Rate Forecasting and Policy Insights

---

## Executive Summary

All over the world, developed nations are experiencing a birth rate crisis that threatens to destablize and permanently alter their social and economic landscape. While nations such as South Korea, Japan and China have historically tended to receive the most press coverage, the situation is now beginning to be recognized as a serious problem in the United States as well.

This project analyzes U.S. census, presidential election, and natality data to identify socioeconomic and political factors that influence birth rates. Using historical data from 2010 and 2020, we have modeled how these variables affect birth rates over time and generated predictions for 2030. The results, available in a dynamic, interactive web model are intended to support data-informed decision-making for planning and policy development in both the public and private sector.

---

## Data

The data we required was readily available for free on public databases. Because our project focuses on the county level, the universal usage of the FIPS (Federal Information Processing Standards) code across these databases allowed us to easily join multiple databases together.
The only significant challenge we overcame was the limited availability of data in counties with smaller populations.
Ultimately we decided to focus solely on these larger counties, reasoning that accurate modeling and analysis on the largest counties would produce the most significant outcome overall.

---

## Models

Our baseline model predicts future birth rates based off the current average birth rate for all included counties. This is not a terrible model, because birth rates fall into a fairly narrow range, but it is not as efficient as it could be. The model resulted in an RMSE of 1.8811 and an MAE of 1.4564.

Our champion model groups counties into seven different socio-economic categories based off of racial demographics and political leanings. The model then utilizes each county's trajectory from 2010 to 2020 and predicts 2030 base rates using the mean birth rate of its socio-economic category during that same time period. This model resulted in a far-superior 0.7950 RMSE and an MAE of 0.6132.

---

## User Testing

Our interactive tool built around the champion model allows users to select a county and observe historical and predicted birth rates for that county, with options to determine how much data is presented.

Based off of numerous user testing sessions, we made four improvements that dramatically improved the usability of the tool:

  - Provided introductory, explanatory language to help the user understand the purpose and usage of the tool
  - Added a clear, color-coded key on the state map to ensure that the selected county was clearly marked and county birth rates in the state were identifiable
  - Allowed for pre-selection of a particular state to minimize search time for the desired county
  - Included a pre-selection for socio-economic category to allow users to more narrowly focus their search

---

## Recommendations and Future Work

Our project should lead all stakeholders to recognize that the birthrate crisis is already here in the United States and is only going to get worse. Given additional time, we would set up meetings with some local stakeholders to get their feedback about what we could do to enhance the tool. Additionally, we would consider what other possible factors might influence birth rate and examine additional models to see if we could improve on our existing one.






