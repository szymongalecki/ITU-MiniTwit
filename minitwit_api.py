from fastapi import FastAPI
import sqlite3

"""
1. API uses the same database as minitwit.py
2. Find the equivalent of 'before_request' and 'after_request'
3. How to map the response to JSON from plain list of values
"""

app = FastAPI()
DATABASE = './minitwit.db'

def connect_db():
    """Returns a new connection to the database."""
    return sqlite3.connect(DATABASE)


@app.get("/")
def default():
    return "welcome to minitwit API :)"


@app.get("/{username}")
def user_data(username):
    cursor = connect_db().cursor()
    query = cursor.execute("SELECT * FROM user WHERE username=?", (username,))
    user_id = query.fetchall()[0][0]
    tweets = cursor.execute("SELECT * FROM message WHERE author_id=?", (user_id,))
    return tweets.fetchall()
