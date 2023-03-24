**Author: Szymon Gałecki**

### Intro
New integration is needed because of two reasons. 
- Firstly we are changing from SQLite3 file based database to PostgreSQL database that will run in docker container. 
- Secondly, because Django application uses data models and not the original schema from Flask app, it created its own database separate from API's database. We want to have a single database that will be accessed by both application and API. Compromise between two schemas was achieved and it's time to adjust few query's to the new shape of schema.

### Database service definition in docker-compose file
```
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
```

### Used connector - Psycopg 2.9.5
reference: https://www.psycopg.org/docs/

### Connect to database container from outside
```python
db = psycopg2.connect(
	database="postgres", 
	user="postgres", 
	password="postgres", 
	host="0.0.0.0",
	port="5432",
)
```

### Connect to database container from another container
```python
db = psycopg2.connect(
	database="postgres",
	user="postgres",
	password="postgres",
	host="DB-postgres",
	port="5432",
)
```

### Create tables in database (from outside)
```python
with psycopg2.connect(
	database="postgres", 
	user="postgres", 
	password="postgres", 
	host="0.0.0.0",
	port="5432",
) as db:
	with db.cursor() as cursor:
		with open("minitwit_schema.sql", "r") as f:
			cursor.execute(f.read())
```

### Drop all rows for tests and simulator
```python
def delete_all_rows() -> None:
	query = """
		DELETE FROM public.follower;
		DELETE FROM public.message;
		DELETE FROM public.user;		
		"""
	post_query(query, ())
```

### Tests and simulator
- All tests are passing
- All simulator requests seem to be serviced, no errors got printed out

### Add authentication
Authentication based on Authorization header sent by simulator with each request
```python
from FastAPI import Request

def authenticate_simulator(request: Request) -> None | HTTPException:
	if ( 
		"Authorization" not in request.headers or 
		request.headers["Authorization"] != "Basic c2ltdWxhdG9yOnN1cGVyX3NhZmUh"
	):
		raise HTTPException(
		status_code=403, detail="You are not authorized to use this resource!"
		)
```
