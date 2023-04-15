from datetime import datetime
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from typing import Tuple
import uvicorn
from werkzeug.security import generate_password_hash
import psycopg2
from prometheus_fastapi_instrumentator import Instrumentator


"""
CONFIGURATION
"""


app = FastAPI()
LIMIT = 100
LATEST = 0

Instrumentator().instrument(app).expose(app)


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


def authenticate_simulator(request: Request) -> None | HTTPException:
    if (
        "Authorization" not in request.headers
        or "Basic c2ltdWxhdG9yOnN1cGVyX3NhZmUh" != request.headers["Authorization"]
    ):
        raise HTTPException(
            status_code=403, detail="You are not authorized to use this resource!"
        )


def initialise_db() -> None:
    """Creates the database tables"""
    with open("minitwit_schema.sql", "r") as f:
        post_query(f.read(), ())


def delete_all_rows() -> None:
    query = """
            DELETE FROM public.follower;
            DELETE FROM public.message;
            DELETE FROM public.user;
            """
    post_query(query, ())


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
    )


def get_query(query: str, parameters: Tuple) -> list:
    """Execute query related to get endpoint"""
    with connect_db() as db:
        with db.cursor() as cursor:
            cursor.execute(query, parameters)
            return cursor.fetchall()


def post_query(query: str, parameters: Tuple) -> None:
    """Execute query related to post endpoint"""
    with connect_db() as db:
        with db.cursor() as cursor:
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


def user_not_found(user_id: int | None) -> None | HTTPException:
    """Throws exception if user_id is not an integer"""
    if user_id is None:
        raise HTTPException(status_code=404, detail="username not found")


"""
GET ENDPOINTS
"""


@app.get("/latest", status_code=200)
def get_latest() -> dict[str, int]:
    """Returns value of global variable LATEST"""
    global LATEST
    return {"latest": LATEST}


@app.get("/msgs", status_code=200)
def get_messages(request: Request, latest: int, no: int = LIMIT) -> list[Tweet]:
    """Returns the latest messages"""
    update_latest(latest)
    authenticate_simulator(request)
    query = """
            SELECT public.message.text, public.message.pub_date, public.user.username
            FROM public.message, public.user
            WHERE public.message.flagged = False AND
            public.user.id = public.message.author_id
            ORDER BY public.message.pub_date DESC LIMIT (%s)
            """
    parameters = (no,)
    response = get_query(query, parameters)
    if response != []:
        return [Tweet(content=r[0], pub_date=r[1], user=r[2]) for r in response]
    else:
        return []


@app.get("/msgs/{username}", status_code=200)
def get_user_messages(
    request: Request, username: str, latest: int, no: int = LIMIT
) -> list[Tweet]:
    """Returns the latest messages of a given user"""
    update_latest(latest)
    authenticate_simulator(request)
    user_id = get_user_id(username)
    user_not_found(user_id)
    query = """
            SELECT public.message.text, public.message.pub_date, public.user.username
            FROM public.message, public.user
            WHERE public.message.flagged = False AND
            public.user.id = public.message.author_id AND public.user.id = (%s)
            ORDER BY public.message.pub_date DESC LIMIT (%s)
            """
    parameters = (user_id, no)
    response = get_query(query, parameters)
    if response is not None:
        return [Tweet(content=r[0], pub_date=r[1], user=r[2]) for r in response]
    else:
        return []


@app.get("/fllws/{username}", status_code=200)
def get_user_followers(
    request: Request, username: str, latest: int, no: int = LIMIT
) -> dict[str, list[str]]:
    """Returns followers of a given user"""
    update_latest(latest)
    authenticate_simulator(request)
    user_id = get_user_id(username)
    user_not_found(user_id)
    query = """
            SELECT public.user.username FROM public.user
            INNER JOIN public.follower ON public.follower.whom_id=public.user.id
            WHERE public.follower.who_id = (%s)
            LIMIT (%s)
            """
    parameters = (user_id, no)
    response = get_query(query, parameters)
    if response is None:
        return {"follows": []}
    else:
        return {"follows": [follower for r in response for follower in r]}


"""
POST ENDPOINTS
"""


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
def post_user_messages(
    request: Request, username: str, latest: int, message: Message
) -> None:
    """Posts message as a given user"""
    update_latest(latest)
    authenticate_simulator(request)
    user_id = get_user_id(username)
    user_not_found(user_id)
    query = """
            INSERT INTO public.message (author_id, text, pub_date, flagged)
            VALUES (%s, %s, %s, %s)
            """
    parameters = (user_id, message.content, datetime.now(), False)
    post_query(query, parameters)


@app.post("/fllws/{username}", status_code=204)
def post_follow_unfollow_user(
    request: Request, username: str, latest: int, f_u: Follow_Unfollow
) -> None:
    """Follows or unfollows user for another given user"""
    update_latest(latest)
    authenticate_simulator(request)
    follower_id = get_user_id(username)
    user_not_found(follower_id)
    if f_u.follow:
        user_id = get_user_id(f_u.follow)
        user_not_found(user_id)
        query = """
                INSERT INTO public.follower (who_id, whom_id)
                VALUES (%s, %s)
                """
    else:
        user_id = get_user_id(f_u.unfollow)
        user_not_found(user_id)
        query = """
                DELETE FROM public.follower
                WHERE who_id = (%s) and WHOM_ID = (%s)
                """
    parameters = (follower_id, user_id)
    post_query(query, parameters)


"""
INITIALISE DATABASE / DELETE ALL ROWS
"""

# initialise_db()
# delete_all_rows()

"""
GUARD & RUN
"""

if __name__ == "__main__":
    uvicorn.run("minitwit_api_2:app", host="0.0.0.0", port=8080, reload=True)
