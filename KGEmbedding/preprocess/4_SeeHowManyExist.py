import pandas as pd

# Load the relevant triplets and allink files
input = pd.read_csv(r"KGENewMethod/Data/ReducedData/filtered_final2.csv")
allink = pd.read_csv(r"KGENewMethod/Data/combineData/ibkh.csv")  # Assuming it's a tab-separated file

# Get the list of ibkh_name from the allink file
ibkh_names = set(allink['ibkh_name'])

# Check how many ibkh_name entities appeared in either Head or Tail in the input
ibkh_in_triplets = set(input['Head']).union(set(input['Tail']))  # Combine Head and Tail entities

# Count how many ibkh_name entities are in the relevant triplets
matches = ibkh_in_triplets.intersection(ibkh_names)
match_count = len(matches)
total_ibkh_names = len(ibkh_names)

# Print out the result as x/total
print(f"{match_count}/{total_ibkh_names} ibkh_name entities appear in either Head or Tail")
