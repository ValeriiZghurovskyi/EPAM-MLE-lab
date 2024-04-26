## About

This Apache Airflow project presents a meticulous sequence of data preprocessing tasks, implemented as an Airflow DAG (Directed Acyclic Graph), that processes raw sales data and transforms it into a dataset ready for machine learning.

The `future_sales_data_preprocessing` DAG mainly includes the following tasks:

1. `load_and_merge_data_task`: This task loads the sales data and related data from `.csv` files such as `sales_train.csv`, `items.csv`, `item_categories.csv`, and `shops.csv`. These dataframes are then merged into a unified dataframe.

2. `check_data_types_task`: This task ensures the correct data types for each column in the merged dataframe. For instance, it converts the date from a string format to datetime, IDs from floating point numbers to integers, and so forth.

3. `fill_missing_values_task`: This task identifies any missing values present in the dataframe and fills them with suitable replacements. For example, missing price values are replaced with the mean price of the item category, missing item count values are substituted with the median count from the shop. Missing string values are filled with 'unknown'.

4. `check_correct_values_task`: This task ensures that all numerical values are non-negative. Negative values, if any present, are replaced with zeros.

5. `drop_invalid_ids_task`: This task drops the rows with invalid IDs. IDs should ideally be non-negative integers.

6. `split_data_task`: This task splits the dataframe into a training set and a testing set. The target column is the 'item_cnt_day'.

7. `cross_validation_task`: This task applies K-Fold cross-validation on the training set to prepare for machine learning model evaluation.

8. `one_hot_encoding_task`: This task applies one-hot encoding to categorical variables to prepare the data for machine learning algorithms.

9. `drop_columns_task`: This task drops unused or unnecessary columns from the dataframe. This task is performed by loading the data one chunk at a time to preserve memory.

These tasks are structured in such a way that each task depends on the successful completion of its preceding task. This dependency pattern is visually conveyed by the '>>' operator that connects the tasks.

As part of performance optimization and memory utilization, XComs (cross-communications) capabilities of Airflow is employed to pass the data across tasks. XCom is a mechanism that allows tasks to exchange messages or small amounts of data. However, due to its size limitation, using XCom to transfer large amounts of data was not plausible.

## How to setup and run

1. Clone the project from the Github repository.

```bash
git clone https://github.com/ValeriiZghurovskyi/EPAM-MLE-lab
```

2. Ensure Docker and Docker Compose are installed on your system.

3. Navigate to the `Module 4. Pipelines` folder:

```bash
cd 'Module 4. Pipelines'
```

4. Run the script to download the data files:

```bash
python3 data/data_download.py
```

5. Run the following commands on your terminal to setup required directories and environment variables:
```bash
mkdir -p ./logs ./plugins ./config
echo -e "AIRFLOW_UID=$(id -u)" > .env
echo -e "_PIP_ADDITIONAL_REQUIREMENTS=scikit-learn" >> .env
```

6. Start Airflow initialization:

```bash
docker compose up airflow-init
```

7. Start the Airflow application:

```bash
docker compose up
```

8. Open your favorite web browser and go to `localhost:8080`. Log in to the Airflow webserver with the username and password (airflow:airflow).

9. Switch on the `future_sales_data_preprocessing` dag and trigger it to run.

## Notes
The start date of the dag is set as current date. However, as the `schedule_interval` is set to `None`, this DAG will only be executed once when triggered manually, it won't perform any subsequent runs unless the DAG is triggered again. 

The tasks in this dag will take `sales_train.csv`, `items.csv`, `item_categories.csv`, and `shops.csv` from your linked data directory, process them and output the processed data back to the linked data directory. Make sure to link your local folder containing these data files to `/opt/airflow/data` in the docker.
