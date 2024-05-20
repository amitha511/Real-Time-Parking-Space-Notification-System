# Use Python image
FROM python:3.8-alpine

# Set working directory in the container
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY . .

ENTRYPOINT [ "python" ]

CMD ["main.py" ]
