#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Run database migrations
echo "Running database migrations..."
python manage.py migrate

# Collect static files (optional, usually for production)
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Execute the CMD (what's specified in the Dockerfile or passed to `docker run`)
exec "$@"
