# Build image:      `docker build --tag minitwit/app .`
# Run container:    `docker run -p 8000:8000 minitwit/app`

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

# Minitwit application uses this port, but it has to be exposed when running
EXPOSE 8000

# Propagate changes in Django models to database schema 
RUN python manage.py migrate

# Build and run the server on port 8000 when the container is started
CMD ["sh", "-c", "DJANGO_SETTINGS_MODULE=ITU_MiniTwit.settings python manage.py runserver 0.0.0.0:8000"]