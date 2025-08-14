# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the contents of the directory app into the container at /app
COPY ./app /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Run app.py when the container launches
ENV PYTHONUNBUFFERED=1
CMD ["python", "-u", "/app/main.py"]