from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
import pandas as pd
import requests
import os
from sklearn.model_selection import train_test_split, KFold
from sklearn.preprocessing import OneHotEncoder

args = {
    'owner': 'Airflow',
    'start_date': datetime.today(),
}

dag = DAG(
    dag_id='future_sales_data_preprocessing',
    default_args=args,
    description='A simple data preprocessing dag',
    schedule_interval=None,
)

def load_and_merge_data_task(**context):
    sales_train = pd.read_csv('/opt/airflow/data/sales_train.csv')
    items = pd.read_csv('/opt/airflow/data/items.csv')
    item_categories = pd.read_csv('/opt/airflow/data/item_categories.csv')
    shops = pd.read_csv('/opt/airflow/data/shops.csv')

    sales_train = sales_train.merge(shops, on='shop_id', how='left')
    sales_train = sales_train.merge(items, on='item_id', how='left')
    sales_train = sales_train.merge(item_categories, on='item_category_id', how='left')
    sales_train.to_csv('/opt/airflow/data/sales_train_merged.csv', index=False)

def check_data_types_task(**context):
    data = pd.read_csv('/opt/airflow/data/sales_train_merged.csv')
    data['date'] = pd.to_datetime(data['date'], format='%d.%m.%Y')
    data[['date_block_num', 'shop_id', 'item_id', 'item_category_id']] = data[['date_block_num', 'shop_id', 'item_id', 'item_category_id']].astype(int)
    data[['item_price', 'item_cnt_day']] = data[['item_price', 'item_cnt_day']].astype(float)
    data[['shop_name', 'item_name', 'item_category_name']] = data[['shop_name', 'item_name', 'item_category_name']].astype(str)
    #context['ti'].xcom_push(key='data', value=data)
    data.to_csv('/opt/airflow/data/data.csv', index=False)

def fill_missing_values_task(**context):
    data = pd.read_csv('/opt/airflow/data/data.csv')
    item_category_mean = data.groupby('item_category_id')['item_price'].transform('mean')
    data['item_price'].fillna(item_category_mean, inplace=True)
    shop_median = data.groupby('shop_id')['item_cnt_day'].transform('median')
    data['item_cnt_day'].fillna(shop_median, inplace=True)
    data.fillna({
        'shop_name': 'unknown_shop',
        'item_name': 'unknown_item',
        'item_category_name': 'unknown_category'
    }, inplace=True)
    data.to_csv('/opt/airflow/data/data.csv', index=False)


def check_correct_values_task(**context):
    data = pd.read_csv('/opt/airflow/data/data.csv')
    data['item_price'] = data['item_price'].apply(lambda x: x if x >= 0 else 0)
    data['item_cnt_day'] = data['item_cnt_day'].apply(lambda x: x if x >= 0 else 0)
    data.to_csv('/opt/airflow/data/data.csv', index=False)
    
def drop_invalid_ids_task(**context):
    data = pd.read_csv('/opt/airflow/data/data.csv')
    data = data[data['shop_id'].ge(0) & data['item_id'].ge(0)]
    data = data.dropna(subset=['shop_id', 'item_id'])
    data.to_csv('/opt/airflow/data/data.csv', index=False)

def split_data_task(**context):
    data = pd.read_csv('/opt/airflow/data/data.csv')
    X = data.drop('item_cnt_day', axis=1)
    y = data['item_cnt_day']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    X_train.to_csv('/opt/airflow/data/X_train.csv', index=False)
    X_test.to_csv('/opt/airflow/data/X_test.csv', index=False)
    y_train.to_csv('/opt/airflow/data/y_train.csv', index=False)
    y_test.to_csv('/opt/airflow/data/y_test.csv', index=False)

def cross_validation_task(**context):
    X_train = pd.read_csv('/opt/airflow/data/X_train.csv')
    kf = KFold(n_splits=5)
    folds = []
    for train_index, val_index in kf.split(X_train):
        folds.append((train_index, val_index))
    context['ti'].xcom_push(key='folds', value=folds)

