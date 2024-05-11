# How to setup and run

1. Clone the project from the Github repository.

```bash
git clone https://github.com/ValeriiZghurovskyi/EPAM-MLE-lab
```

2. Navigate to the `Module 5. Model deployment` folder:

```bash
cd 'Module 5. Model deployment'
```

## Online Prediction 

We will use Docker to build and run the application for online predictions. 

1. Build the Docker image for the online prediction:

```bash
docker build -t online-prediction -f app/online/Dockerfile .
```

2. Once built, you can start the prediction API server using:

```bash
docker run -d -p 8000:5000 --name prediction-app online-prediction
```

3. You can check the logs with:

```bash
docker logs <container_id>
```

4. The REST API endpoint will listen for POST requests at http://localhost:8000/predict. You can test it using curl:

```bash
curl -X POST -H "Content-Type: application/json" -d '{"features":[5,3.5,1.2,4.5]}' http://localhost:8000/predict
```

5. To make sure that our REST endpoint is stable and response time is manageable (<< 1 sec), we can use the following command:

```bash
curl -o /dev/null -s -w %{time_total} -X POST -H "Content-Type: application/json" -d '{"features":[5,3.5,1.2,4.5]}' http://localhost:8000/predict
```
I have result time: 0.006805

6. To stop and remove the application, you can use:

```bash
docker stop prediction-app
docker rm <container_id>
```

It's important to note that if you try to visit 'http://localhost:8000/predict' in a browser, you will see an error message since browsers send a GET request by default, and our API is waiting for a POST request.

## Batch Prediction 

For the batch prediction, we use a python script that is scheduled to run with cron. 

1. The following command will run script predict.py every hour. 

```bash
(crontab -l; echo "0 * * * * /usr/bin/python3 <abs_path_to_script> >> <abs_path_to_log.txt> 2>&1") | crontab -
```

<abs_path_script> - Absolute path to the file with the script in the app/batch/predict.py folder

<abs_path_script> - Absolute path to the file where our prediction logs will be stored.

In my case, the command looked like this:

```bash
(crontab -l; echo "* * * * * /usr/bin/python3 /home/valerii/Desktop/EPAM-MLE-lab/Module\ 5.\ Model\ deployment/app/batch/predict.py >> /home/valerii/Desktop/EPAM-MLE-lab/Module\ 5.\ Model\ deployment/app/files/log.txt 2>&1") | crontab -
```
If the batch prediction is successful, you will see the following lines in the log.txt file to which you specified the path:

2024-05-11 23:00:11.086485 - Prediction completed. Output file: /home/valerii/Desktop/EPAM-MLE-lab/Module\ 5.\ Model\ deployment/app/files/iris_result.py

2. To stop the cron job, you need to delete the corresponding task from the crontab file. You can edit the crontab file by running the crontab -e command in your terminal. Then simply delete your task line and save your changes.:

```bash
crontab -e
```

## Testing

We use Pytest for testing our application. You can run the tests with the following command:

```bash
pytest app/tests/tests.py
```

If the tests pass successfuly, you will see the following lines:

============================= 3 passed in 1.62s ==============================


Make sure that pytest is installed in your environment, otherwise you can install it with pip:

```bash
pip install pytest
```

## Installation of the Package

The python package of this project can be installed using the following command:

```bash
pip install .
```

This allows you to import the modules in your scripts with `import app.online`, `import app.batch`


### Publishing On PyPI
The setup.py script is also our main entrypoint to register the package name on PyPI and upload source distributions.

To “register” the package (this will reserve the name, upload package metadata, and create the pypi.python.org webpage):

```bash
python setup.py register
```

If you haven’t published things on PyPI before, you’ll need to create an account.