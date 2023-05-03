# Use an official Python runtime as a parent image
FROM python:3.11-slim-buster

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Set the entrypoint to run the app.py script
ENTRYPOINT ["python", "server.py"]
