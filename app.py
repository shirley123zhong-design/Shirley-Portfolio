import streamlit as st

# ========= IMPORT YOUR EXISTING LEGO MODULES =========
from Projects.python.data_loader import load_theme_year_stats
from Projects.python.data_preparation import prepare_data
from Projects.python.year_explorer_cool_function import run_year_explorer
from Projects.python.theme_visual_interaction import (
    show_theme_trend_charts,
    show_year_bar_chart,
)
from Projects.python.theme_forecasting_interaction import run_forecast_interaction
from Projects.python.theme_duration_interaction import run_theme_duration_interaction

# ========= PAGE CONFIG =========
st.set_page_config(
    page_title="Shirley Zhong - Data Portfolio",
    page_icon="📊",
    layout="wide",
)

# ========= SIDEBAR (PROFILE + NAV) =========
with st.sidebar:
    st.title("📇 About Me")
    st.write(
        """
        Hi, I’m **Shirley (Ruyi Zhong)**.

        I work with **Python, SQL, and Power BI** to turn data into clear,
        business-oriented insights. This portfolio focuses on analysing
        LEGO’s historical product themes.
        """
    )

    st.write("📍 Based in Denmark")
    st.write("📧 Email: shirley123zhong@gmail.com")
    st.write("[🔗 LinkedIn](https://linkedin.com/in/ruyi-zhong-a2252a194)")

    st.markdown("---")
    st.caption("This portfolio is built with Streamlit in Python.")

    st.markdown("---")
    st.subheader("📂 Navigate")
    page = st.radio(
        "Go to:",
        ["🏠 Overview", "🐍 Python Projects", "🗄 SQL Projects", "📊 Power BI Dashboards"],
        label_visibility="collapsed",
    )

# ========= HELPER: LOAD & PREP DATA ONCE =========
@st.cache_data(show_spinner="Loading LEGO theme-year data…")
def load_clean_lego_data():
    # Uses your existing pipeline from main_running.py
    df = load_theme_year_stats()
    df_clean = prepare_data(df)
    df = load_theme_year_stats()
    df_clean.to_csv("lego_theme_year_stats_clean.csv", index=False)
    return df_clean


# ========= PAGES =========
def show_overview():
    st.title("📊 Data Portfolio – LEGO Theme Analytics")

    st.write(
        """
        Welcome! This portfolio showcases an end-to-end **LEGO theme analytics**
        project using **SQL**, **Python**, and **Power BI**.

        I use the official LEGO dataset (sets + themes) to analyse:

        - How many sets are released per theme and year  
        - Which themes are growing, declining, or stable  
        - When new themes are introduced  
        - How much each theme contributes to LEGO’s yearly portfolio  
        - How long themes survive in the product line  
        - Simple forecasting of future set releases
        """
    )

    st.markdown("---")

    # ----- SKILLS -----
    st.header("🛠 Skills")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("🐍 Python")
        st.write(
            """
            - Data cleaning & wrangling (`pandas`) on LEGO datasets  
            - Exploratory data analysis and feature creation  
            - Visualisations (`matplotlib`) – time series & rankings  
            - Time-series forecasting with **Prophet**  
            - Small interactive console tools for analysis
            """
        )

    with col2:
        st.subheader("🗄 SQL")
        st.write(
            """
            - Joins, aggregations, subqueries, CTEs  
            - Window functions (`LAG`) for year-on-year growth  
            - Building analytical views for reporting  
            - Turning raw LEGO tables into a clean view:
              `vw_theme_year_stats`
            """
        )

    with col3:
        st.subheader("📈 Power BI")
        st.write(
            """
            - Data modelling & relationships  
            - Basic–intermediate DAX measures  
            - Interactive dashboards with slicers & filters  
            - Connecting Power BI to SQL Server views
            """
        )

    st.markdown("---")

    # ----- PROJECT OVERVIEW -----
    st.header("📂 Project Overview")

    st.write(
        """
        All current projects in this portfolio are built around the same
        LEGO dataset, but from different angles:

        - 🧱 **LEGO Theme Analytics (SQL + Python)**  
          End-to-end analysis of LEGO themes over time: growth, portfolio
          share, new theme launches, and longest-running themes.

        - 🗄 **SQL Theme Trend Analysis**  
          A collection of analytical SQL queries and one final view
          (`vw_theme_year_stats`) that summarises theme performance
          per year and powers the Python & Power BI layers.

        - 📊 **Power BI Dashboards** *(planned)*  
          Dashboards using the same LEGO view to present trends and
          portfolio composition visually.
        """
    )

    st.caption("Use the left-hand menu to explore Python, SQL, and Power BI sections.")


