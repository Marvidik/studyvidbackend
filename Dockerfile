# Use the official Python image from the Docker Hub
FROM python:3.10-slim

# Set environment variables to avoid pyc files and enable buffered output
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set a working directory inside the container
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt /app/

# Install the dependencies listed in requirements.txt
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy the entrypoint.sh script and grant execution permissions
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Copy the entire project code into the container
COPY . /app/

# Expose port 8000 (Django default)
EXPOSE 8000

# Run the entrypoint script
ENTRYPOINT ["/app/entrypoint.sh"]

# Default command to run Django's development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]



