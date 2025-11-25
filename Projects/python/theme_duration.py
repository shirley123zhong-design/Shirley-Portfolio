import pandas as pd

def find_longest_running_themes(df, top_n=10):

    df_temp = df.copy()

    theme_years = (
        df_temp.groupby("theme")["year"]
        .agg(first_year="min", last_year="max")
        .reset_index()
    )

    theme_years["duration_years"] = (
        theme_years["last_year"] - theme_years["first_year"] + 1
    )

    theme_years_sorted = theme_years.sort_values(
        by="duration_years", ascending=False
    )

    # Print summary
    print("\n==============================")
    print("LONGEST RUNNING LEGO THEMES")
    print("==============================")
    print(f"Top {top_n} themes by duration:\n")
    print(theme_years_sorted.head(top_n).to_string(index=False))

    return theme_years_sorted
