# Use an official Python image as the base image
FROM python:3.10

# Set the working directory to /app
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install the dependencies
RUN pip install -r requirements.txt

# Copy the Python program
COPY videosummary.py .
COPY videosummary.py app

RUN chmod +x videosummary.py

# Run the Python program when the container starts
CMD ["python", "videosummary.py", "$1", "$2", "$3"]
