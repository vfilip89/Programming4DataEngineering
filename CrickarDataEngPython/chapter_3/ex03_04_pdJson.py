import pandas as pd

df1 = pd.read_json('data.json')

print(df1['records'][0])       # First record
print(df1['records'][0]['name'])  # Name of the first record

for i in range(10):
    print(df1['records'][i])  


#--------------------------------------------------------------#
import pandas as pd
import json  # Use Python's built-in JSON library

# Reading Nested JSON
with open('data.json', 'r') as f:
    data = json.load(f)  # Use json.load() to parse JSON data

# Normalizing the JSON to create a DataFrame
df = pd.json_normalize(data, record_path='records')  # Use pd.json_normalize()

# Writing DataFrame to JSON
df.to_json('output_columns.json', orient='columns')  # Column-oriented JSON
df.to_json('output_records.json', orient='records')  # Record-oriented JSON

print("DataFrame written to json successfully!")
print(df.head())
print(df1.head())


