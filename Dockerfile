FROM python:3.10-alpine

# Set the working directory
WORKDIR /usr/src

RUN pip install --upgrade pip

# Copy the requirements file into the container
COPY ./requirements.txt /usr/src

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Copy the current directory contents into the container at /usr/src
COPY . /usr/src

# Set environment variables for MySQL connection
ENV PYTHONUNBUFFERED 1

# Install the MySQL client and configure the Django app to use MySQL
# Install dependencies
RUN apk update && \
    apk add build-base mariadb-connector-c-dev && \
    pip install mysqlclient
