# Use a base image, Python 3.9 slim version
FROM python:3.9-slim

# Set build arguments for user ID and group ID
ARG USER_ID
ARG GROUP_ID

# Create a new group and user with specified IDs
RUN addgroup --gid $GROUP_ID user \
    && adduser --disabled-password --gecos '' --uid $USER_ID --gid $GROUP_ID user

# Switch to the newly created user
USER user

# Set the working directory in the container
WORKDIR /app

# Copy requirements.txt into the container
COPY requirements.txt .

# Install Python dependencies as the non-root user
RUN pip install -r requirements.txt

# Copy relevant directories and files into the container
COPY inference/ ./
COPY settings.json .
COPY data/ ./data/
COPY models/ ./models/

# Configure the container to run as an executable
ENTRYPOINT ["python", "inference.py"]

