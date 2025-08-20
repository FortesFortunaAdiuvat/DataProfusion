FROM python:3.13-slim

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port for the web service
EXPOSE 8000

# Run the gunicorn server
CMD ["gunicorn", "-b", "0.0.0.0:8000", "app:create_app()"]
