# Use a Python image (slim: lighter but compatible with all libraries, unlike alpine)
FROM python:3.13-slim

LABEL app="Graph3Count"
LABEL version="v1"

# Define the working directory in the container
WORKDIR /app

# Copy the application files into the container
COPY /app /app

# Install the Python dependencies (--no-cache-dir prevents the cache from being used)
RUN pip install --no-cache-dir -r requirements.txt

# Expose a port (not mandatory, only for guidance)
EXPOSE 8080

# Start the Python server when the container starts in the background
CMD sh -c "python -m http.server 8080 --bind 0.0.0.0 & sleep infinity"
# Note: the command is executed at the /app level so anything outside of /app would not be accessible with the Python server.