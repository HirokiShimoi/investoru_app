import pandas as pd

df = pd.read_csv('Zaikoichi.csv', header=None)

df = df.iloc[:, [2,3,]]

df.columns = ['product_code', 'name']

df.to_csv("cleaned_file.csv", index=False)