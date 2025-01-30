import pandas as pd

# Example timedelta data
data = {'DURATION': [pd.Timedelta(minutes=5), pd.Timedelta(minutes=15),
                     pd.Timedelta(minutes=45), pd.Timedelta(hours=2)]}
df = pd.DataFrame(data)
print()
print(df.head())
print()

# Convert to seconds for binning
df['DURATION_SECONDS'] = df['DURATION'].dt.total_seconds()

# Define custom bins (e.g., short, medium, long)
bins = [0, 600, 1800, 3600]  # 0-10 min, 10-30 min, 30-60 min
labels = ['Short', 'Medium', 'Long']

# Apply pd.cut
df['DURATION_CATEGORY'] = pd.cut(df['DURATION_SECONDS'], bins=bins, labels=labels, right=False)

print(df)
print()
print(df['DURATION'].value_counts(bins=3))
print()
print(df['DURATION_SECONDS'].value_counts(bins=3))
