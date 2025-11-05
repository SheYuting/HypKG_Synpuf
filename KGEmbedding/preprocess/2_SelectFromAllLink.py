import pandas as pd
import os

# Define input and output directories
input_directory = r'KGEALL/PrepRelation/All_Link/ProcessTotal'
inputAll = r'KGENewMethod/mimic_ibkh_linkv2.csv'
output_directory = r'KGENewMethod/Data/combineData'

print("Running")

# Read the input CSV
allink = pd.read_csv(inputAll)

# List all files in the input directory
files = [file_name for file_name in os.listdir(input_directory)]

# Initialize a list to store unique 'ibkh_name' values
ibkhName = []

# Loop through the 'ibkh_name' column and add unique values to the list
for i in allink['ibkh_name']:
    if i not in ibkhName:
        ibkhName.append(i)

# Create a DataFrame from the list of unique 'ibkh_name' values
output = pd.DataFrame(ibkhName, columns=['ibkh_name'])

# Save the DataFrame to a CSV file
output.to_csv(os.path.join(output_directory, 'ibkh.csv'), index=False)

print("Saved combined ibkh.csv")
