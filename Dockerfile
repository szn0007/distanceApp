# Use a lightweight Python image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Create and set the working directory
WORKDIR /app

# Copy the requirements file and install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Install Gunicorn explicitly
RUN pip install gunicorn==20.1.0

# Copy the Django project files
COPY . /app/

# Copy the secrets.json file
COPY secrets.json /app/secrets.json

# Command to run the application with Gunicorn and apply migrations
CMD ["sh", "-c", "python manage.py migrate && gunicorn --bind 0.0.0.0:8000 distanceApp.wsgi:application --workers 3"]
