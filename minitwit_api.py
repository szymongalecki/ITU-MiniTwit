from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import PlainTextResponse
import sqlite3

"""
1. API uses the same database as minitwit.py
2. Find the equivalent of 'before_request' and 'after_request' - https://fastapi.tiangolo.com/tutorial/middleware/
3. How to map the response to JSON from plain list of values, is it necessary?
4. Investigate more the provided API
"""

app = FastAPI()
DATABASE = './minitwit.db'
LIMIT = 100

def connect_db():
    """Returns a new connection to the database."""
    return sqlite3.connect(DATABASE)

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

def JSON(response, fields):
    """Creates JSON response with given fields"""
    return [dict(zip(fields, r)) for r in response]

def single_value(response):
    """Returns single value from nonempty collection, otherwise None"""
    if response is None:
        return None
    else:
        return response[0][0]

def get_user_id(username: str):
    """Returns user_id if username exists in database."""
    query = """
            SELECT user_id 
            FROM user 
            WHERE username = ?
            """
    parameters = (username, )
    response = execute_query(query, parameters)
    return single_value(response)

@app.get("/", response_class=PlainTextResponse)
def default():
    return "HELLO FROM THE API\nAT LEAST, I CAN SAY THAT I'VE TRIED"

@app.get("/msgs")
def get_messages():
    """Returns the latest messages"""
    query = """
            SELECT message.text, message.pub_date, user.username 
            FROM message, user 
            WHERE message.flagged = 0 AND
            user.user_id = message.author_id
            ORDER BY message.pub_date DESC LIMIT ?
            """
    parameters = (LIMIT, )
    response = execute_query(query, parameters)
    if response is not None:
        return JSON(response, ["content", "pub_date", "user"])
    else:
        return []


@app.get("/msgs/{username}")
def get_user_messages(username: str):
    """Returns the latest messages of given user"""
    user_id = get_user_id(username)
    if user_id is None:
        raise HTTPException(status_code=404, detail="username not found")
    query = """
            SELECT message.text, message.pub_date, user.username 
            FROM message, user 
            WHERE message.flagged = 0 AND
            user.user_id = message.author_id AND user.user_id = ?
            ORDER BY message.pub_date DESC LIMIT ?
            """
    parameters = (user_id, LIMIT)
    response = execute_query(query, parameters)
    if response is not None:
        return JSON(response, ["content", "pub_date", "user"])
    else:
        return []

