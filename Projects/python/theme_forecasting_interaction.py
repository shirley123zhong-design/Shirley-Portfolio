import pandas as pd
from .theme_forecasting import forecast_theme

def run_forecast_interaction(df):
    """
    input a theme and how many years to forecast.
    Then call forecast_theme() and show the forecast chart.
    """

    df_temp = df.copy()

    unique_themes = df_temp["theme"].unique()
    themes_list = unique_themes.tolist()
    themes_list_sorted = sorted(themes_list)

    if len(themes_list_sorted) == 0:
        print("[run_forecast_interaction] No themes available in the data.")
        return

    print("\n===============")
    print("THEME FORECASTING")
    print("=================")
    print(f"Total number of themes: {len(themes_list_sorted)}")

    print("\nHere are some example themes you can try:")
    example_themes_to_show = 10
    print(", ".join(themes_list_sorted[:example_themes_to_show]))

    theme_input = input(
        "\nPlease type the exact theme name you want to forecast "
        "(or press Enter to use the first theme): "
    )
    selected_theme = theme_input.strip()

    if selected_theme == "":
        selected_theme = themes_list_sorted[0]
        print(f"\nNo theme entered. Using default theme: {selected_theme}")
    else:
        if selected_theme not in themes_list_sorted:
            print(f"\nTheme '{selected_theme}' not found in the data.")
            print(f"Using default theme instead: {themes_list_sorted[0]}")
            selected_theme = themes_list_sorted[0]

    periods_input = input(
        "\nHow many future years do you want to forecast? "
        "(press Enter for default = 5): "
    )
    periods_clean = periods_input.strip()

    if periods_clean == "":
        periods = 5
        print("\nNo value entered. Using default: 5 years.")
    else:
        if not periods_clean.isdigit():
            print("\nThat is not a valid number. Using default = 5 years.")
            periods = 5
        else:
            periods = int(periods_clean)
            if periods <= 0:
                print("\nNumber must be positive. Using default = 5 years.")
                periods = 5

    print(f"\nYou selected theme: {selected_theme}")
    print(f"Forecast horizon: {periods} years")


    forecast_df = forecast_theme(df_temp, selected_theme, periods=periods)

    if forecast_df is not None:
        print("\nLast 10 forecast rows (date and prediction):")
        if "ds" in forecast_df.columns and "yhat" in forecast_df.columns:
            preview = forecast_df[["ds", "yhat"]].tail(10)
            print(preview.to_string(index=False))
