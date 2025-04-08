# Base image
FROM python:3.10-slim-bookworm

# Working directory
WORKDIR /app

# Install pip & uv
RUN apt-get update && apt-get upgrade -y && apt-get install -y gcc && apt-get clean
RUN pip install --upgrade pip uv

# Copy dependencies
COPY requirements.txt .

# Install deps
RUN uv pip install --system --requirement requirements.txt

# Copy all project files
COPY . .

# Expose the Flask port
EXPOSE 5000

# Run the app via Python directly (safe & stable)
CMD ["python", "main.py"]