def show_python_projects():
    st.title("🐍 Python Projects – LEGO Theme Analytics")

    st.write(
        """
        This section focuses on the **Python layer** of the LEGO project.

        Data is loaded from the SQL view `vw_theme_year_stats`, cleaned in
        a `data_preparation` module, and then explored through interactive
        analysis, visualisations, and forecasting.
        """
    )

    st.markdown("## 🧱 LEGO Theme Analytics (Python + SQL)")

    st.write(
        """
        **Goal**  
        Understand how LEGO themes evolve over time and support questions like:

        - Which themes are growing or declining?  
        - Which themes dominate LEGO’s yearly portfolio?  
        - When are new themes launched?  
        - How long do themes stay active?  
        - What might future set releases look like?

        **Tech stack**

        - **SQL Server:** analytical view `vw_theme_year_stats`  
        - **Python:** `pandas`, `matplotlib`, `prophet`  
        - **Structure:** modular files for loading, preparation, 
          visualisation, forecasting, and theme duration analysis  
        """
    )

    # ----- Load data once -----
    df_clean = load_clean_lego_data()

    with st.expander("🔎 Data preview", expanded=False):
        st.write("First 10 rows of the cleaned dataset (from `vw_theme_year_stats`):")
        st.dataframe(df_clean.head(10))

    st.markdown("### 🔍 Interactive Analysis & Tools")

    # Tabs = your different interaction modules
    tab_trends, tab_forecast, tab_explorer, tab_duration = st.tabs(
        [
            "📈 Theme Trends",
            "📉 Forecasting",
            "🕵 Year Explorer",
            "⏱ Theme Duration",
        ]
    )

    with tab_trends:
        st.write(
            """
            **Theme Trends**

            - Line chart: number of sets per year for a selected theme  
            - Line chart: portfolio share (%) per year for that theme  
            - Bar chart: sets per theme in a selected year  

            These views are powered by your `theme_trends.py` module.
            """
        )
        show_theme_trend_charts(df_clean)
        show_year_bar_chart(df_clean)

    with tab_forecast:
        st.write(
            """
            **Forecasting (Prophet)**

            - Choose a theme and forecast horizon (years)  
            - Prophet model: year → number of sets for that theme  
            - Output: forecast plot + last 10 predicted values  

            Implemented in `theme_forecasting.py` +
            `theme_forecasting_interaction.py`.
            """
        )
        run_forecast_interaction(df_clean)

    with tab_explorer:
        st.write(
            """
            **Year Explorer**

            - Input a year and see all themes active that year  
            - See which themes are newly launched (`is_new_theme_year`)  
            - Rank themes by number of sets and portfolio share  

            Implemented in `year_explorer_cool_function.py`.
            """
        )
        run_year_explorer(df_clean)

    with tab_duration:
        st.write(
            """
            **Theme Duration Analysis**

            - Calculate first and last active year per theme  
            - Compute how many years each theme has been active  
            - Rank longest-running themes in LEGO history  

            Implemented in `theme_duration_interaction.py`.
            """
        )
        run_theme_duration_interaction(df_clean)

    st.markdown("---")
    st.caption("All Python analysis in this portfolio is based on the LEGO dataset.")


