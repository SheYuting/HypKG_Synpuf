import pandas as pd
from tqdm import tqdm

# File paths
triplets_file_path = r'KGENewMethod/Data/combineData/combined_triplets.csv'
ibkh_file_path = r'KGENewMethod/Data/combineData/ibkh.csv'
output_file_path = r'KGENewMethod/Data/RelaventData/relevant_triplets.csv'

# Load the CSV files
print("Loading data...")
triplets_df = pd.read_csv(triplets_file_path)
ibkh_df = pd.read_csv(ibkh_file_path)

# Get the list of ibkh_names
ibkh_names = set(ibkh_df['ibkh_name'])

# Initialize set for entities that are relevant and a list for relevant triplets
relevant_entities = set(ibkh_names)
relevant_triplets = []

# Selecting relevant relations with progress bar
print("Selecting relevant relations...")
for _, row in tqdm(triplets_df.iterrows(), total=len(triplets_df)):
    head, relation, tail = row['Head'], row['Relation'], row['Tail']
    
    # Check if both head and tail are in ibkh_names
    if head in ibkh_names and tail in ibkh_names:
        relevant_triplets.append(row)
        relevant_entities.update([head, tail])
    # Check if one entity is in ibkh_names and the other is connected in another relation
    elif (head in ibkh_names or tail in ibkh_names):
        # We keep this relation for now but check further in the next loop for connections
        relevant_triplets.append(row)

# Filter again based on new connections in relevant_triplets
final_relevant_triplets = []
for triplet in relevant_triplets:
    head, tail = triplet['Head'], triplet['Tail']
    if head in relevant_entities or tail in relevant_entities:
        final_relevant_triplets.append(triplet)

# Convert list back to DataFrame
relevant_triplets_df = pd.DataFrame(final_relevant_triplets)

# Save the relevant triplets to a new CSV
print(f"Saving relevant relations to {output_file_path}...")
relevant_triplets_df.to_csv(output_file_path, index=False)

print(f"Relevant relations saved to {output_file_path}")
