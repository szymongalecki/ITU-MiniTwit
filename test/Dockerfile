# Parent image from which we are building
FROM python:3.10-alpine

# Set the working directory
WORKDIR /usr/src

# Update Python package manager, PIP
RUN pip install --upgrade pip

# Copy Python code, requirements, assets and !!! sqlite3 database !!! to the working directory
COPY . /usr/src

# Install needed Python packages using PIP
RUN pip install -r requirements.txt

RUN pytest test.py

USER nonroot