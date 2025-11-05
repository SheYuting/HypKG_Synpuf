import os
import pandas as pd

def convert_csv_to_triplet_format(folder_path):
    # Iterate over all CSV files in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith('.csv'):
            file_path = os.path.join(folder_path, filename)
            # Read the CSV file
            df = pd.read_csv(file_path)
            
            # Find the index of the 'Source' column
            source_col_index = df.columns.get_loc('Source')
            
            # Select head and tail columns
            head_col = df.iloc[:, 0]  # first column is head entity
            tail_col = df.iloc[:, 1]  # second column is tail entity
            
            # Initialize an empty DataFrame to store all triplets
            all_triplets = pd.DataFrame(columns=['Head', 'Relation', 'Tail'])
            
            # Iterate over relation columns (from column 3 up to Source column, exclusive)
            for rel_index in range(2, source_col_index):
                relation_col = df.columns[rel_index]
                # Create a DataFrame with Head, Relation, and Tail
                triplet_df = pd.DataFrame({
                    'Head': head_col,
                    'Relation': df.iloc[:, rel_index],  # specific relation column
                    'Tail': tail_col
                })
                
                # Append the triplets to the main DataFrame
                all_triplets = pd.concat([all_triplets, triplet_df], ignore_index=True)
            
            # Create the output filename (only one file per input CSV)
            output_filename = f'triplets_{filename.split(".")[0]}.csv'
            output_path = os.path.join(r'KGENewMethod/Data/tripletData', output_filename)
            
            # Save the final triplet DataFrame to CSV
            all_triplets.to_csv(output_path, index=False)
            print(f'Saved triplet file: {output_path}')

# Specify the folder path where your CSV files are located
folder_path = 'KGEALL/PrepRelation/All_Link/ProcessTotal'

# Call the function to convert and save triplets
convert_csv_to_triplet_format(folder_path)
