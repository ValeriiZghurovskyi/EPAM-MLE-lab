import numpy as np
import pandas as pd
import pickle
import json
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

train_clean = pd.read_csv('data/processed.csv')

X = train_clean.drop(columns=['SalePrice'])
y = train_clean['SalePrice']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LinearRegression()
model.fit(X_train, y_train)                                 

pickle.dump(model, open('model.pkl', 'wb'))     

y_pred = model.predict(X_test)

rmse_multiple = np.sqrt(mean_squared_error(np.log(y_test), np.log(y_pred)))
r2_multiple = r2_score(y_test, y_pred)

metrics = {
    'Root Mean Squared Error': rmse_multiple,
    'R2 Score': r2_multiple
}

with open('metrics.json', 'w') as f:
    json.dump(metrics, f)
