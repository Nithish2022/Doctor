# Use the official Python image.
FROM python:3.9-slim

# Install wkhtmltopdf and other dependencies.
RUN apt-get update && apt-get install -y \
    wkhtmltopdf \
    tesseract-ocr \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies.
COPY requirements.txt /app/
WORKDIR /app
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code.
COPY . /app

# Set environment variables.
ENV TESSERACT_CMD=/usr/bin/tesseract
ENV WKHTMLTOPDF_CMD=/usr/bin/wkhtmltopdf

# Expose the port and define the command to run the app.
EXPOSE 5000
CMD ["python", "app.py"]
