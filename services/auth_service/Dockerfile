# Dockerfile for auth_service

# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Upgrade pip
RUN pip install --upgrade pip

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install Gunicorn
RUN pip install gunicorn


# Make ports available to the world outside this container
EXPOSE 8000 50051

# Define environment variable
ENV PYTHONUNBUFFERED=1

# Make it executable
RUN chmod +x /app/start.sh

# Use argument to set environment (default to dev)
ARG DJANGO_ENV=dev
ENV DJANGO_ENV=$DJANGO_ENV

# Command to start the appropriate environment
CMD ["/app/start.sh"]
