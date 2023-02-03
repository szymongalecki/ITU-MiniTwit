FROM python:3.10-alpine

# Install any needed dependencies...
# RUN go get ...

# Set the working directory
WORKDIR /usr/src

RUN pip install --upgrade pip

COPY ./requirements.txt /usr/src

RUN pip install -r requirements.txt

COPY . /usr/src

# Make port 8080 available to the host
EXPOSE 8080

# Build and run the server when the container is started
CMD ["python", "minitwit.py"]
