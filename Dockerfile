# Base image
FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Copy requirements.txt to the container
COPY requirements.txt .

# Install system dependencies for google-crc32c C extension
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the rest of your application code to the container
COPY . .

# Command to run the app
CMD ["streamlit", "run", "app.py"]