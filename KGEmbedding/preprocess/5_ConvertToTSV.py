import pandas as pd

# Load the final data from CSV
input = pd.read_csv(r"KGENewMethod/Data/ReducedData/filtered_final3.csv")

# Specify the column names
input.columns = ['Head', 'Relation', 'Tail']

# Convert the DataFrame to a TSV file, ensuring the headers are included
output_path = r"KGENewMethod/Data/finalData/filtered_final3.tsv"
input.to_csv(output_path, sep='\t', index=False)

print(f"Data successfully saved to {output_path} with column headers")
