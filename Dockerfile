# Use the official Python 3.12 slim base image
FROM python:3.12-slim

# Set environment variables to prevent Python from creating `.pyc` files and to enable unbuffered output
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Copy `requirements.txt` and install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy project code into the container
COPY . .

# Expose the port on which the application will run (modify according to your app's needs)
EXPOSE 8100

# Set the startup command
CMD ["python", "app.py"]