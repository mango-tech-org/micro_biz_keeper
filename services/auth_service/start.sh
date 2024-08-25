#!/bin/bash

# Start the gRPC server in the background and log the start
echo "Starting gRPC server..."
python auth_service/grpc_server.py &
GRPC_SERVER_PID=$!

# Check the environment and start the appropriate Django server
if [ "$DJANGO_ENV" = "dev" ]; then
    echo "Starting Django development server with Gunicorn..."
    gunicorn --workers 3 --bind 0.0.0.0:8000 --reload --env DJANGO_SETTINGS_MODULE=auth_service.settings auth_service.wsgi:application &
    DJANGO_SERVER_PID=$!
    echo "Django development server (Gunicorn) started with PID $DJANGO_SERVER_PID"
else
    echo "Starting Django production server with Gunicorn..."
    gunicorn --workers 3 --bind 0.0.0.0:8000 --env DJANGO_SETTINGS_MODULE=auth_service.settings auth_service.wsgi:application &
    DJANGO_SERVER_PID=$!
    echo "Django production server (Gunicorn) started with PID $DJANGO_SERVER_PID"
fi

# Function to gracefully shut down both servers
shutdown_servers() {
    echo "Shutting down Django server..."
    kill $DJANGO_SERVER_PID
    echo "Shutting down gRPC server..."
    kill $GRPC_SERVER_PID
}

# Trap signals to ensure both servers are shut down properly
trap shutdown_servers SIGTERM SIGINT

# Wait for the Django server to finish (this will block the script)
wait $DJANGO_SERVER_PID
