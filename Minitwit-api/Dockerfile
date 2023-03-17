# Build image:      `docker build --tag minitwit/api .`
# Run container:    `docker run --rm -p 8080:8080 minitwit/api`

# Parent image from which we are building
FROM python:3.10-alpine

# Set the working directory
WORKDIR /usr/src

# Update Python package manager, PIP
RUN pip install --upgrade pip

# Copy Python code, requirements, !!! schema and db !!! to the working directory
COPY . /usr/src

# Install needed Python packages using PIP
RUN pip install -r requirements.txt

# Minitwit API uses this port, but it has to be exposed when running container
EXPOSE 8080

# Run the API when the container is started, on port 8080, defined in minitwit_api.py
CMD ["sh", "-c", "python minitwit_api.py"]