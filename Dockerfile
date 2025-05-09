# Use the official Python image as the base
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Install PostgreSQL development libraries
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    gcc && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Django project files
COPY . .

# Set environment variables for Django superuser
ENV DJANGO_SUPERUSER_USERNAME=admin \
    DJANGO_SUPERUSER_PASSWORD=1234 \
    DJANGO_SUPERUSER_EMAIL=admin@gmail.com

# Expose port 8000 for the application
EXPOSE 8000

# Run database migrations and create superuser
RUN python manage.py migrate && \
    python manage.py createsuperuser --noinput || true

# Run the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
