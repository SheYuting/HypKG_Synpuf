import pandas as pd
import json

# Load the CSV file
csv_file_path = r'E:\KGE\promote_ibkh_linkv1.csv'
csv_data = pd.read_csv(csv_file_path)

# Create a dictionary with 'node_id' as the key and 'ibkh_name' as the value
json_data = dict(zip(csv_data['node_id'], csv_data['ibkh_name']))

# Save the dictionary to a JSON file
json_file_path = r'E:\KGE\NewExperiment\PythonFiles\node_textPromote.json'
with open(json_file_path, 'w') as json_file:
    json.dump(json_data, json_file, indent=4)

print(f"JSON file has been created and saved to: {json_file_path}")
