#!/bin/bash

# Define variables
IMAGE_NAME="comfort-dash:latest"
TAR_FILE="comfort-dash_latest.tar"
COMPRESSED_FILE="comfort-dash_latest.tar.gz"
CONTAINER_NAME="comfort-dash-container"
HOST_PORT=8100
CONTAINER_PORT=8100

# Check if Docker is installed
if ! command -v docker &> /dev/null
then
    echo "Docker is not installed. Please install Docker first."
    exit 1
fi

# Decompress the compressed file
if [ -f "$COMPRESSED_FILE" ]; then
    echo "Decompressing $COMPRESSED_FILE..."
    gzip -d $COMPRESSED_FILE
else
    echo "$COMPRESSED_FILE not found. Please ensure the file is correctly uploaded."
    exit 1
fi

# Import the Docker image
if [ -f "$TAR_FILE" ]; then
    echo "Importing Docker image..."
    docker load -i $TAR_FILE
    if [ $? -ne 0 ]; then
        echo "Failed to import Docker image."
        exit 1
    fi
else
    echo "$TAR_FILE not found. Please ensure decompression was successful."
    exit 1
fi

# Check if there is an existing container with the same name and remove it
if [ $(docker ps -a -q -f name=$CONTAINER_NAME) ]; then
    echo "A container with the same name exists, stopping and removing it..."
    docker stop $CONTAINER_NAME
    docker rm $CONTAINER_NAME
fi

# Run the new Docker container
echo "Running new Docker container..."
docker run -d -p $HOST_PORT:$CONTAINER_PORT --name $CONTAINER_NAME $IMAGE_NAME
if [ $? -eq 0 ]; then
    SERVER_IP=$(hostname -I | awk '{print $1}')
    echo "Container is running successfully. Access it at http://$SERVER_IP:$HOST_PORT"
else
    echo "Failed to run the Docker container."
    exit 1
fi
