from contextlib import closing
from datetime import datetime
import os
import time
from fastapi import FastAPI, HTTPException
import sqlite3
from pydantic import BaseModel
from typing import Tuple
import uvicorn
from werkzeug.security import generate_password_hash
import psycopg2

"""
CONFIGURATION 
"""

app = FastAPI()
CONNECTION = psycopg2.connect(
    database="postgres",
    user="postgres",
    password="postgres",
    host="DB-postgres",
    port="5432",
)
LIMIT = 100
LATEST = 0


"""
DATA MODELS 
"""


class Message(BaseModel):
    content: str


class Tweet(BaseModel):
    content: str
    pub_date: datetime
    user: str


class User(BaseModel):
    username: str
    email: str
    pwd: str


class Follow_Unfollow(BaseModel):
    follow: str | None = None
    unfollow: str | None = None


"""
HELPER FUNCTIONS 
"""


def initialise_db():
    """Creates the database tables"""
    with open("minitwit_schema.sql", "r") as f:
        post_query(f.read(), ())


def update_latest(latest: int) -> None:
    """Updates value of global variable LATEST"""
    global LATEST
    LATEST = latest if latest != -1 else LATEST


def connect_db():
    """Returns connection to db"""
    return psycopg2.connect(
        database="postgres",
        user="postgres",
        password="postgres",
        host="DB-postgres",
        port="5432",
    )


def reconnect_db():
    """Reconnect to database if connection is terminated"""
    global CONNECTION
    CONNECTION = connect_db()


def get_query(query: str, parameters: Tuple) -> list:
    """Execute query related to get endpoint"""
    if not CONNECTION:
        reconnect_db()

    with CONNECTION as connection:
        with connection.cursor() as curs:
            curs.execute(query, parameters)
            return curs.fetchall()


def post_query(query: str, parameters: Tuple) -> None:
    """Execute query related to post endpoint"""
    if not CONNECTION:
        reconnect_db()

    with CONNECTION as connection:
        with connection.cursor() as cursor:
            cursor.execute(query, parameters)


def get_user_id(username: str) -> int | None:
    """Returns user_id if username exists in database"""
    query = """
            SELECT id
            FROM public.user
            WHERE username = (%s)
            """
    parameters = (username,)
    response = get_query(query, parameters)
    if response != []:
        return response[0][0]
    return None


"""
GET ENDPOINTS
"""

# OK
@app.get("/latest", status_code=200)
def get_latest() -> dict[str, int]:
    """Returns value of global variable LATEST"""
    global LATEST
    return {"latest": LATEST}


# OK, for tests only
@app.get("/users", status_code=200)
def get_users():
    """Returns all usernames"""
    response = get_query("SELECT username FROM public.user", ())
    return response


# OK
@app.get("/msgs", status_code=200)
def get_messages(latest: int, no: int = LIMIT) -> list[Tweet]:
    """Returns the latest messages"""
    update_latest(latest)
    limit = no if no else LIMIT
    query = """
            SELECT public.message.text, public.message.pub_date, public.user.username
            FROM public.message, public.user
            WHERE public.message.flagged = False AND
            public.user.id = public.message.author_id
            ORDER BY public.message.pub_date DESC LIMIT (%s)
            """
    parameters = (limit,)
    response = get_query(query, parameters)
    if response != []:
        return [Tweet(content=r[0], pub_date=r[1], user=r[2]) for r in response]
        # return [dict(zip(["content", "pub_date", "user"], r)) for r in response]
    else:
        return []


# OK
@app.get("/msgs/{username}", status_code=200)
def get_user_messages(username: str, latest: int, no: int = LIMIT) -> list[Tweet]:
    """Returns the latest messages of a given user"""
    update_latest(latest)
    limit = no if no else LIMIT
    user_id = get_user_id(username)
    query = """
            SELECT public.message.text, public.message.pub_date, public.user.username 
            FROM public.message, public.user 
            WHERE public.message.flagged = False AND
            public.user.id = public.message.author_id AND public.user.id = (%s)
            ORDER BY public.message.pub_date DESC LIMIT (%s)
            """
    parameters = (user_id, limit)
    response = get_query(query, parameters)
    if response is not None:
        return [Tweet(content=r[0], pub_date=r[1], user=r[2]) for r in response]
        # return [dict(zip(["content", "pub_date", "user"], r)) for r in response]
    else:
        return []


@app.get("/fllws/{username}", status_code=200)
def get_user_followers(
    username: str, latest: int, no: int = LIMIT
) -> dict[str, list[str]]:
    """Returns followers of a given user"""
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
    response = get_query(query, parameters)
    if response is None:
        return {"follows": []}
    else:
        return {"follows": [follower for r in response for follower in r]}


"""
POST ENDPOINTS 
"""

# OK
@app.post("/register", status_code=204)
def post_register_user(latest: int, user: User) -> None:
    update_latest(latest)
    if get_user_id(user.username) is not None:
        raise HTTPException(status_code=400, detail="The username is already taken")
    if "@" not in user.email:
        raise HTTPException(status_code=400, detail="Provided email has no @")
    query = """
            INSERT INTO public.user (username, email, password, date_joined, first_name, last_name, is_superuser, is_staff, is_active) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
    parameters = (
        user.username,
        user.email,
        generate_password_hash(user.pwd),
        datetime.now(),
        "",
        "",
        False,
        False,
        False,
    )
    post_query(query, parameters)


@app.post("/msgs/{username}", status_code=204)
def post_user_messages(username: str, latest: int, message: Message) -> None:
    """Posts message as a given user"""
    update_latest(latest)
    user_id = get_user_id(username)
    query = """
            INSERT INTO message (author_id, text, pub_date, flagged)
            VALUES (?, ?, ?, 0)
            """
    parameters = (user_id, message.content, int(time.time()))
    post_query(query, parameters)


@app.post("/fllws/{username}", status_code=204)
def post_follow_unfollow_user(username: str, latest: int, f_u: Follow_Unfollow) -> None:
    """Follows or unfollows user for another given user"""
    update_latest(latest)
    follower = get_user_id(username)
    if f_u.follow:
        user = get_user_id(f_u.follow)
        query = """ 
                INSERT INTO follower (who_id, whom_id) 
                VALUES (?, ?) 
                """
    else:
        user = get_user_id(f_u.unfollow)
        query = """
                DELETE FROM follower 
                WHERE who_id=? and WHOM_ID=?
                """
    parameters = (follower, user)
    post_query(query, parameters)


"""
EMPTY DATABASE
"""

# initialise_db()

"""
GUARD & RUN 
"""

if __name__ == "__main__":
    uvicorn.run("minitwit_api_2:app", host="0.0.0.0", port=8080, reload=True)
