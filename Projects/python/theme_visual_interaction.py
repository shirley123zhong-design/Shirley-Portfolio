import pandas as pd
from .theme_trends import (plot_theme_trend,plot_portfolio_share,plot_sets_per_theme_for_year,)


def show_theme_trend_charts(df):
    """
    input a theme and show:
    -Number of sets per year for that theme
    -Portfolio share per year for that theme
    """

    df_temp = df.copy()
    unique_themes_series = df_temp["theme"].unique()
    themes_list = unique_themes_series.tolist()

    themes_list_sorted = sorted(themes_list)

    print("\n========================")
    print("THEME TREND VISUALISATION")
    print("==========================")
    print(f"Total number of themes: {len(themes_list_sorted)}")

    print("\nHere are some example themes you can try:")
    example_themes_to_show = 10
    examples = themes_list_sorted[:example_themes_to_show]
    print(", ".join(examples))

    user_input = input(
        "\nPlease type the exact theme name you want to see "
        "(or press Enter to use the first theme in the list): "
    )

    selected_theme = user_input.strip()

    if selected_theme == "":
        selected_theme = themes_list_sorted[0]
        print(f"\nNo theme entered. Using default theme: {selected_theme}")
    else:
        if selected_theme not in themes_list_sorted:
            print(f"\nTheme '{selected_theme}' was not found in the data.")
            print(f"Using default theme instead: {themes_list_sorted[0]}")
            selected_theme = themes_list_sorted[0]

    print(f"\nYou selected theme: {selected_theme}")

    print("\nShowing chart: Number of sets per year...")
    plot_theme_trend(df_temp, selected_theme)

    print("\nShowing chart: Portfolio share per year...")
    plot_portfolio_share(df_temp, selected_theme)


def show_year_bar_chart(df):
    """
    input a year and show:
    A bar chart of number of sets per theme in that year.
    """

    df_temp = df.copy()

    years_series = df_temp["year"].dropna()
    years_as_int = years_series.astype(int)
    unique_years = years_as_int.unique()
    years_list = unique_years.tolist()

    years_list_sorted = sorted(years_list)

    if len(years_list_sorted) == 0:
        print("[show_year_bar_chart] No years available in the data.")
        return

    min_year = years_list_sorted[0]
    max_year = years_list_sorted[-1]

    print("\n===============================")
    print("BAR CHART: SETS PER THEME / YEAR")
    print("=================================")
    print(f"Years available in the data: {min_year} to {max_year}")

    user_input = input(
        f"\nPlease enter a year between {min_year} and {max_year} "
        f"(or press Enter to use {max_year}): "
    )

    cleaned_input = user_input.strip()

    if cleaned_input == "":
        selected_year = max_year
        print(f"\nNo year entered. Using default year: {selected_year}")
    else:
        if not cleaned_input.isdigit():
            print("\nThat is not a valid number. Using default year instead.")
            selected_year = max_year
        else:
            year_value = int(cleaned_input)

            if year_value < min_year or year_value > max_year:
                print("\nYear is outside the valid range. Using default year instead.")
                selected_year = max_year
            else:
                selected_year = year_value

    print(f"\nYou selected year: {selected_year}")
    print("Showing bar chart: number of sets per theme...")
    plot_sets_per_theme_for_year(df_temp, selected_year)
