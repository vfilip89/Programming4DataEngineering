import pandas as pd

df = pd.read_csv('scooter.csv')

# print()
# print(df.head())  # First 5 rows
# print()
# print(df.tail())  # Last 5 rows
print()
print(df.isnull().sum())
print()
print(df.info())

# print()
df.drop(columns=['region_id'], inplace=True)
# df.drop(index=[34225], inplace=True) # Drop a specific row
# print()
# print(df.tail())  # Last 5 rows
print()
print(df.info())

# print()
# print(df['start_location_name'][(df['start_location_name'].isnull())])
# # Drop rows where 'start_location_name' is null
# df.dropna(subset=['start_location_name'], inplace=True)
# print("\nDropped rows where 'start_location_name' is null\n")
# print(df['start_location_name'][(df['start_location_name'].isnull())])
# print()
# print(df.info())

# Drop columns with more than 25% null values
thresh = int(len(df) * 0.25)
df.dropna(axis=1, thresh=thresh, inplace=True)
print("\nDropped columns with more than 25% null values\n")
print()
print(df.info())

# Fill all NaNs in 'DURATION' with a default value
df.fillna({'DURATION': '00:00:00'}, inplace=True)
print("\nFilling all NaNs in 'DURATION' with '00:00:00'\n")
print()
print(df.info())

# Fill multiple columns with specific values
values = {'start_location_name': 'Start St.', 'end_location_name': 'Stop St.'}
df.fillna(value=values, inplace=True)
print("""\nTreating all NaNs in 'start_location_name':
      'Start St.', 'end_location_name': 'Stop St.'\n""")
print()
print(df.info())

print()
print(df['month'].value_counts())
# # Filter rows where month is 'May'
# may_rows = df[df['month'] == 'May']
# # Drop these rows from the DataFrame
# df.drop(index=may_rows.index, inplace=True)
# or just Combine filtering and dropping in a single step:
df = df[df['month'] != 'May']  # Removes all rows where month is May
print("\nDropped May-rows\n")
print()
print(df['month'].value_counts())
print()
print(df.info())

# Filter rows with both fields null
to_drop = df[(df['start_location_name'].isnull()) & (df['end_location_name'].isnull())]
# Drop these rows
df.drop(index=to_drop.index, inplace=True)
print("\nDropped rows with both 'start_location_name' and 'end_location_name' null\n")
print()
print(df.info())

# df.reset_index(drop=True, inplace=True)


