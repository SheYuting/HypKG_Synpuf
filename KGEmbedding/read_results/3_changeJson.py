import json
import pandas as pd

# Load the JSON file
with open(r'E:\KGE\NewExperiment\Result\ComplExSmall\node_text3.json', 'r') as file:
    json_data = json.load(file)

# Load the CSV file
csv_data = pd.read_csv(r'E:\KGE\mimic_ibkh_linkv3.csv')

# Create a dictionary to map node_id (which corresponds to the index in JSON) to ibkh_name
index_mapping = dict(
    zip(csv_data['node_id'].astype(str), csv_data['ibkh_name']))

# Replace the names in the JSON data with the corresponding ibkh_name based on index
updated_json_data = {}
for key, value in json_data.items():
    if key in index_mapping:
        updated_json_data[key] = index_mapping[key]
    else:
        # Keep the original if no match is found
        updated_json_data[key] = value

# Save the updated JSON file
with open('updated_json_file.json3', 'w') as file:
    json.dump(updated_json_data, file, indent=4)

print("JSON file has been updated and saved as 'updated_json_file3.json'.")
