# Parent image from which we are building
FROM python:3.10-alpine

# Set the working directory
WORKDIR /usr/src

# Update Python package manager, PIP
RUN pip install --upgrade pip

# Copy list of needed Python packages to the working directory
# !!! Currently requirements.txt and this Dockerfile are outside of ITU_MiniTwit directory !!!
COPY ./requirements.txt /usr/src

# Install needed Python packages using PIP
RUN pip install -r requirements.txt

# Copy Python code, assets and !!! sqlite3 database !!!
COPY ./ITU_MiniTwit /usr/src

# Minitwit application uses this port, but it has to be exposed when running:
# `docker run -p 8000:8000 <image name>`
EXPOSE 8000

# Propagate changes in Django models to database schema 
RUN python manage.py migrate

# Build and run the server on port 8000 when the container is started
CMD ["sh", "-c", "DJANGO_SETTINGS_MODULE=ITU_MiniTwit.settings python manage.py runserver 0.0.0.0:8000"]