import os
import pandas as pd

def combine_triplet_files(input_folder, combined_output_path):
    # Initialize an empty DataFrame to store combined triplets
    combined_triplets = pd.DataFrame(columns=['Head', 'Relation', 'Tail'])
    
    # Iterate over all CSV files in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith('.csv') and not filename.startswith('2'):
            file_path = os.path.join(input_folder, filename)
            # Read the CSV file
            triplet_df = pd.read_csv(file_path)
            
            # Concatenate the triplet DataFrame with the combined DataFrame
            combined_triplets = pd.concat([combined_triplets, triplet_df], ignore_index=True)
            print(f'Added {filename} to the combined DataFrame.')
    
    # Save the combined DataFrame to a single CSV file
    combined_triplets.to_csv(combined_output_path, index=False)
    print(f'Combined file saved as: {combined_output_path}')

# Specify the folder where the individual triplet CSV files are stored
input_folder = r'KGENewMethod/Data/tripletData'
# Specify the path for the combined CSV output file
combined_output_path = r'KGENewMethod/Data/combineData/combined_triplets.csv'

# Call the function to combine all triplet CSV files into one
combine_triplet_files(input_folder, combined_output_path)
