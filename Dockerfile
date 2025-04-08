# Base image
FROM python:3.10-slim

# Set working directory
WORKDIR /

# Install pip + uv
RUN pip install --upgrade pip uv

# Copy requirements and install
COPY requirements.txt .
RUN uv pip install --system --requirements requirements.txt

# Copy all project files
COPY . .

# Expose port
EXPOSE 5000

# Run app
CMD ["uv", "run", "main:create_app", "--reload", "--host=0.0.0.0", "--port", "5000"]
