import pandas as pd

def prepare_data(raw_df: pd.DataFrame) -> pd.DataFrame:
    """
    remove duplicates
    standardize dtypes
    fill missing values where needed

    growth, portfolio %, new themes already calculated in SQL in dbo.vw_theme_year_stats.
    """
    df = raw_df.copy()
    df = _drop_duplicates(df)
    df = _coerce_dtypes(df)
    df = _fill_missing(df)
    return df


def _drop_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    before = len(df)
    df = df.drop_duplicates().copy()
    after = len(df)
    removed = before - after
    print(f"[data_preparation] Removed {removed} duplicate rows.")
    return df


def _coerce_dtypes(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardize column types
    """
    df = df.copy()

    # Integers
    for col in ["year", "num_sets", "prev_num_sets", "total_sets_year",
                "new_themes_launched"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").astype("Int64")

    # Floats
    for col in ["abs_change", "pct_change", "pct_of_portfolio"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Flags
    if "is_new_theme_year" in df.columns:
        df["is_new_theme_year"] = df["is_new_theme_year"].astype("Int64")

    # Strings
    if "theme" in df.columns:
        df["theme"] = df["theme"].astype(str)

    return df


def _fill_missing(df: pd.DataFrame) -> pd.DataFrame:
    """
    numeric metrics → 0
    text → 'Unknown' if missing/empty
    """
    df = df.copy()

    numeric_cols = []
    for col in [
        "num_sets",
        "prev_num_sets",
        "abs_change",
        "pct_change",
        "total_sets_year",
        "pct_of_portfolio",
        "new_themes_launched",
    ]:
        if col in df.columns:
            numeric_cols.append(col)

    for col in numeric_cols:
        df[col] = df[col].fillna(0)

    if "theme" in df.columns:
        df["theme"] = df["theme"].replace("", pd.NA)
        df["theme"] = df["theme"].fillna("Unknown")

    return df

def get_available_years(df):
    """Return sorted list of years."""
    df_temp = df.copy()
    df_temp["year"] = df_temp["year"].astype(int)
    unique_years = df_temp["year"].unique()
    unique_years_list = unique_years.tolist()
    unique_years_list_sorted = sorted(unique_years_list)
    return unique_years_list_sorted

def get_year_slice(df: pd.DataFrame, year: int) -> pd.DataFrame:
    """Filter dataframe for a given year."""
    matching_rows = []
    for index, row in df.iterrows():
            matching_rows.append(row)
    df_result = pd.DataFrame(matching_rows)
    return df_result



def get_new_themes_for_year(df, year):
    """
    Return a table of themes that were launched in the given year.
    """
    df_year = df[df["year"] == year].copy()

    if "is_new_theme_year" not in df_year.columns:
        return pd.DataFrame()

    df_new_themes = df_year[df_year["is_new_theme_year"] == 1].copy()
    columns_to_keep = []
    if "theme" in df_new_themes.columns:
        columns_to_keep.append("theme")
    if "num_sets" in df_new_themes.columns:
        columns_to_keep.append("num_sets")
    if "pct_of_portfolio" in df_new_themes.columns:
        columns_to_keep.append("pct_of_portfolio")
    df_selected = df_new_themes[columns_to_keep].copy()
    df_unique = df_selected.drop_duplicates(subset="theme").copy()
    df_sorted = df_unique.sort_values(by="theme", ascending=True).copy()
    df_final = df_sorted.reset_index(drop=True)
    return df_final


def rank_themes_by_sets_in_year(df: pd.DataFrame, year: int):
    """Rank themes by number of sets in a given year."""
    df_year = df[df["year"] == year].copy()

    columns_to_keep = []
    if "theme" in df_year.columns:
        columns_to_keep.append("theme")
    if "num_sets" in df_year.columns:
        columns_to_keep.append("num_sets")
    if "pct_of_portfolio" in df_year.columns:
        columns_to_keep.append("pct_of_portfolio")

    df_selected = df_year[columns_to_keep].copy()
    df_unique = df_selected.drop_duplicates(subset="theme").copy()
    df_sorted = df_unique.sort_values(
        by="num_sets",
        ascending=False
    ).copy()

    df_final = df_sorted.reset_index(drop=True)

    return df_final

# ============================================================
# Run this file directly to export a clean CSV for Power BI
# ============================================================
if __name__ == "__main__":
    from .data_loader import load_theme_year_stats

    print("Loading raw data...")
    df = load_theme_year_stats()

    print("Cleaning data...")
    df_clean = prepare_data(df)

    print("Exporting CSV...")
    df_clean.to_csv("lego_theme_year_stats_clean.csv", index=False)

    print("Done! CSV saved as lego_theme_year_stats_clean.csv")
