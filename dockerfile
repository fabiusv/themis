# Use the official Python image as a base
FROM python:3.9

# Set the working directory inside the container
WORKDIR /app

# Copy the content of the local src directory to the working directory
COPY src/ .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 80
EXPOSE 80

# Run uvicorn command
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80", "--reload"]
