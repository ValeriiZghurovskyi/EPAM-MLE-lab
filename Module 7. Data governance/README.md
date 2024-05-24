# Data governance

## How to run my project:
1. Clone the repository:
```
git clone https://github.com/ValeriiZghurovskyi/EPAM-MLE-lab
```

2. Go to the `Module 7. Data governance` folder:
```
cd 'Module 7. Data governance'
```

3. Pull the data:
```
dvc pull data/train.csv
```
>You may need to authorize access to the storage at this point.

4. You can run the pipeline using next command:
```
dvc repro
```
This command will start the process of data cleaning, encoding, scaling, and training the model on this data.

If you have already launched this pipeline but need to launch it again, you can enter the following:
```
dvc repro --force
```

5. At the end of the training, you will have a model file and a .json file with metrics. You can also view metrics with the following command:
```
dvc metrics show
```

## How I made this project:

1. Initialize the DVC in the repository:

```
dvc init --subdir
```
>I used --subdir since we're in a subdirectory of the repository

2. Add a remote DVC repository to store our data:
```
dvc remote add -d myremote gdrive://<googledrive_folderID>
```

3. We have to move our data to the "Data" folder and enter the following command to add the data to the DVC:
```
dvc add data/train.csv
```

4. Now we can push our data to remote DVC storage:
```
dvc push
```

5. We can also push our changes to Git:
```
git add data/train.csv.dvc data/.gitignore
git commit -m "Start"
git push
```

6. Creating pipeline:
a. You need to move all the scripts for processing and training to the `src` folder.

b. Create dvc.yaml using next commands:

```
dvc stage add -n clean_data -d data/train.csv -d src/clean_data.py -o data/clean.csv python3 src/clean_data.py
```
```
dvc stage add -n encode_data -d data/clean.csv -d src/encoding.py -o data/encoded.csv python3 src/encoding.py
```
```
dvc stage add -n scale_data -d data/encoded.csv -d src/scaling.py -o data/processed.csv python3 src/scaling.py
```
```
dvc stage add -n train -d data/processed.csv -d src/train.py -o model.pkl --metrics-no-cache metrics.json python3 src/train.py
```

Now we can use `dvc repro` to start our pipeline.











