# Use an official Python runtime as a parent image
FROM python:3.10

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
COPY requirements.txt .

RUN --mount=type=cache,target=/root/.cache/pip pip install -r requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Copy the entrypoint script into the container
COPY entrypoint.sh /app

# Grant execute permissions to the script
RUN chmod +x /app/entrypoint.sh

# Run the entrypoint script
CMD ["/app/entrypoint.sh"]


