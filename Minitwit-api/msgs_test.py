import requests
import base64


# API in droplet
HOST = "http://138.68.73.127:8080"

# API in local container
# HOST = "http://localhost:8080"
USERNAME = "simulator"
PWD = "super_safe!"
CREDENTIALS = ":".join([USERNAME, PWD]).encode("ascii")
ENCODED_CREDENTIALS = base64.b64encode(CREDENTIALS).decode()
HEADERS = {
    "Connection": "close",
    "Content-Type": "application/json",
    f"Authorization": f"Basic {ENCODED_CREDENTIALS}",
}


def get_10_messages():
    url = f"{HOST}/msgs"
    response = requests.get(url, params={"no": 1}, headers=HEADERS)
    print(f"Status code: {response.status_code}")
    print(f"Content: {response.text}")


get_10_messages()
