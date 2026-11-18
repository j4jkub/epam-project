FROM python:3.12-slim
# Set the working directory to /app
WORKDIR /app
# Copy the requirements file to the container
COPY requirements.txt /app/
# Install the required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY . /app/backend
ENV PYTHONPATH=/app

RUN mkdir -p /app/uploads
# Expose port 8000 to communicate with the host
EXPOSE 8000

# Command to run the Django server
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]