# Base image
FROM python:3.10-slim-bookworm

# Working directory
WORKDIR /app

# Security patch
RUN apt-get update && apt-get upgrade -y && apt-get clean

# Install pip + uv
RUN pip install --upgrade pip uv

# Copy dependencies
COPY requirements.txt .
RUN uv pip install --system --requirement requirements.txt

# Copy project files
COPY . .

# Expose port
EXPOSE 5000

# Start app
CMD ["uv", "run", "--no-venv", "main:create_app", "--reload", "--host=0.0.0.0", "--port", "5000"]
