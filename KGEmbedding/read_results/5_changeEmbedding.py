import json
import pandas as pd
import numpy as np

# Load the JSON file with the entity list
with open(r'E:\KGE\NewExperiment\Result\TransE\node_text3.json', 'r') as f:
    entity_list = json.load(f)

# Load the CSV file with the embeddings
embeddings_df = pd.read_csv(
    r'E:\KGE\NewExperiment\Result\TransE\combined_data.csv', header=None)

# Prepare a list to hold the final results
result = []

# Iterate through the entity list
for entity_id, entity_name in entity_list.items():
    # Try to find the corresponding name in the embeddings file
    matched_row = embeddings_df[embeddings_df[1] == entity_name]

    if not matched_row.empty:
        # If found, use the name and embedding from the CSV
        embedding_values = matched_row.iloc[0, 2:].tolist()
    else:
        # If not found, use 128 zeros
        embedding_values = [0] * 128

    # Add the result to the list
    result.append([entity_name] + embedding_values)

# Convert the result to a DataFrame
result_df = pd.DataFrame(result)

# Save the result as a CSV file
result_df.to_csv(
    r'E:\KGE\NewExperiment\Result\TransE\MIMICTransLarge_Embedding.csv', index=False, header=False)

print("Processing complete. The result has been saved to 'modified_entity_embeddings3.csv'.")
