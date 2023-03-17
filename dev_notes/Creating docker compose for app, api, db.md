**Author: Szymon Gałecki**

### What is the difference between Dockerfile and docker-compose.yaml?
The contents of a Dockerfile describe how to create and build a Docker image, while docker-compose is a command that runs Docker containers based on settings described in a docker-compose.yaml file.

### Understand the structure of Dockerfile by commenting existing one.
resource:
- https://docs.docker.com/engine/reference/builder/

This is a commented Dockerfile for Minitwit Django Application:
```dockerfile
# Build image: `docker build --tag minitwit/app .`
# Run container: `docker run --rm -p 8000:8000 minitwit/app`

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

# Minitwit application uses this port, but it has to be exposed when running container
EXPOSE 8000

# Propagate changes in Django models to database schema
RUN python manage.py migrate

# Build and run the application on port 8000 when the container is started
CMD ["sh", "-c", "DJANGO_SETTINGS_MODULE=ITU_MiniTwit.settings python manage.py runserver 0.0.0.0:8000"]
```

### Minitwit App and API have their Dockerfiles ready, time for db.
resources:
- https://vsupalov.com/database-in-docker/
- https://docs.docker.com/storage/volumes/

"If you’re working on a small project, and are deploying to a single machine, it’s completely okay to run your database in a Docker container.
**Be sure to mount a volume to make the data persistent**, and have backup processes in place. Try to restore them every once in a while to make sure your backups are any good."

"Here’s a pretty bad anti-pattern, which can cause you a lot of trouble, even if you’re just working on a small project. **You should not run stateful applications in orchestration tools which are built for stateless apps.**"


### Difference between the RUN and CMD command in Dockerfile
resource:
- https://stackoverflow.com/questions/37461868/difference-between-run-and-cmd-in-a-dockerfile

**RUN** is an image build step, the state of the container after a **RUN** command will be committed to the container image. A Dockerfile can have many **RUN** steps that layer on top of one another to build the image.

**CMD** is the command the container executes by default when you launch the built image. A Dockerfile will only use the final **CMD** defined. The **CMD** can be overridden when starting a container with `docker run $image $other_command`.

### SQLite getting started tutorial
resource:
https://www.sqlite.org/cli.html

### Docker image is built correctly but container terminates just after launching...
"The main process inside the container has ended successfully": This is the most common reason for a Docker container to stop! When the process running inside your container ends, the container will exit.

If you’re running a container with a shell (like `bash`) as the default command, then the container will exit immediately if you haven’t attached an interactive terminal. If there’s no terminal attached, then your shell process will exit, and so the container will exit. You can stop this by adding `--interactive --tty` (or just `-it`) to your `docker run ...` command, which will let you type commands into the shell.

### How to check if the database content was read?
Once container is run `docker run -it minitwit/db`, sqlite interactive terminal is launched. Execute a select statement on one of the tables to check content, for example:
`sqlite> select * from user`, you should see similar output:
```sqlite
1|Roger Histand|Roger+Histand@hotmail.com|pbkdf2:sha256:50000$27tb2qgX$64cd47b7cbd27b0f27f170a26e0e434ae24a310cf2e4704f075fcc9f48339c8e
2|Geoffrey Stieff|Geoffrey.Stieff@gmail.com|pbkdf2:sha256:50000$ZKEH4LvN$c16172a5a217c2410d410daf558ffaa2fecb088bae29913277f75151f4719e27
3|Wendell Ballan|Wendell-Ballan@gmail.com|pbkdf2:sha256:50000$QvV3EqQX$6dad4d42045b6542b6b0d888f7c6e679e77495451ee9fe1c96763ee8f2f82970
...
```

### Surprise in docker-compose
If you specify both an `image` and `build` and image of that name does not exist, it will be created from Dockerfile located in build directory, under the name specified in image. 

However if you try to create an image which exists under that name in the DockerHub, build will be ignored and Dockerfile in that location will not be used. Instead image of that name will be pulled from DockerHub.

I discovered it after seeing that api runs on port 5000, which was not used in our project. When I checked images in docker desktop I noticed that api image was 2 years old, which seemed odd. Later I realised that this is not our image, but group which did the same course two years ago.

### Why initial idea will not work?
I wanted to host a separate container for app, api and db. Db container has a mounted volume and api and db container communicate with it to access database. 