def show_sql_projects():
    st.title("🗄 SQL Projects – LEGO Theme Trend Analysis")

    st.write(
        """
        This section summarises the **SQL work** that prepares the LEGO data
        for Python and Power BI. All queries are built on top of the original
        `sets` and `themes` tables and combined into the view
        **`vw_theme_year_stats`**.
        """
    )

    st.markdown("## 🔧 Key SQL Analyses")

    st.markdown("### 1. Sets per theme per year (base dataset)")
    st.code(
        """
        SELECT 
            s.year,
            t.name AS theme,
            COUNT(*) AS num_sets
        FROM dbo.sets s
        JOIN dbo.themes t 
            ON s.theme_id = t.id
        GROUP BY s.year, t.name
        ORDER BY s.year, t.name;
        """,
        language="sql",
    )
    st.write(
        "- Counts how many sets are released for each theme in each year.\n"
        "- Serves as the base dataset for all further analysis."
    )

    st.markdown("### 2. Year-on-year growth per theme")
    st.code(
        """
        WITH theme_year AS (
            SELECT 
                s.year,
                t.name AS theme,
                COUNT(*) AS num_sets
            FROM sets s
            JOIN themes t 
                ON s.theme_id = t.id
            GROUP BY s.year, t.name
        ),
        with_lag AS (
            SELECT
                year,
                theme,
                num_sets,
                LAG(num_sets) OVER (PARTITION BY theme ORDER BY year) AS prev_num_sets
            FROM theme_year
        )
        SELECT
            year,
            theme,
            num_sets,
            prev_num_sets,
            (num_sets - prev_num_sets) AS abs_change,
            CASE 
                WHEN prev_num_sets IS NULL OR prev_num_sets = 0 THEN NULL
                ELSE ROUND(100.0 * (num_sets - prev_num_sets) / prev_num_sets, 2)
            END AS pct_change
        FROM with_lag
        ORDER BY theme, year;
        """,
        language="sql",
    )
    st.write(
        "- Uses `LAG` to compare each year to the previous year.\n"
        "- Produces absolute and percentage growth for each theme."
    )

    st.markdown("### 3. Top 10 fastest-growing themes")
    st.code(
        """
        WITH theme_year AS (
            SELECT 
                s.year,
                t.name AS theme,
                COUNT(*) AS num_sets
            FROM sets s
            JOIN themes t 
                ON s.theme_id = t.id
            GROUP BY s.year, t.name
        ),
        with_lag AS (
            SELECT
                year,
                theme,
                num_sets,
                LAG(num_sets) OVER (PARTITION BY theme ORDER BY year) AS prev_num_sets
            FROM theme_year
        ),
        growth AS (
            SELECT
                year,
                theme,
                num_sets,
                prev_num_sets,
                (num_sets - prev_num_sets) AS abs_change,
                CASE 
                    WHEN prev_num_sets IS NULL OR prev_num_sets = 0 THEN NULL
                    ELSE ROUND(100.0 * (num_sets - prev_num_sets) / prev_num_sets, 2)
                END AS pct_change
            FROM with_lag
        )
        SELECT TOP 10
            theme,
            year,
            num_sets,
            prev_num_sets,
            abs_change,
            pct_change
        FROM growth
        WHERE pct_change IS NOT NULL
        ORDER BY pct_change DESC;
        """,
        language="sql",
    )
    st.write(
        "- Identifies themes with explosive year-on-year growth.\n"
        "- Shows which year each theme peaked."
    )

    st.markdown("### 4. Total sets released per theme (lifetime ranking)")
    st.code(
        """
        SELECT 
            t.name AS theme,
            COUNT(*) AS total_sets
        FROM sets s
        JOIN themes t 
            ON s.theme_id = t.id
        GROUP BY t.name
        ORDER BY total_sets DESC;
        """,
        language="sql",
    )
    st.write(
        "- Ranks themes by total number of sets ever released.\n"
        "- Highlights the most important themes in LEGO’s portfolio."
    )

    st.markdown("### 5. Portfolio contribution (% of total sets per year)")
    st.code(
        """
        WITH theme_year AS (
            SELECT 
                s.year,
                t.name AS theme,
                COUNT(*) AS num_sets
            FROM sets s
            JOIN themes t 
                ON s.theme_id = t.id
            GROUP BY s.year, t.name
        ),
        year_total AS (
            SELECT 
                year,
                SUM(num_sets) AS total_sets_year
            FROM theme_year
            GROUP BY year
        )
        SELECT 
            ty.year,
            ty.theme,
            ty.num_sets,
            yt.total_sets_year,
            ROUND(100.0 * ty.num_sets / yt.total_sets_year, 2) AS pct_of_portfolio
        FROM theme_year ty
        JOIN year_total yt
            ON ty.year = yt.year
        ORDER BY 
            ty.year ASC,            
            pct_of_portfolio ASC;
        """,
        language="sql",
    )
    st.write(
        "- Measures each theme’s share of LEGO’s yearly product portfolio.\n"
        "- Used later in Python visualisations of portfolio share."
    )

    st.markdown("### 6. New theme launches per year")
    st.code(
        """
        WITH theme_year AS (
            SELECT 
                s.year,
                t.name AS theme
            FROM dbo.sets s
            JOIN dbo.themes t 
                ON s.theme_id = t.id
            GROUP BY s.year, t.name
        ),
        first_year AS (
            SELECT 
                theme,
                MIN(year) AS first_year
            FROM theme_year
            GROUP BY theme
        )
        SELECT 
            first_year AS year,
            COUNT(*) AS new_themes_launched
        FROM first_year
        GROUP BY first_year
        ORDER BY year;
        """,
        language="sql",
    )
    st.write(
        "- Finds the first year each theme appears.\n"
        "- Counts how many new themes were introduced in each year."
    )

    st.markdown("### 7. Final analytical view: `vw_theme_year_stats`")
    st.write(
        """
        All of the above logic is combined into a single SQL Server view
        **`vw_theme_year_stats`**, which contains:

        - `year`, `theme`, `num_sets`  
        - `prev_num_sets`, `abs_change`, `pct_change`  
        - `total_sets_year`, `pct_of_portfolio`  
        - `is_new_theme_year`, `new_themes_launched`  

        This view is the **single source of truth** used by:

        - `load_theme_year_stats()` in Python  
        - Power BI dashboards (planned)
        """
    )

    st.info(
        "In a full portfolio or GitHub repo, you can include the complete "
        "SQL script file (e.g. `SQL/LEGO_THEME_SET.sql`) with all queries."
    )


