import pandas as pd

df = pd.read_csv('data.csv')
print(df.head(10))


data = {
    'Name': ['Paul', 'Bob', 'Susan', 'Yolanda'],
    'Age': [23, 45, 18, 21]
}
df = pd.DataFrame(data)
df.to_csv('fromdf.csv', index = False)
print(df)