# Build image:      
#   `docker build --tag minitwit/db .`

# Run container and access sqlite termninal:    
#   `docker run -it --name dbtest --mount source=db_volume,target=/db  minitwit/db `

# Run container in a detached state and launch bash to inspect container:
#   `docker run -itd --name dbtest --mount source=db_volume,target=/db  minitwit/db`
#   `docker exec -it dbtest bash`         

# Parent image
FROM ubuntu:latest

# Set the working directory
WORKDIR /db

# Update apt repository cache, update apt-cache, install SQLite3
RUN apt-get -y update                               && \
    apt-get -y upgrade                              && \
    apt-get install -y sqlite3 libsqlite3-dev

# Copy db file 
COPY minitwit.db /db

# Every time the container is launched create a dump file of initial state and
# open minitwit database
CMD sqlite3 minitwit.db .dump > initial_state_dump.sql; \
    sqlite3 minitwit.db
