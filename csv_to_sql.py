import pandas as pd

# Load the CSV file
file_path = 'trip.csv'  # Update this with your actual file path
df = pd.read_csv(file_path)

# Generate the SQL statements
table_name = "trip"
columns = df.columns

# Create table statement
create_table_sql = f"CREATE TABLE {table_name} (\n"
for column in columns:
    create_table_sql += f"    {column} VARCHAR(255),\n"  # Defaulting to VARCHAR(255), adjust as needed
create_table_sql = create_table_sql.rstrip(",\n") + "\n);\n"

# Insert statements
insert_statements = []
for _, row in df.iterrows():
    values = "', '".join(map(str, row.values))
    insert_statements.append(f'INSERT INTO {table_name} ({", ".join(columns)}) VALUES ("{values}");')

# Combine all statements into one script
sql_script = create_table_sql + "\n" + "\n".join(insert_statements)

# Write the SQL script to a file
with open('output.sql', 'w') as file:
    file.write(sql_script)

print("SQL script generated and saved to output.sql")
