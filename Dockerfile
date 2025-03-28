# Base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy project files
COPY . /app

# Install UV Astral
RUN pip install uv

# Create virtual environment
RUN python -m venv .venv

# Activate venv and install dependencies
RUN .venv/bin/python -m pip install --upgrade pip
RUN uv pip install --requirements requirements.txt

# Expose port 5000
EXPOSE 5000

# Command to run the app
CMD ["uv", "run", "main:app", "--host=0.0.0.0", "--port=5000"]
