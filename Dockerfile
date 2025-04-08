# Base image
FROM python:3.10-slim

# Working directory
WORKDIR /app

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
CMD ["uv", "run", "main:create_app", "--reload", "--host=0.0.0.0", "--port", "5000"]