At this point we were still using SQLite3 for database. The thing that I didn't realise is that I can't easily access raw content of another container even though they share a network. Even if I could, I would have two containers trying to access a single file which would end up in concurrent access to a single file. SQLite3 is based on file access and doesn't use any explicit port for communication.  
I have to choose another DBMS, preferably with official docker image and migrate data. 

### Test Mongo 

Just Mongo database
```bash
# Pull and run mongo image
docker run -d -p 27017:27017 mongo

# Show running containers
docker ps

" CONTAINER ID   IMAGE    PORTS                      NAMES
" 5dec3105ccb1   mongo    0.0.0.0:27017->27017/tcp   frosty_williamson

# Connect to the container and launch mongo shell 
# mongo shell reference: https://www.mongodb.com/docs/v4.4/mongo/
docker exec -it frosty_williamson mongosh

```

Mongo database and mongo-express interface 
```
# Use root/example as user/password credentials
version: '3.1'
services:
	mongo:
		image: mongo
		restart: always
		environment:
			MONGO_INITDB_ROOT_USERNAME: root
			MONGO_INITDB_ROOT_PASSWORD: example

	mongo-express:
		image: mongo-express
		restart: always
		ports:
			- 8081:8081
		environment:
			ME_CONFIG_MONGODB_ADMINUSERNAME: root
			ME_CONFIG_MONGODB_ADMINPASSWORD: example
			ME_CONFIG_MONGODB_URL: mongodb://root:example@mongo:27017/
```

Create database, table and entry. Check if it appears in mongo-express.
```bash
docker exec -it DB mongosh

# create database
test> use example
switched to db example

# create table
example> db.createCollection("example1")
{ ok: 1 }

# insert entry
example> db.example1.insertOne({user:"Szymon", age: 26})
{
  acknowledged: true,
  insertedId: ObjectId("6412340526da59da6b4b8c69")
}

# retrieve entry
example> db.example1.find()
[
  {
    _id: ObjectId("6412340526da59da6b4b8c69"),
    user: 'Szymon',
    age: 26
  }

```


It appears in the mongo-express.
![](https://raw.githubusercontent.com/szymongalecki/ITU-MiniTwit/composing/dev_notes/mongo-express.png)
### Postgres is added as an alternative to Mongo

To access Postgres through interface use Adminer on port :8082.
![](https://raw.githubusercontent.com/szymongalecki/ITU-MiniTwit/composing/dev_notes/postgres_credentials.png)

### Final docker compose with two DBMS containers and interfaces, Django Application and FastAPI API

```
# Passwords are explicit, for tests only, do not use for production :)
version: '3'
services:
	mongo:
		image: mongo
		container_name: DB-mongo
		restart: always
		volumes:
			- mongo_volume:/data/db
		environment:
			MONGO_INITDB_ROOT_USERNAME: root
			MONGO_INITDB_ROOT_PASSWORD: pass
		ports:
			- 27017:27017
	
	mongo-express:
		image: mongo-express
		container_name: DB-mongo-interface
		depends_on:
			- mongo
		restart: always
		environment:
			ME_CONFIG_MONGODB_ADMINUSERNAME: root
			ME_CONFIG_MONGODB_ADMINPASSWORD: pass
			ME_CONFIG_MONGODB_URL: mongodb://root:pass@mongo:27017/
		ports:
			- 8081:8081
		
	postgres:
		image: postgres
		container_name: DB-postgres
		restart: always
		volumes:
			- postgres_volume:/var/lib/postgresql/data
		environment:
			- POSTGRES_DB=postgres
			- POSTGRES_USER=postgres
			- POSTGRES_PASSWORD=postgres
		ports:
			- 5432:5432
	
	adminer:
		image: adminer
		container_name: DB-postgres-interface
		restart: always
		ports:
			- 8082:8080

	api:		
		build: ./Minitwit-api
		container_name: API
		depends_on:
			- mongo
			- postgres
		ports:
			- 8080:8080
	
	app:
		build: ./ITU_MiniTwit
		container_name: APP
		depends_on:
			- mongo
			- postgres
		ports:
			- 8000:8000

volumes:
	mongo_volume:
	postgres_volume:
```

### Run

```bash
# 6 containers will be run, so you probably want to run a detached mode
docker-compose up -d

# Stop and remove all containers
docker-compose down
```

### Future changes

1. After deciding on DBMS solution one of the two pairs of services will be removed:
	1. Mongo / Mongo-express
	2. Postgres / Adminer
2. Integration with application and API
3. Use GitHub secrets for hardcoded passwords in the docker-compose file after everything is tested but before deployment
