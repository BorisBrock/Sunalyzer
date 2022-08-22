FROM python:3.10.6-slim-bullseye

# Resolve all Python requirements
COPY requirements.txt .
RUN pip install -r requirements.txt && rm requirements.txt

# Copy all required data to the container
COPY backend backend
COPY site site

# Make sure the main startup script is available and runnable
COPY run.sh .
RUN chmod a+x run.sh

# Create and expose data folder in the container
VOLUME ["/data"]

# Expose port 5000 for the webserver
EXPOSE 5000

# Fixes an issue with Python prints being swallowed
ENV PYTHONUNBUFFERED=1

# Main entry point of the container
ENTRYPOINT ["./run.sh"]