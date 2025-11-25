import pandas as pd
import sqlalchemy as sa
import urllib

def load_theme_year_stats():
    """
    Connects to SQL Server and loads the LEGO theme-year view into a DataFrame.
    """

    odbc_str = (
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=GUYIFAT\\GUYI;"
        "DATABASE=LEGO;"
        "Trusted_Connection=yes;"
    )

    params = urllib.parse.quote_plus(odbc_str)
    engine = sa.create_engine(f"mssql+pyodbc:///?odbc_connect={params}")

    query = "SELECT * FROM dbo.vw_theme_year_stats;"
    df = pd.read_sql(query, engine)   # 👈 IMPORTANT: read_sql, not read

    return df


