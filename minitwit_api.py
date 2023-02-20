from fastapi import FastAPI, HTTPException
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

def get_user_id(username):
    """Returns user_id if username exists in database."""
    cursor = connect_db().cursor()
    query = """
            SELECT user_id 
            FROM user 
            WHERE username = ?
            """
    user_id = cursor.execute(query, (username, )).fetchone()
    cursor.close()
    return user_id[0] if user_id else None

@app.get("/", response_class=PlainTextResponse)
def default():
    return "HELLO FROM THE API\nAT LEAST, I CAN SAY THAT I'VE TRIED"

@app.get("/msgs/{username}")
def get_user_messages(username):
    user_id = get_user_id(username)
    if user_id is None:
        raise HTTPException(status_code=404, detail="username not found")
    cursor = connect_db().cursor()
    query = """
            SELECT message.*, user.* 
            FROM message, user 
            WHERE message.flagged = 0 AND
            user.user_id = message.author_id AND user.user_id = ?
            ORDER BY message.pub_date DESC LIMIT ?
            """
    response = cursor.execute(query, (user_id, LIMIT)).fetchall()
    cursor.close()
    return response
