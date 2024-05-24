import pandas as pd
from sklearn.preprocessing import LabelEncoder

data_clean = pd.read_csv('data/clean.csv')

cat_columns = data_clean.select_dtypes(include=['object'])

label_encoder = LabelEncoder()

for columna in cat_columns.columns:
    data_clean[columna] = label_encoder.fit_transform(data_clean[columna])

data_clean.to_csv('data/encoded.csv', index=False)