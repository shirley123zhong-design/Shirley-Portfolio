import pandas as pd
import sqlalchemy as sa

# 🔹 Replace this with your actual Server Name and Database Name
server = "YOUR_SERVER_NAME"
database = "LEGO"
driver = "ODBC Driver 17 for SQL Server"

# Build connection string
conn_str = f"mssql+pyodbc://{server}/{database}?driver={driver}"

try:
    engine = sa.create_engine(conn_str)
    df = pd.read_sql("SELECT TOP 5 * FROM dbo.vw_theme_year_stats", engine)
    print("SUCCESS! Connection works. Here's a preview:")
    print(df)
except Exception as e:
    print("Connection failed. Error:")
    print(e)

print("All imports successful!")