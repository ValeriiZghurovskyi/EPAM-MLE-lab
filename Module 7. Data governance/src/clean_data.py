import pandas as pd
from sklearn.impute import KNNImputer

data = pd.read_csv('data/train.csv')

num_columns_to_impute = []
cat_columns_to_impute = []
columns_to_remove = []

for column in data.columns: 
    null_count = data[column].isnull().sum()

    if null_count >= 500: 
        columns_to_remove.append(column)
    elif null_count >= 1 and data[column].dtype in ['int64', 'float64']:
        num_columns_to_impute.append(column)
    elif null_count >= 1:
        cat_columns_to_impute.append(column)

data_clean = data.drop(columns_to_remove, axis=1)

knn_imputer = KNNImputer(n_neighbors=5, metric='nan_euclidean') 
knn_imputer.fit(data_clean[num_columns_to_impute]) 
data_clean[num_columns_to_impute] = knn_imputer.transform(data_clean[num_columns_to_impute])

for column in cat_columns_to_impute:
    data_clean[column].fillna(data_clean[column].mode()[0], inplace=True)

data_clean.to_csv('data/clean.csv', index=False)