import pandas as pd
import random

# Load the CSV file into a pandas dataframe
df = pd.read_csv('/Users/ashish/Desktop/aditya/bfro.csv')

# Get the number of records in the dataframe
num_records = len(df)

# Set the number of records you want to randomly select
num_to_select = 50

# Generate a list of 50 random integers between 0 and num_records
rand_indices = random.sample(range(num_records), num_to_select)

# Use iloc to select the rows corresponding to the random indices
selected_rows = df.iloc[rand_indices]

# Print the selected rows
print(selected_rows)
selected_rows.to_csv('/Users/ashish/Desktop/aditya/bf.csv', index=False)