import glob
import os
import pandas as pd
from sqlalchemy import create_engine

# Define paths
keywords_dir = '/Users/apple/PycharmProjects/pythonDb/Keywords/'
output_dir = "/Users/apple/PycharmProjects/pythonDb/final_csv"
description_dir = '/Users/apple/PycharmProjects/pythonDb/SqlGen/'


# Function to read and concatenate CSV files from a directory
def read_and_concatenate_csvs(directory):
    csv_files = glob.glob(directory + '*.csv')
    dataframes = [pd.read_csv(file) for file in csv_files]
    return pd.concat(dataframes, ignore_index=True).astype(str)


# Read and combine keyword CSV files
combined_df = read_and_concatenate_csvs(keywords_dir)

# Filter out sponsored entries
filtered_df = combined_df[combined_df['Sponsored'] != "True"]

# Replace '+' with spaces in the search terms
filtered_df['search_term'] = filtered_df['search_term'].str.replace("+", " ")

# Save the combined DataFrame to a single CSV file in the output directory
os.makedirs(output_dir, exist_ok=True)
combined_csv_path = os.path.join(output_dir, 'combined_data.csv')
filtered_df.to_csv(combined_csv_path, index=False)

# Prepare data for database
db_df = filtered_df.drop_duplicates(subset='search_term', keep='first')[['search_term', 'image_url', 'discount']]

# Format the discount column
db_df['discount'] = db_df['discount'].apply(lambda x: f"Upto {x}% Off" if x != '0' else "")

# Capitalize search terms
db_df['search_term'] = db_df['search_term'].str.title()

# Save the processed data to a new CSV file
new_csv_path = os.path.join(output_dir, 'new_csv.csv')
db_df.to_csv(new_csv_path, index=False)

# Read and combine description CSV files
description_df = read_and_concatenate_csvs(description_dir)


# Function to find the common prefix in a list of strings
def find_common_prefix(strings):
    if not strings:
        return ''
    min_string = min(strings)
    max_string = max(strings)
    for i, c in enumerate(min_string):
        if c != max_string[i]:
            return min_string[:i]
    return min_string


# Function to replace the common prefix with a placeholder
def replace_common_prefix(df, column_name, placeholder):
    strings = df[column_name].tolist()
    common_prefix = find_common_prefix(strings)
    df[column_name] = df[column_name].str.replace(common_prefix, placeholder)

    # Print key-value pairs of placeholder vs values
    unique_values = df[column_name].unique()
    placeholder_values = {placeholder: common_prefix}
    for value in unique_values:
        if value != placeholder:
            placeholder_values[value] = value.replace(placeholder, common_prefix)
    print("Placeholder vs Values:")
    for key, value in placeholder_values.items():
        print(f"{key}: {value}")


# Replace common prefix in image URLs with a placeholder
replace_common_prefix(description_df, 'image_url', '__PH1__')

# Create SQL directory if it does not exist
sql_dir = 'sql_files'
os.makedirs(sql_dir, exist_ok=True)

# Prepare final DataFrame for the database
final_df = description_df.drop_duplicates(subset='search_term', keep='first')[
    ['search_term', 'image_url', 'subtitle', 'description']]

# Define the database path and engine
db_path = os.path.join(sql_dir, 'DynamicAdAssets.db')
engine = create_engine(f'sqlite:///{db_path}')

# Save the DataFrame to the SQL database
final_df.to_sql('DynamicAssets', engine, index=False, if_exists='replace')
