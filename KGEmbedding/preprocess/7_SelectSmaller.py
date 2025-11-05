import pandas as pd
import os

# Load the CSV file
df = pd.read_csv(r'KGENewMethod/Data/ReducedData/filtered_final3.csv')

# Count the occurrences of each entity in both Head and Tail columns
entity_count = pd.concat([df['Head'], df['Tail']]).value_counts()

# Function to filter entities that appear no more than 3000 times, but prioritize limiting them to 2000 occurrences
def limit_entity_appearances(df, max_limit=20, soft_limit=50):
    entity_appearance = {}
    
    filtered_rows = []
    
    # Iterate through the dataframe row by row
    for index, row in df.iterrows():
        head, tail = row['Head'], row['Tail']
        
        if head not in entity_appearance:
            entity_appearance[head] = 0
        if tail not in entity_appearance:
            entity_appearance[tail] = 0
        
        # Check if including the row would keep entities within limits
        if (entity_appearance[head] < max_limit or entity_appearance[tail] < max_limit):
            filtered_rows.append(row)
            entity_appearance[head] += 1
            entity_appearance[tail] += 1
        elif (entity_appearance[head] < soft_limit and entity_appearance[tail] < soft_limit):
            filtered_rows.append(row)
            entity_appearance[head] += 1
            entity_appearance[tail] += 1

    # Create new DataFrame from filtered rows
    return pd.DataFrame(filtered_rows)

# Apply the function to filter the DataFrame
filtered_df = limit_entity_appearances(df)

# Define output directory and file name
output_directory = 'KGENewMethod/Data/ReducedData'
output_file = os.path.join(output_directory, 'filtered_final4.csv')

# Ensure the directory exists
os.makedirs(output_directory, exist_ok=True)

# Save the filtered data to the specified CSV file
filtered_df.to_csv(output_file, index=False)
