import pandas as pd
from EDA_Crickard_ch5 import clean_scooter_data_ex05_03


df = pd.read_csv('scooter.csv')

# print()
# print(df.head())  # First 5 rows
# print()
# print(df.tail())  # Last 5 rows
print()
print(df.isnull().sum())
print()
print(df.info())

# Clean the dataset using the function of ex05_03.
df = clean_scooter_data_ex05_03(df)
print()
print(df.isnull().sum())
print()
print(df.info())

# Make all column names lowercase
df.columns = [x.lower() for x in df.columns]
print()
print(df.columns)
# Alternatively, rename specific columns for clarity
df.rename(columns={'duration': 'trip_duration', 'trip_ledger_id': 'trip_ledger'}, inplace=True)
print()
print(df.columns)
# Make all values in the 'month' column uppercase
df['month'] = df['month'].str.upper()
print()
print(df['month'].value_counts())
print()

# Add a column with a static value
# df['new_column'] = 'Default Value'
# print(df['new_column'].value_counts())
# print()

# Add a column based on a condition with for loop
# for i,r in df.head().iterrows():
#     if r['trip_id']==1613335:
#         df.at[i,'new_column']='Yes'
#     else:
#         df.at[i,'new_column']='No'
# print(df[['trip_id', 'new_column']].head())
# print()

# Iterating through DataFrames works but can be very slow
# Add a column based on a condition more efficiently with loc
df['special_trip'] = 'No'
df.loc[df['trip_id'] == 1613335, 'special_trip'] = 'Yes'

print(df[['trip_id', 'special_trip']].head())
print()
print(df.info())
print()

print(df['started_at'].head())
print()

# Split 'started_at' into 'date' and 'time'
new = df['started_at'].str.split(expand=True)
df['date'], df['time'] = new[0], new[1]
print(df[['started_at', 'date', 'time']].head())
print()

# Convert 'started_at' to datetime
df['started_at'] = pd.to_datetime(df['started_at'], format='%m/%d/%Y %H:%M')
print(df.info())
print()
print(df.head())
print()

# Filter rows based on a datetime condition
filtered_df = df[df['started_at'] > '2019-07-1']
print(filtered_df.head())
print()

