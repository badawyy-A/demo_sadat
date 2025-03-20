# Use a lightweight Python image
FROM python:3.9

# Set the working directory inside the container
WORKDIR /app


# Copy requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install missing dependencies for OpenCV
RUN apt-get update && apt-get install -y libgl1-mesa-glx && rm -rf /var/lib/apt/lists/*

# Copy application code
COPY . .

# Expose the FastAPI port
EXPOSE 5002

# Run the FastAPI app
CMD ["python", "app.py"]