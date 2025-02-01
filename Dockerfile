# Use a lightweight Python image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy only requirements first to leverage Docker's build cache
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files
COPY . /app

# Create a directory for configuration files
RUN mkdir -p /root/.movie_recommendation

# Copy configuration files (if they exist in the project root)
COPY config.toml /root/.movie_recommendation/config.toml
COPY credentials.toml /root/.movie_recommendation/credentials.toml

# Expose port 80 (default for HTTP)
EXPOSE 80

# Start the application
CMD ["python", "app.py"]