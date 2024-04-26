import os

import pandas as pd
import glob
import json


directory_path = '/Users/apple/PycharmProjects/pythonDb/keywords2/'
# Get a list of all CSV files in the directory
csv_files = glob.glob(directory_path + '*.csv')

# Initialize an empty list to store DataFrames
dfs = []

# Iterate over each CSV file, read it into a DataFrame, and append it to the list
for file in csv_files:
    df = pd.read_csv(file)
    dfs.append(df)

# Concatenate all DataFrames in the list into a single DataFrame
combined_df = pd.concat(dfs, ignore_index=True).astype(str)

combined_df.to_csv()
outputDir = "/Users/apple/PycharmProjects/pythonDb/final_csv"
os.makedirs(outputDir, exist_ok=True)

# Save the combined DataFrame to a single CSV file in the new directory
output_csv_file = os.path.join(outputDir, 'combined_data.csv')
combined_df.to_csv(output_csv_file, index=False)

new_df = combined_df.drop_duplicates(subset='search_term', keep='first')[
    ['search_term', 'image_url', 'price', "discount"]]
new_csv = os.path.join(outputDir, 'new_csv.csv')
new_df.to_csv(new_csv, index=False)

json_file = os.path.join(outputDir, 'new.json')
new_df.to_json(json_file, orient='records')

final_json = json.load(open(json_file))
print(final_json)


def convert_json_to_sql(final_json):
    columns = final_json[0].keys()

    data = []

    for item in final_json:
        columns_vals = []

        for column in columns:
            columns_vals.append(str(item.get(column, '')))

        data.append('(' + ",".join(f"'{item}'" for item in columns_vals) + ')')

    columns = '(' + ",".join(f"'{item}'" for item in columns) + ')'
    values = ",".join(data)

    return "INSERT INTO root_products {columns} VALUES {values}".format(columns=columns, values=values)



query_string = convert_json_to_sql(final_json)

query_file = os.path.join(outputDir, 'insert_query.sql')
with open(query_file, 'w') as f:
    f.write(query_string)
    f.close()
