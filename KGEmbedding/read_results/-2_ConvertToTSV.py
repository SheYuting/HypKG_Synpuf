import pandas as pd

# Load the final data from CSV
input = pd.read_csv(
    r"E:\KGE\NewExperiment\filtered_final4.csv")

# Specify the column names
input.columns = ['Head', 'Relation', 'Tail']

# Convert the DataFrame to a TSV file, ensuring the headers are included
output_path = r"E:\KGE\NewExperiment\filtered_final4.tsv"
input.to_csv(output_path, sep='\t', index=False)

print(f"Data successfully saved to {output_path} with column headers")
