# Build image:      `docker build --tag minitwit/db .`
# Run container:    `docker run --rm minitwit/db`

# Parent image, ref - https://hub.docker.com/_/alpine
FROM ubuntu:latest

# Set the working directory
WORKDIR /usr/src

# Update apt repository cache, update apt-cache, install SQLite3
RUN apt-get -y update                               && \
    apt-get -y upgrade                              && \
    apt-get install -y sqlite3 libsqlite3-dev

# Copy db file 
COPY minitwit.db /usr/src

# Read db file
RUN sqlite3 /usr/src/minitwit.db

# Current issues
# 1. Don't know if the db content was read correctly and if I should include schema.
# 2. Don't know why the container closes after launching altough image was built correctly.
#   Probably there is no defined entrypoint and it seems like everything is done after reading db.
