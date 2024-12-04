#!/bin/bash

# Define service names in an array
services=("api_gateway" "auth_service" "product_service" "order_service" "payment_service" "notification_service")

# Root folder path
root_folder=~/Desktop/microcommerce

# Create the root directory
echo "Creating root folder: $root_folder"
mkdir -p "$root_folder"

# Navigate to the root folder
cd "$root_folder" || { echo "Failed to navigate to $root_folder"; exit 1; }

# Create directories and files for each service
for service in "${services[@]}"; do
    # Create each service directory
    echo "Creating service folder: $service"
    mkdir -p "$service"
    
    # Navigate into the service directory
    cd "$service" || { echo "Failed to navigate to $service"; exit 1; }
    
    # Create main app file
    echo "Creating main.py in $service"
    touch main.py
    
    # Create Dockerfile for each service
    echo "Creating Dockerfile in $service"
    cat <<EOF > Dockerfile
# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
EOF

    # Create requirements.txt file with FastAPI and Uvicorn
    echo "Creating requirements.txt in $service"
    echo -e "fastapi\nuvicorn\npymongo\n" > requirements.txt

    # Go back to root folder for the next service
    cd ..
done

# Create a Docker Compose file for all services
echo "Creating docker-compose.yml"
cat <<EOF > docker-compose.yml
version: '3'
services:
EOF

for service in "${services[@]}"; do
    echo "Adding $service to docker-compose.yml"
    cat <<EOF >> docker-compose.yml
  $service:
    build: ./$service
    ports:
      - "8000"
    depends_on:
      - mongodb
EOF
done

# Add MongoDB service to Docker Compose
echo "Adding MongoDB service to docker-compose.yml"
cat <<EOF >> docker-compose.yml
  mongodb:
    image: mongo
    ports:
      - "27017:27017"
EOF

echo "Setup complete! Check the $root_folder directory for service folders and docker-compose.yml"
