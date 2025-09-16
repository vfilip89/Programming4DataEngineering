import pandas as pd
from EDA_Crickard_ch5 import clean_scooter_data_ex05_03, modify_scooter_data_ex05_04


df = pd.read_csv('scooter.csv')

# print()
# print(df.head())  # First 5 rows
# print()
# print(df.tail())  # Last 5 rows
print()
print(df.isnull().sum())
print()
print(df.info())

# # Clean the dataset using the function of ex05_03.
# df = clean_scooter_data_ex05_03(df)
# print()
# print(df.isnull().sum())
# print()
# print(df.info())

# # Modify the dataset using the function of ex05_04.
# df = modify_scooter_data_ex05_04(df)
# print()
# print(df.isnull().sum())
# print()
# print(df.info())

# Get the top 5 most frequent starting locations
new = pd.DataFrame(df['start_location_name'].value_counts().head())
new.reset_index(inplace=True)
new.columns = ['address', 'count']
print(new)
print()

# Split address to extract street information
n = new['address'].str.split(pat=',', n=1, expand=True)
replaced = n[0].str.replace("@", "and", regex=False)
new['street'] = replaced
print(new)
print()

# Load geocoded data
geo = pd.read_csv('geocodedstreet.csv')
print(geo)
print()

# # Join the top locations with geocoded data
# joined = new.join(other=geo, how='left', lsuffix='_new', rsuffix='_geo')
# print(joined[['street_new', 'street_geo', 'x', 'y']])

# Merge the top locations with geocoded data
merged = pd.merge(new, geo, on='street')
print(merged)
print()