def show_powerbi_projects():
    st.title("📊 Power BI Dashboards – LEGO Theme Analytics")

    st.write(
        """
        These dashboards were created in **Power BI** using the `vw_theme_year_stats`
        dataset, which contains yearly LEGO theme performance from 1949 to 2024
        and has been cleaned by python and SQL.

        The dashboards explore:
        1.total sets released per year
        2.total sets by theme
        3.precentage of portfolio by themes(how many sets released for the theme compare to total sets released in the year)
        4.longest-running LEGO themes
        5.Total launched themes card
        6.interactive filters for year and theme
        """
    )

    st.subheader("📈 Dashboard Preview")

    # Show screenshots of the dashboard
    st.image("Projects/PowerBI/dashboard1.png", caption="Dashboard Overview")
    st.image("Projects/PowerBI/dashboard2-slicer.png", caption="Total sets by theme")
    st.image("Projects/PowerBI/dax.png", caption="Dax-add new column,measure")
    st.image("Projects/PowerBI/power-query.png", caption="transform data")

    st.subheader("⬇ Download Power BI Report")
    with open("Projects/PowerBI/LEGO_THEME_SETS.pbix", "rb") as f:
        data = f.read()
        st.download_button(
            label="Download LEGO Power BI Dashboard (.pbix)",
            data=data,
            file_name="LEGO_THEME_SETS.pbix",
            mime="application/octet-stream"
        )


# ========= ROUTER =========
if page == "🏠 Overview":
    show_overview()
elif page == "🐍 Python Projects":
    show_python_projects()
elif page == "🗄 SQL Projects":
    show_sql_projects()
elif page == "📊 Power BI Dashboards":
    show_powerbi_projects()

st.markdown("---")
st.caption("Last updated: 2025.")


