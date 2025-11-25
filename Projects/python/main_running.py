import pandas as pd
from .data_loader import load_theme_year_stats
from .data_preparation import prepare_data
from .year_explorer_cool_function import run_year_explorer
from .theme_visual_interaction import show_theme_trend_charts, show_year_bar_chart
from .theme_forecasting_interaction import run_forecast_interaction
from .theme_duration_interaction import run_theme_duration_interaction



def main():
    """
    Load data from SQL view
    Clean and prepare the data
    Show visualisations for themes and years
    Start the year explorer interaction
    """

    df = load_theme_year_stats()
    print("Loaded data successfully! Preview:")
    print(df.head())

    df_clean = prepare_data(df)
    print(f"Rows after cleaning: {len(df_clean)}")
    print("Columns:", df_clean.columns.tolist())

    show_theme_trend_charts(df_clean)
    show_year_bar_chart(df_clean)
    run_forecast_interaction(df_clean)
    run_year_explorer(df_clean)
    run_theme_duration_interaction(df_clean)


if __name__ == "__main__":
    main()

