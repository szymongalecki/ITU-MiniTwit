import time
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import PlainTextResponse
import sqlite3
from pydantic import BaseModel
from typing import Dict, Tuple, List


"""
1. API uses the same database as minitwit.py
2. Find the equivalent of 'before_request' and 'after_request' - https://fastapi.tiangolo.com/tutorial/middleware/
3. How to map the response to JSON from plain list of values, is it necessary?
4. Investigate more the provided API
5. What is represented by LATEST?
6. How to authenticate minitwit_sim_api_test.py?
"""

app = FastAPI()
DATABASE = "./minitwit.db"
LIMIT = 100
LATEST = 0

"""
DATA MODELS DATA MODELS DATA MODELS DATA MODELS DATA MODELS DATA MODELS DATA MODELS DATA MODELS DATA MODELS
"""


class Message(BaseModel):
    content: str


class User(BaseModel):
    username: str
    email: str
    pwd: str


"""
HELPER FUNCTIONS HELPER FUNCTIONS HELPER FUNCTIONS HELPER FUNCTIONS HELPER FUNCTIONS HELPER FUNCTIONS
"""


def update_latest(latest: int):
    global LATEST
    LATEST = latest if latest != -1 else LATEST


def connect_db():
    """Returns a new connection to the database."""
    return sqlite3.connect(DATABASE)


def execute_query(query: str, parameters: Tuple):
    """Executes query with provided parameters, fetches all results, commits changes"""
    response = None
    try:
        connection = sqlite3.connect(DATABASE)
        try:
            cursor = connection.cursor()
            response = cursor.execute(query, parameters).fetchall()
            cursor.close()
            connection.commit()
            connection.close()
            if response == []:
                response = None
        except Exception as e:
            print(f"FAILED TO EXECUTE QUERY: {e}")
    except Exception as e:
        print(
            f"FAILED TO CONNECT TO DATABASE: {e}",
        )
    finally:
        return response


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
    parameters = (username,)
    response = execute_query(query, parameters)
    user_id = single_value(response)
    if user_id is None:
        raise HTTPException(status_code=404, detail="username not found")
    else:
        return user_id


"""
GET GET GET GET GET GET GET GET GET GET GET GET GET GET GET GET GET GET GET GET GET GET GET GET
"""


@app.get("/latest")
def get_latest():
    """Returns integer used by simulator to track requests"""
    global LATEST
    return {"latest": LATEST}


@app.get("/msgs")
def get_messages(latest: int, no: int = LIMIT):
    """Returns the latest messages"""
    update_latest(latest)
    limit = no if no else LIMIT
    query = """
            SELECT message.text, message.pub_date, user.username 
            FROM message, user 
            WHERE message.flagged = 0 AND
            user.user_id = message.author_id
            ORDER BY message.pub_date DESC LIMIT ?
            """
    parameters = (limit,)
    response = execute_query(query, parameters)
    if response is not None:
        return [dict(zip(["content", "pub_date", "user"], r)) for r in response]
    else:
        return []


@app.get("/msgs/{username}")
def get_user_messages(username: str, latest: int, no: int = LIMIT):
    """Returns the latest messages of given user"""
    update_latest(latest)
    limit = no if no else LIMIT
    user_id = get_user_id(username)
    query = """
            SELECT message.text, message.pub_date, user.username 
            FROM message, user 
            WHERE message.flagged = 0 AND
            user.user_id = message.author_id AND user.user_id = ?
            ORDER BY message.pub_date DESC LIMIT ?
            """
    parameters = (user_id, limit)
    response = execute_query(query, parameters)
    if response is not None:
        return [dict(zip(["content", "pub_date", "user"], r)) for r in response]
    else:
        return []


@app.get("/fllws/{username}")
def get_followers(username: str, latest: int, no: int = LIMIT):
    """Returns followers of given user"""
    update_latest(latest)
    limit = no if no else LIMIT
    user_id = get_user_id(username)
    query = """
            SELECT user.username FROM user
            INNER JOIN follower ON follower.whom_id=user.user_id
            WHERE follower.who_id=?
            LIMIT ?
            """
    parameters = (user_id, limit)
    response = execute_query(query, parameters)
    if response is None:
        return {"follows": []}
    else:
        return {"follows": [follower for r in response for follower in r]}


"""
POST POST POST POST POST POST POST POST POST POST POST POST POST POST POST POST POST 
"""


@app.post("/msgs/{username}", status_code=201)
def post_user_message(username: str, latest: int, message: Message):
    """Post message as given username"""
    update_latest(latest)
    user_id = get_user_id(username)
    query = """
            INSERT INTO message (author_id, text, pub_date, flagged)
            VALUES (?, ?, ?, 0)
            """
    parameters = (user_id, message.content, int(time.time()))
    print(parameters)
    execute_query(query, parameters)
    return True
