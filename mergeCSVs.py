import pandas as pd

# Define the filenames and column to join on
file1 = 'csv2.csv'
file2 = 'csv1.csv'
join_col = 'name'

# Read in the CSV files as Pandas DataFrames
df1 = pd.read_csv(file1)
df2 = pd.read_csv(file2)

# Remove file extension from values in specified column in df1
df1[join_col] = df1[join_col].str.rsplit('.', 1).str[0]

# Perform an inner join on the specified column
merged = pd.merge(df1, df2, on=join_col, how='inner')

# Write the merged data to a new CSV file
merged.to_csv('merged.csv', index=False)