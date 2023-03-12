FROM python:3.10-alpine

# Install any needed dependencies...
# RUN go get ...

# Set the working directory
WORKDIR /usr/src

RUN pip install --upgrade pip

COPY ./requirements.txt /usr/src

RUN pip install -r requirements.txt

COPY ./ITU_MiniTwit /usr/src

# Make port 8080 available to the host
EXPOSE 8000

RUN python manage.py migrate

# Build and run the server when the container is started
CMD ["sh", "-c", "DJANGO_SETTINGS_MODULE=ITU_MiniTwit.settings python manage.py runserver 0.0.0.0:8000"]

