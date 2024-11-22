import pyarrow.parquet as pq
import os
import pandas as pd

'''
Extracts the rows/text from the parquet file.
'''
# Extract all data from the Parquet file
def extract_parquet_data(parquet_file_path):
    try:
        parquet_file = pq.ParquetFile(parquet_file_path)
        batch_dataframe = []

        for i in parquet_file.iter_batches(batch_size=350):
            batch_dataframe.append(i.to_pandas())

        # Concatenate all batches into a single DataFrame
        all_data = pd.concat(batch_dataframe, ignore_index=True)
        
        return all_data
    
    except FileNotFoundError as e:
        print("Error:", e)

# Load the data
parquet_file_path = os.path.abspath('simpleWikiData.parquet')

# Extract all rows of data
all_data = extract_parquet_data(parquet_file_path)