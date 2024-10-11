import pyarrow.parquet as pq
import os
import pandas as pd

'''
Extracts simple data file info from parquet file.
'''

# Use the absolute path to the Parquet file
parquet_file_path = os.path.abspath('simpleWikiData.parquet')
print("Attempting to open:", parquet_file_path)

# Initialize a list to store DataFrames
batch_dataframe = []

# Open the Parquet file
try:
    parquet_file = pq.ParquetFile(parquet_file_path)

    # Iterate through batches and convert to DataFrames
    for i in parquet_file.iter_batches(batch_size=350):
        batch_dataframe.append(i.to_pandas())
    
    # Concatenate all DataFrames into a single DataFrame
    all_data = pd.concat(batch_dataframe, ignore_index=True)

    # Display the first few rows of the DataFrame
    print("First 10 rows of the DataFrame:")
    print(all_data.head(10))

    print(f"Number of text rows: {len(all_data)}")
    
except FileNotFoundError as e:
    print("Error:", e)
