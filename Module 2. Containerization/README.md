## Cloning the Repository
First, clone the repository from GitHub using the following command:
```bash
git clone https://github.com/ValeriiZghurovskyi/EPAM-MLE-lab
```

## Data and Models Loading
1. Navigate to the `EPAM-MLE-lab` folder:
```bash
cd EPAM-MLE-lab
```

2. Navigate to the `Module 2. Containerization` folder:
```bash
Module 2. Containerization
```

3. Run the script to download the model and test files:
```bash
python3 data_download/data_download.py
```

## Building Docker Image
1. Ensure your user has the necessary permissions to use Docker:
```bash
groups $USER
```
Make sure your user belongs to the "docker" group. If not, add your user to the group:
```bash
sudo usermod -aG docker $USER
```
Then, restart Docker:
```bash
sudo service docker restart
```

2. Configure the settings file:
   - General: Specify the directories' names where the models, data, and results are stored.
   - Inference: Specify the model and data file names.

3. Build the Docker image, replacing `<image_name>` with the desired name for your image:
```bash
docker build -t <image_name> --build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g) -f inference/Dockerfile .
```

4. Create a directory to store the results:
```bash
mkdir results
```

5. Run the container:
```bash
docker run -it <image_name>
```
Replace `<image_name>` with the name of your Docker image.

To retrieve the results on your local machine:
- Find the ID of the container:
```bash
docker ps -a
```
- Copy the result file from the container to your local machine:
```bash
docker cp <container_id>:/app/results/inference_results.csv ./results/
```
Alternatively, you can run the container with a volume mounted for the results directory:
```bash
docker run -v "${PWD}/results:/app/results" <image_name>
```
Replace `<container_id>` with the container's ID and `<image_name>` with the Docker image's name.

Make sure to replace placeholders like `<image_name>` and `<container_id>` with the appropriate values.