def one_hot_encoding_task(**context):
    X_train = pd.read_csv('/opt/airflow/data/X_train.csv')
    X_test = pd.read_csv('/opt/airflow/data/X_test.csv')
    
    encoder = OneHotEncoder(handle_unknown='ignore')

    X_train_encoded = encoder.fit_transform(X_train[['shop_name']])
    X_test_encoded = encoder.transform(X_test[['shop_name']])

    onehotcols = encoder.get_feature_names_out(['shop_name'])

    X_train_encoded_df = pd.DataFrame(X_train_encoded.todense(), columns=onehotcols)
    X_test_encoded_df = pd.DataFrame(X_test_encoded.todense(), columns=onehotcols)

    X_train = X_train.drop('shop_name', axis=1)
    X_test = X_test.drop('shop_name', axis=1)

    X_train = pd.concat([X_train, X_train_encoded_df], axis=1)
    X_test = pd.concat([X_test, X_test_encoded_df], axis=1)

    X_train.to_csv('/opt/airflow/data/X_train.csv', index=False)
    X_test.to_csv('/opt/airflow/data/X_test.csv', index=False)

def drop_columns_task(**context):
    columns_to_drop = ['item_category_name', 'item_name', 'item_id']
    chunksize = 100000

    for i, chunk in enumerate(pd.read_csv('/opt/airflow/data/X_train.csv', chunksize=chunksize)):
        chunk = chunk.drop(columns_to_drop, axis=1)
        if i == 0:
            chunk.to_csv('/opt/airflow/data/X_train.csv', index=False, mode='w')
        else:
            chunk.to_csv('/opt/airflow/data/X_train.csv', index=False, mode='a', header=False)

    for i, chunk in enumerate(pd.read_csv('/opt/airflow/data/X_test.csv', chunksize=chunksize)):
        chunk = chunk.drop(columns_to_drop, axis=1)
        if i == 0:
            chunk.to_csv('/opt/airflow/data/X_test.csv', index=False, mode='w')
        else:
            chunk.to_csv('/opt/airflow/data/X_test.csv', index=False, mode='a', header=False)


download_shops = PythonOperator(
    task_id='download_shops',
    python_callable=download_shops_task,
    dag=dag,
)

download_sales_train = PythonOperator(
    task_id='download_sales_train',
    python_callable=download_sales_train_task,
    dag=dag,
)

download_items = PythonOperator(
    task_id='download_items',
    python_callable=download_items_task,
    dag=dag,
)

download_item_categories = PythonOperator(
    task_id='download_item_categories',
    python_callable=download_item_categories_task,
    dag=dag,
)

load_and_merge_data = PythonOperator(
    task_id='load_and_merge_data',
    python_callable=load_and_merge_data_task,
    provide_context=True,
    dag=dag,
)

check_data_types = PythonOperator(
    task_id='check_data_types',
    python_callable=check_data_types_task,
    provide_context=True,
    dag=dag,
)

fill_missing_values = PythonOperator(
    task_id='fill_missing_values',
    python_callable=fill_missing_values_task,
    provide_context=True,
    dag=dag,
)

check_correct_values = PythonOperator(
    task_id='check_correct_values',
    python_callable=check_correct_values_task,
    provide_context=True,
    dag=dag,
)

drop_invalid_ids = PythonOperator(
    task_id='drop_invalid_ids',
    python_callable=drop_invalid_ids_task,
    provide_context=True,
    dag=dag,
)

split_data = PythonOperator(
    task_id='split_data',
    python_callable=split_data_task,
    provide_context=True,
    dag=dag,
)

cross_validation = PythonOperator(
    task_id='cross_validation',
    python_callable=cross_validation_task,
    provide_context=True,
    dag=dag,
)

one_hot_encoding = PythonOperator(
    task_id='one_hot_encoding',
    python_callable=one_hot_encoding_task,
    provide_context=True,
    dag=dag,
)

drop_columns = PythonOperator(
    task_id='drop_columns',
    python_callable=drop_columns_task,
    provide_context=True,
    dag=dag,
)

load_and_merge_data >> check_data_types >> fill_missing_values >> check_correct_values >> drop_invalid_ids >> split_data >> cross_validation >> one_hot_encoding >> drop_columns
