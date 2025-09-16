import pandas as pd

df = pd.read_csv('scooter.csv')

print()
print(df.columns)
print()
print(df.dtypes)
print()
print(df['month'])
print()
print(df.head())  # First 5 rows
print()
print(df.tail())  # Last 5 rows
print()
print(df.shape)  # Returns (rows, columns)
print()
# pd.set_option('display.max_columns', 500)
# print(df.head())
# print()
print(df['DURATION'])
print()
print(df[['trip_id', 'DURATION', 'start_location_name']])
print()
print(df.sample(5))  # Get 5 random rows
print()
print(df[:10])  # First 10 rows
print()
print(df[10:])  # Rows from 10 to the end
print()
print(df[3:9])  # Rows from 3 to 8 (inclusive of start, exclusive of end)
print()
print(df.loc[34221])  # Access a specific row by index that here is an integer
print()
print(df.at[2, 'DURATION'])  # Access a specific value
print()
print(df[df['user_id'] == 8417864])
print()
condition1 = df['user_id'] == 8417864
condition2 = df['trip_ledger_id'] == 1488838
print(df[condition1 & condition2])  # Rows matching both conditions
print()
user=df.where(df['user_id']==8417864)
print(user)
print()
one=df['user_id']==8417864
two=df['trip_ledger_id']==1488838
print(df.where(one & two))