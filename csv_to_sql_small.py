import pandas as pd
import os

# Load the CSV file
file_path = 'stoptimes.csv'  # Update this with your actual file path
df = pd.read_csv(file_path)

# Generate the SQL statements
table_name = "stoptimes"
columns = df.columns

# Create table statement
create_table_sql = f"CREATE TABLE {table_name} (\n"
for column in columns:
    create_table_sql += f"    {column} VARCHAR(255),\n"  # Defaulting to VARCHAR(255), adjust as needed
create_table_sql = create_table_sql.rstrip(",\n") + "\n);\n"

# Insert statements
insert_statements = []
for _, row in df.iterrows():
    values = "', '".join(map(str, row.values))  # Join values with ', '
    insert_statements.append(f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ('{values}');")

# Combine all statements into multiple scripts if size exceeds 1 MB
max_file_size = 1 * 800 * 800  # 1 MB in bytes
file_count = 1
current_file_size = 0
current_script = create_table_sql + "\n"

def write_to_file(script, count):
    with open(f'output_{count}.sql', 'w') as file:
        file.write(script)
    print(f"SQL script generated and saved to output_{count}.sql")

for statement in insert_statements:
    statement_size = len(statement.encode('utf-8')) + 1  # +1 for newline character
    if current_file_size + statement_size > max_file_size:
        write_to_file(current_script, file_count)
        file_count += 1
        current_script = create_table_sql + "\n"  # Include the table creation statement in each file
        current_file_size = 0
    current_script += statement + "\n"
    current_file_size += statement_size

# Write the remaining script to a new file
if current_script.strip():
    write_to_file(current_script, file_count)
