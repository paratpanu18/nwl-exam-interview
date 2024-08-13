FROM ubuntu:20.04

# Set environment variables to avoid interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Update package list and install dependencies
RUN apt-get update && \
    apt-get install -y \
    wget \
    software-properties-common \
    gnupg

# Add the deadsnakes PPA which contains Python 3.12.0
RUN add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update && \
    apt-get install -y \
    python3.12 \
    python3.12-distutils \
    python3.12-venv

# Install pip for Python 3.12
RUN wget https://bootstrap.pypa.io/get-pip.py && \
    python3.12 get-pip.py && \
    rm get-pip.py

# Create a symlink to make python3 point to python3.12
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.12 1

COPY requirements.txt .

# Install any Python dependencies from requirements.txt if it exists
RUN if [ -f requirements.txt ]; then pip3.12 install -r requirements.txt; fi

# Copy everything from the current directory to the container's working directory
COPY . /nwl-interview-exam

# Set the working directory to /nwl-interview-exam
WORKDIR /nwl-interview-exam

# Expose port 6970
EXPOSE 6970

# Specify the command to run your Python script (adjust script name as needed)
CMD ["python3.12", "main.py"]