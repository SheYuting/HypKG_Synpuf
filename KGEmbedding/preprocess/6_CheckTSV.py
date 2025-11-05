import pandas as pd

# Load the TSV file
file_path = r'KGENewMethod/Data/finalData/final.tsv'

# Read the TSV file
data = pd.read_csv(file_path, sep='\t')

# Print the first few rows to check the content
print(data.head())  # Shows the first 5 rows by default
