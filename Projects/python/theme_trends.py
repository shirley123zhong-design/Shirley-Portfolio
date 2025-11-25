import matplotlib.pyplot as plt
import pandas as pd


def plot_theme_trend(df, theme):
    """
    Plot the number of sets released per year for a given theme.
    Uses columns: 'theme', 'year', 'num_sets'.
    """
    df_temp = df.copy()

    theme_rows = df_temp[df_temp["theme"] == theme].copy()

    if theme_rows.empty:
        print(f"[plot_theme_trend] No data found for theme: {theme}")
        return

    theme_rows = theme_rows.sort_values(by="year", ascending=True)

    plt.figure(figsize=(10, 5))
    plt.plot(theme_rows["year"],theme_rows["num_sets"],marker="o")
    # marker="0", add dots

    plt.title(f"Number of Sets Released per Year – {theme}")
    plt.xlabel("Year")
    plt.ylabel("Number of Sets Released")

    plt.grid(True)
    plt.tight_layout()
    plt.show()


def plot_portfolio_share(df, theme):
    """
    (%) per year for a given theme.
    Uses columns: 'theme', 'year', 'pct_of_portfolio'.
    """

    df_temp = df.copy()

    theme_rows = df_temp[df_temp["theme"] == theme].copy()

    if theme_rows.empty:
        print(f"[plot_portfolio_share] No data found for theme: {theme}")
        return

    if "pct_of_portfolio" not in theme_rows.columns:
        print("[plot_portfolio_share] Column 'pct_of_portfolio' is missing.")
        return

    theme_rows = theme_rows.sort_values(by="year", ascending=True)

    plt.figure(figsize=(10, 5))
    plt.plot(theme_rows["year"],theme_rows["pct_of_portfolio"],marker="o")

    plt.title(f"Portfolio Share per Year – {theme}")
    plt.xlabel("Year")
    plt.ylabel("Portfolio Share (%)")

    plt.grid(True)
    plt.tight_layout()
    plt.show()


def plot_sets_per_theme_for_year(df, year):
    """
    a bar chart showing: how many sets each theme has
    in a given year.
    Uses columns: 'year', 'theme', 'num_sets'.
    """

    df_temp = df.copy()
    year_rows = df_temp[df_temp["year"] == year].copy()

    if year_rows.empty:
        print(f"[plot_sets_per_theme_for_year] No data found for year: {year}")
        return

    if "theme" not in year_rows.columns or "num_sets" not in year_rows.columns:
        print("[plot_sets_per_theme_for_year] Required columns are missing.")
        return

    year_rows_unique = year_rows[["theme", "num_sets"]].drop_duplicates(subset="theme")

    year_rows_sorted = year_rows_unique.sort_values(by="num_sets",ascending=False)

    plt.figure(figsize=(10, 5))
    plt.bar(year_rows_sorted["theme"],year_rows_sorted["num_sets"])

    plt.title(f"Number of Sets per Theme in {year}")
    plt.xlabel("Theme")
    plt.ylabel("Number of Sets")

    plt.xticks(rotation=45, ha="right")

    plt.tight_layout()
    plt.show()
