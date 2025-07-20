# Dockerfile

# 1. Use an official, lightweight Python image as our base.
FROM python:3.11-slim

# 2. Set the working directory inside the container.
WORKDIR /app

# 3. Set environment variables for Python best practices in Docker.
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 4. Copy only the requirements file first for build caching.
COPY requirements.txt .

# 5. Install all the Python dependencies.
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copy the rest of your application's source code into the container.
COPY . .

# We don't specify a command to run here because Docker Compose will
# provide different commands for our api and worker services.