## I only did forecast based on the lego dataset, historical data only
## but I am thinking to introduce some external dataset, GDP, kids amounts, lego annual report and such,
## then I can try to use regression model for the forecast
from prophet import Prophet
import pandas as pd
import matplotlib.pyplot as plt


def forecast_theme(df, theme, periods=5):
    """
    Build a simple yearly forecast for the number of sets
    for a given theme, using Prophet.
    df       : cleaned dataframe from prepare_data()
    theme    : the theme name to forecast
    periods  : how many future years to predict
    """
    df_temp = df.copy()

    theme_rows = df_temp[df_temp["theme"] == theme].copy()

    if theme_rows.empty:
        print(f"[forecast_theme] No data found for theme: {theme}")
        return None
    if "year" not in theme_rows.columns or "num_sets" not in theme_rows.columns:
        print("[forecast_theme] Required columns 'year' or 'num_sets' are missing.")
        return None

    df_model = theme_rows[["year", "num_sets"]].copy()

    df_model["ds"] = pd.to_datetime(df_model["year"], format="%Y")

    df_model["y"] = df_model["num_sets"]

    df_model_final = df_model[["ds", "y"]].copy()

    model = Prophet(
        yearly_seasonality=False,  
        weekly_seasonality=False,
        daily_seasonality=False
    )

    model.fit(df_model_final)

    future = model.make_future_dataframe(
        periods=periods,
        freq="Y"  
    )

    forecast = model.predict(future)

    fig = model.plot(forecast)
    plt.title(f"Forecast: Number of Sets for {theme}")
    plt.xlabel("Year")
    plt.ylabel("Number of Sets")
    plt.tight_layout()
    plt.show()

    return forecast

