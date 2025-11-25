import streamlit as st
import pandas as pd
from .data_preparation import (
    get_available_years,
    get_year_slice,
    get_new_themes_for_year,
    rank_themes_by_sets_in_year,
)

def run_year_explorer(df):
    st.subheader("🔍 LEGO Year Explorer")

    years_list = get_available_years(df)
    min_year = min(years_list)
    max_year = max(years_list)

    selected_year = st.slider(
        "Select a year:",
        min_value=min_year,
        max_value=max_year,
        value=min_year,
        step=1
    )

    st.markdown(f"### 📅 Themes in {selected_year}")

    new_themes_df = get_new_themes_for_year(df, selected_year)
    st.write("**New themes launched this year:**")
    st.dataframe(new_themes_df if not new_themes_df.empty else pd.DataFrame({"info": ["No new themes this year"]}))

    ranked_df = rank_themes_by_sets_in_year(df, selected_year)
    st.write("**Themes ranked by number of sets:**")
    st.dataframe(ranked_df if not ranked_df.empty else pd.DataFrame({"info": ["No data for this year"]}))
