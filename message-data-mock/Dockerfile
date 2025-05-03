# Use an official Python base image
FROM python:3.11-slim

# Set working directory inside the container
WORKDIR /app

# Copy requirement file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Flask app into the container
COPY message_mock.py .

# Expose the port Flask runs on
EXPOSE 9999

# Run the Flask app
CMD ["python", "message_mock.py"]