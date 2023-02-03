FROM python:3.10

# Install any needed dependencies...
# RUN go get ...

# Set the working directory
WORKDIR /usr/src

RUN pip install --upgrade pip

COPY ./requirements.txt /usr/src

RUN pip install -r requirements.txt
RUN apt-get install -y sqlite3

COPY . /usr/src

# Make port 8080 available to the host
EXPOSE 8080

# Build and run the server when the container is started
#CMD ["python3', 'mibnitwit.py']
CMD /bin/bash
