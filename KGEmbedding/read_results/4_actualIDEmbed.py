import pandas as pd

# Load the entity names file (first file)
entity_names = pd.read_csv(
    r'E:\KGE\NewExperiment\Result\TransE\training_triples\entity_to_id.tsv\entity_to_id.tsv', delimiter='\t')

# Load the embeddings file (second file) ensuring no row is treated as a header
embeddings = pd.read_csv(
    r'E:\KGE\NewExperiment\Result\TransE\transELarge_entity_embeddings_128.csv', header=0)

# Ensure the embeddings have the correct number of columns (128 in this case)
embeddings.columns = range(128)

# Combine the data
combined_data = pd.concat([entity_names, embeddings], axis=1)

# Save the combined data to a new CSV file with the correct headers
combined_data.to_csv(
    r'E:\KGE\NewExperiment\Result\TransE\combined_data.csv', index=False)

print("Data has been successfully merged and saved to 'combined_data.csv'")
