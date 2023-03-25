from contextlib import closing
import os
import time
from fastapi import FastAPI, HTTPException
import sqlite3
from pydantic import BaseModel
from typing import Tuple
import uvicorn
from werkzeug.security import generate_password_hash


"""
CONFIGURATION
"""

app = FastAPI()
DATABASE = "./minitwit.db"
LIMIT = 100
LATEST = 0


"""
DATA MODELS
"""


class Message(BaseModel):
    content: str


class Tweet(BaseModel):
    content: str
    pub_date: int
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


def init_db() -> None:
    """Creates the database tables"""
    with closing(sqlite3.connect(DATABASE)) as db:
        with open("schema.sql", "r") as f:
            db.cursor().executescript(f.read())
        db.commit()


def update_latest(latest: int) -> None:
    """Updates value of global variable LATEST"""
    global LATEST
    LATEST = latest if latest != -1 else LATEST


def execute_query(query: str, parameters: Tuple) -> list | None:
    """Executes query with given parameters, fetches all results, commits to db"""
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


def get_user_id(username: str) -> int | HTTPException:
    """Returns user_id if username exists in database"""
    query = """
            SELECT user_id
            FROM user
            WHERE username = ?
            """
    parameters = (username,)
    response = execute_query(query, parameters)
    user_id = None if response is None else response[0][0]
    if user_id is None:
        raise HTTPException(status_code=404, detail="username not found")
    else:
        return user_id


"""
GET ENDPOINTS
"""


@app.get("/latest", status_code=200)
def get_latest() -> dict[str, int]:
    """Returns value of global variable LATEST"""
    global LATEST
    return {"latest": LATEST}


@app.get("/msgs", status_code=200)
def get_messages(latest: int, no: int = LIMIT) -> list[Tweet]:
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
        return [Tweet(content=r[0], pub_date=r[1], user=r[2]) for r in response]
        # return [dict(zip(["content", "pub_date", "user"], r)) for r in response]
    else:
        return []


@app.get("/msgs/{username}", status_code=200)
def get_user_messages(username: str, latest: int, no: int = LIMIT) -> list[Tweet]:
    """Returns the latest messages of a given user"""
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
        return [Tweet(content=r[0], pub_date=r[1], user=r[2]) for r in response]
        # return [dict(zip(["content", "pub_date", "user"], r)) for r in response]
    else:
        return []


@app.get("/fllws/{username}", status_code=200)
def get_user_followers(username: str, latest: int, no: int = LIMIT) -> dict[str, list[str]]:
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
    response = execute_query(query, parameters)
    if response is None:
        return {"follows": []}
    else:
        return {"follows": [follower for r in response for follower in r]}


"""
POST ENDPOINTS
"""


@app.post("/register", status_code=204)
def post_register_user(latest: int, user: User) -> None:
    """Registers a new user with the given data"""
    update_latest(latest)
    try:
        get_user_id(user.username)
    except HTTPException as user_does_not_exist:
        pass
    else:
        raise HTTPException(status_code=400, detail="The username is already taken")

    if "@" not in user.email:
        raise HTTPException(status_code=400, detail="Provided email has no @")
    query = """
            INSERT INTO user (username, email, pw_hash)
            VALUES (?, ?, ?)
            """
    parameters = (user.username, user.email, generate_password_hash(user.pwd))
    execute_query(query, parameters)


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
    execute_query(query, parameters)


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
    execute_query(query, parameters)


"""
EMPTY DATABASE
"""

os.system(f"rm {DATABASE}")
init_db()

"""
GUARD & RUN
"""

if __name__ == "__main__":
    uvicorn.run("minitwit_api:app", host="0.0.0.0", port=8080, reload=True)
