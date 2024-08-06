FROM ubuntu:20.04

# Set environment variables to avoid interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Update package list and install dependencies
RUN apt-get update && \
    apt-get install -y \
    wget \
    gnupg \
    python3 \
    python3-pip \
    mongodb

# Copy everything from the current directory to the container's working directory
COPY . /nwl-interview-exam

# Set the working directory to /app
WORKDIR /nwl-interview-exam

# Install any Python dependencies from requirements.txt if it exists
RUN if [ -f requirements.txt ]; then pip3 install -r requirements.txt; fi

# Expose port 6970
EXPOSE 6970

# Specify the command to run your Python script (adjust script name as needed)
CMD ["python3", "main.py"]