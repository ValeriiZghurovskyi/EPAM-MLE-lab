import pandas as pd
from sklearn.preprocessing import StandardScaler

encoded_data = pd.read_csv('data/encoded.csv')

scaler = StandardScaler()

X = encoded_data.drop(columns=['SalePrice'])
y = encoded_data['SalePrice']
X_scaled = pd.DataFrame(scaler.fit_transform(X), columns=X.columns)

scaled_data = pd.concat([X_scaled, y], axis=1)

scaled_data.to_csv('data/processed.csv', index=False)