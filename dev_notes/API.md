**Author: Szymon Gałecki**
### What is API?
API, or application programming interface, is a set of defined rules that enable different applications to communicate with each other. It acts as an intermediary layer that processes data transfers between systems, letting companies open their application data and functionality to external third-party developers, business partners, and internal departments within their companies.

### Learn FastAPI basics
resources:
https://fastapi.tiangolo.com/
https://www.uvicorn.org/

process:
- Start with a 'hello world' project
- Setup a virtual environment to better track python dependencies for future integration with Docker
- Virtual environment was created but I can't activate it, "permission denied"
- Make "activate" executable
```sh
ls -l
-rw-r--r--  1 szymongalecki  staff  2187 Feb 19 18:42 activate

chmod +x activate

ls -l
-rwxr-xr-x  1 szymongalecki  staff  2187 Feb 19 18:42 activate
```
- New error "You must source this script: $ source ./v1/bin/activate"
```sh
. ./v1/bin/activate
```
- Explanation - "dot-source operator runs a script in the current scope so that any functions, aliases, and variables that the script creates are added to the current scope."

main packages:
1. **FastAPI** is a modern, fast (high-performance), web framework for building APIs with Python 3.7+ based on standard Python type hints.
2. **Uvicorn** - is an asynchronous server gateway interface web server implementation for Python.
3. **Typing** - This module provides runtime support for type hints. 

start application locally:
```sh
uvicorn minitwit_api:app --reload --port 8080
```

auto-generated API documentation:
http://127.0.0.1:8080/docs

### Map single feature of minitwit to API

```sh
# setup virtual environment
virtualenv venv_api
. ./venv_api/bin/activate

# install packages from requirements
pip install -r requirements.txt

# document all used packages
pip freeze > new_requirements.txt

```

- Can't query the database, not sure if I succesfully connected
- I was  connected but the path was wrong, I missed a forward slash in the front of the path 
- Now, the database is empty for some reason, I have no idea why as I didn't put it into docker...
- Replaced empty database with its original version from GitHub
- Opened both minitwit.py and mitwit_sim_api.py, database became empty
- Now just the minitwit_sim_api.py, it cause the database to become empty, why?

```python
# Why would you put something like that into API code???
os.system(f"rm {DATABASE}")
init_db()
```

```
Exemplary desired output for: @app.get("/msgs/{username}")

http://172.16.170.160:5001/msgs/Kerry%20Passer

[
  {
    "content": "\u201cIt will not be made out of sight over the side; more fell for that time, and that for you,\u2019 said he, leaning back in Baker Street.", 
    "pub_date": 1233065869, 
    "user": "Kerry Passer"
  }, 
  {
    "content": "My groom and the bright spring sunshine.", 
    "pub_date": 1233065864, 
    "user": "Kerry Passer"
  },
  .
  .
  .
]
```

### Find and kill process on given port
```bash
# Find
sudo lsof -i :<PORT>

# Kill
kill -9 <PID>
```

### New approach
- Enpoints use two general functions: 

**Function for executing query in a single database connection, return response**
```python
def execute_query(query, parameters):
	"""Executes query with provided parameters, fetches all results"""
	response = None
	try:
		connection = sqlite3.connect(DATABASE)
		try:
			cursor = connection.cursor()
			response = cursor.execute(query, parameters).fetchall()
			cursor.close()
			connection.close()
			if response == []:
				response = None
		except Exception as e:
			print(f"FAILED TO EXECUTE QUERY: {e}")
	
	except Exception as e:
		print(f"FAILED TO CONNECT TO DATABASE: {e}", )
	finally:
		return response
```

**Function for parsing response to JSON with provided list of fields**
```python
def JSON(response, fields):
	"""Creates JSON response with given fields"""
	return [dict(zip(fields, r)) for r in response]
```

- Universal JSON parser wasn't good enough, changed to local formatting in respective endpoint functions
- TLDR - it didn't work as nicely as I expected

### Mapped endpoints 
- @app.get("/msgs")
- @app.get("/msgs/{username}")

### Mapping - @app.get("/fllws/{username}") 
```
Exemplary desired output for: @app.get("/fllws/{username}") 

http://10.26.44.25:5050/fllws/Kerry%20Passer

{
  "follows": [
    "Octavio Wagganer", 
    "Mellie Yost", 
    "Nathan Sirmon"
  ]
}
```
- Returned content is ok
- Update LATEST value as it is checked by the simulator test

### Mapping POST endpoints
- POST requests opposed to GET requests can't be triggered by simple URL
- Some parameters of the POST request are in the URL like 'latest' and 'no' but the rest is in the payload
- To easily trigger, understand and test POST enpoints, use FastAPI automatically generated automatic /docs
- Status code 204 https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/204
- While there are many status codes it's useful to know their groups
	1.  Informational responses (`100` – `199`)
	2.  Successful responses (`200` – `299`)
	3.  Redirection messages(`300` – `399`)
	4.  Client error responses(`400` – `499`)
	5.  Server error responses (`500` – `599`)

### Testing
- Tests for the API were not independent so to test all of them it was best to go from the first to the last one
- Run a single test `pytest minitwit_sim_api_test.py::test_latest`
- All the changes made by test are committed so test that will pass on the first try may fail on the second, as the changes that they are trying to make were already done. Take for example registering the same user twice.

### Typing
- I used the fact that typing in Python is now widely supported to document the returned types in the code
- It is easy to see where the functions use custom data model which verifies the types and where the returned data is simply a dictionary satisfying JSON format

### Security
- Well, no security. Anyone can query our API. 