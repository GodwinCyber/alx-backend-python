# ==============================
# Dockerfile for Django API App
# ==============================

# Use officail Python base Image
FROM python:3.10

# Set working directory inisde container
WORKDIR /app

# Copy requirement.txt  first
COPY requirement.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirement.txt

# Copy all project files into the container
COPY . .

# Expose Django's default port
EXPOSE 8000

# Default command to run Django app
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]





