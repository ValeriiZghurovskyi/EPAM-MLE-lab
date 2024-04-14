import os
import json
import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.svm import SVC
import mlflow
import mlflow.pytorch


class IrisNet(nn.Module):
    def __init__(self):
        super(IrisNet, self).__init__()
        self.fc1 = nn.Linear(4, 128)
        self.fc2 = nn.Linear(128, 64)
        self.fc3 = nn.Linear(64, 32)
        self.fc4 = nn.Linear(32, 3)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = torch.relu(self.fc3(x))
        return self.fc4(x)


class IrisNet2(nn.Module):
    def __init__(self):
        super(IrisNet2, self).__init__()
        self.fc1 = nn.Linear(4, 64)
        self.fc2 = nn.Linear(64, 32)
        self.fc3 = nn.Linear(32, 3)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        return self.fc3(x)

def evaluate_model(model, X_test, y_test):
    model.eval()
    with torch.no_grad():
        outputs = model(X_test)
        _, predicted = torch.max(outputs, 1)
        accuracy = accuracy_score(y_test, predicted)
    return accuracy

def train_model(settings, model_to_train, learning_rate, epochs):
    torch.manual_seed(settings['general']['random_state'])
    run_name = f"{model_to_train}_lr_{learning_rate}_epochs_{epochs}"
    with mlflow.start_run(run_name=run_name):
        data_dir = settings['general']['data_dir']
        train_path = f"{data_dir}/{settings['train']['table_name']}"
        models_dir = settings['general']['models_dir']

        data = pd.read_csv(train_path)
        X = data.drop('target', axis=1).values
        y = LabelEncoder().fit_transform(data['target'])
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=settings['train']['test_size'], random_state=settings['general']['random_state'])

        mlflow.log_params({
            'model': model_to_train,
            'test_size': settings['train']['test_size'],
            'learning_rate': learning_rate,
            'epochs': epochs,
            'random_state': settings['general']['random_state']
        })
        mlflow.log_artifact('requirements.txt')

        X_train = torch.tensor(X_train, dtype=torch.float32)
        y_train = torch.tensor(y_train, dtype=torch.long)
        X_test = torch.tensor(X_test, dtype=torch.float32)
        y_test = torch.tensor(y_test, dtype=torch.long)
        train_dataset = TensorDataset(X_train, y_train)
        train_loader = DataLoader(dataset=train_dataset, batch_size=16, shuffle=True)
        
        if model_to_train == 'IrisNet':
            model = IrisNet()
        elif model_to_train == 'IrisNet2':
            model = IrisNet2()

        criterion = nn.CrossEntropyLoss()
        optimizer = optim.Adam(model.parameters(), lr=learning_rate)
        for epoch in range(epochs):
            model.train()
            all_predictions = [] 
            all_targets = [] 
            for X_batch, y_batch in train_loader:
                optimizer.zero_grad()
                outputs = model(X_batch)
                _, predictions = torch.max(outputs, 1)
                all_predictions.extend(predictions.tolist())
                all_targets.extend(y_batch.tolist())
                loss = criterion(outputs, y_batch)
                loss.backward()
                optimizer.step()

            accuracy = accuracy_score(all_targets, all_predictions)
            precision = precision_score(all_targets, all_predictions, average='macro')
            recall = recall_score(all_targets, all_predictions, average='macro')
            f1 = f1_score(all_targets, all_predictions, average='macro')

            mlflow.log_metrics({
                'Loss': loss.item(),
                'Accuracy': accuracy,
                'Precision': precision,
                'Recall': recall,
                'F1-Score': f1
            }, step=epoch)

        mlflow.pytorch.log_model(model, "models")

if __name__ == "__main__":
    with open('settings.json') as f:
        settings = json.load(f)
        
    mlflow.set_tracking_uri('http://mlflow-server:5000')
    mlflow.set_experiment('IrisNet_training_experiment')
    models = ['IrisNet', 'IrisNet2']
    learning_rates = [0.1, 0.01, 0.001]
    features_lists = [['sepal length (cm)', 'sepal width (cm)', 'petal length (cm)','petal width (cm)'],
                      ['sepal length (cm)', 'sepal width (cm)', 'petal length (cm)'],
                      ['sepal length (cm)', 'petal length (cm)','petal width (cm)'],
                      [ 'sepal width (cm)', 'petal length (cm)','petal width (cm)']]
    svc = SVC()

    for model in models:
        for learning_rate in learning_rates:
            train_model(settings, model, learning_rate, 50)


    for features in features_lists:
        data_dir = settings['general']['data_dir']
        train_path = f"{data_dir}/{settings['train']['table_name']}"
        data = pd.read_csv(train_path)
        X = data[features].values
        y = data['target']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=settings['train']['test_size'], random_state=settings['general']['random_state'])
        svc.fit(X_train, y_train)
        predictions = svc.predict(X_test)
        accuracy = svc.score(X_test, y_test)
        precision = precision_score(y_test, predictions, average='macro')
        recall = recall_score(y_test, predictions, average='macro')
        f1 = f1_score(y_test, predictions, average='macro')
        loss = 1 - accuracy

        features_str = "_".join(features) 
        run_name = f"SVC_{features_str}"
        with mlflow.start_run(run_name=run_name):
            mlflow.log_params({
                'model': 'SVC',
                'test_size': settings['train']['test_size'],
                'random_state': settings['general']['random_state']
            })
            mlflow.log_artifact('requirements.txt')

            mlflow.log_metrics({
                'Loss': loss.item(),
                'Accuracy': accuracy,
                'Precision': precision,
                'Recall': recall,
                'F1-Score': f1
            })

            mlflow.sklearn.log_model(svc, "models")
