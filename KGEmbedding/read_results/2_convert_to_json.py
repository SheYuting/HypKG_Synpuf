import pandas as pd
import json

# Load the CSV file
file_path = r'E:\KGE\NewExperiment\Result\TransE\training_triples\entity_to_id.tsv\entity_to_id.tsv'
df = pd.read_csv(file_path, sep='\t')

# Convert the DataFrame to a dictionary
data_dict = dict(zip(df.id.astype(str), df.label))

# Convert the dictionary to a JSON string without Unicode escape sequences
json_data = json.dumps(data_dict, ensure_ascii=False, indent=4)

# Specify the output path where you have write permissions
json_output_path = r'E:\KGE\NewExperiment\Result\TransE\training_triples\entity_to_id.tsv\entity_to_id.json'

# Save the JSON data to a file
with open(json_output_path, 'w', encoding='utf-8') as json_file:
    json_file.write(json_data)

print(f"JSON file has been saved to {json_output_path}")
