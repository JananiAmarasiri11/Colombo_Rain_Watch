# Colombo Rain Watch

How well can yesterday’s weather predict tomorrow’s rainfall in Colombo? This project compares nine forecasting methods and uses a Streamlit dashboard to explore where their predictions succeed and where they miss heavy rain.

## Data and evaluation

I used 5,844 daily weather records for Colombo, Sri Lanka, from 1 January 2010 to 31 December 2025. The rainfall values are ERA5 historical estimates accessed through the [Open-Meteo Historical Weather API](https://open-meteo.com/en/docs/historical-weather-api).

The machine-learning models use earlier rainfall, the previous day’s temperature and wind speed, and the forecast month. The baseline uses yesterday’s rainfall. For example, a forecast for 28 November can use weather through 27 November.

I used 2010–2023 to train the base models, 2024 to compare them and train the stacking and hybrid models, and all 365 days of 2025 for final testing.

## Models and results

The nine methods were the previous-day rainfall baseline, Random Forest, Bagging Regressor, XGBoost, LightGBM, CatBoost, Ridge stacking, ARIMA, and an ARIMA + Random Forest hybrid. The stacking model learned how to combine five models’ forecasts. The hybrid used Random Forest to estimate a correction to the ARIMA forecast.

| 2025 test result | Finding |
| --- | --- |
| Previous-day baseline | Predicting the same rainfall as yesterday gave a mean absolute error (MAE) of 6.406 mm. |
| Lowest overall MAE | CatBoost achieved 5.955 mm across all 365 days. |
| Lowest MAE on the wettest days | ARIMA + Random Forest achieved 27.286 mm across the 38 days with at least 16.2 mm of rainfall. |

The model with the lowest average error still struggled with extreme rainfall. On 28 November 2025, the archive estimated **213.90 mm**. CatBoost predicted **35.18 mm**, while the hybrid predicted **59.82 mm**. The hybrid came closer but underestimated the rainfall by **154.08 mm**.

## Explore the dashboard

- **Overview** shows the rainfall timeline and monthly totals.
- **Model comparison** compares errors and training times across all nine methods.
- **Date explorer** lets you select a 2025 date and compare a saved forecast with archived rainfall.
- **Prediction lab** runs the saved CatBoost model using weather inputs you can adjust.

To reproduce the example above, open **Prediction lab**, select **28 November 2025**, keep the default inputs and click **Generate rainfall forecast**. The expected result is **35.18 mm**.

## Run locally

Download or clone the repository. Open a terminal in the folder containing `app.py` and run:

```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Open the local URL printed in the terminal. The dashboard loads the trained model from `colombo_catboost.cbm`. The training process, charts and evaluation are in `Colombo_Rain_Watch.ipynb`.

## AI use

Parts of the notebook code were generated with ChatGPT. Parts of the Streamlit dashboard code and interface were generated with ChatGPT and GitHub Copilot.