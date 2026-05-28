import pandas as pd
from sqlalchemy import create_engine

# 1. Read the Excel file we just generated
print("Reading Excel file...")
df = pd.read_excel('Student_Database_Export.xlsx')

# 2. Your PostgreSQL Connection String
# FORMAT: postgresql://username:password@host:port/database_name
# Replace these credentials with your actual local pgAdmin credentials!
PG_USER = "postgres"
PG_PASSWORD = "Password" 
PG_HOST = "localhost"
PG_PORT = "5432"
PG_DB = "student_db" # Make sure you create a blank database named 'student_db' in pgAdmin first!

DATABASE_URL = f"postgresql://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DB}"

try:
    # 3. Connect to PostgreSQL
    print("Connecting to PostgreSQL...")
    engine = create_engine(DATABASE_URL)
    
    # 4. Automatically build the table and upload the data
    print("Uploading data to PostgreSQL table 'students'...")
    df.to_sql('students', engine, if_exists='replace', index=False)
    
    print("✅ Success! The Excel data has been fully migrated to a PostgreSQL table.")

except Exception as e:
    print(f"❌ Failed to upload. Error: {e}")