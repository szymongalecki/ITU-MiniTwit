from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import string
import random
import pytest

def randomString(l):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=l))

def setupDriver(subpage):
    options = Options()
    options.add_argument('--headless=new')
    driver = webdriver.Chrome(options=options)    
    driver.get("http://138.68.73.127:8000/"+subpage+"/")
    return driver

@pytest.fixture
def signUp():
    driver = setupDriver("signup")
    driver.find_element("id", "id_username").send_keys(randomString(9))
    driver.find_element("id", "id_email").send_keys(randomString(9)+"@gmail.com")
    driver.find_element("id", "id_password1").send_keys("admin123!")
    driver.find_element("id", "id_password2").send_keys("admin123!")
    driver.find_element("xpath", "/html/body/div/div[2]/form/button").click()
    time.sleep(2)
    return driver.title

@pytest.fixture
def logIn():
    driver = setupDriver("login")
    driver.find_element("id", "id_username").send_keys("testuser")
    driver.find_element("id", "id_password").send_keys("admin123!")
    driver.find_element("xpath", "/html/body/div/div[2]/form/button").click()
    time.sleep(2)
    return driver.title

@pytest.fixture
def postTweet():
    driver = setupDriver("login")
    driver.find_element("id", "id_username").send_keys("testuser")
    driver.find_element("id", "id_password").send_keys("admin123!")
    driver.find_element("xpath", "/html/body/div/div[2]/form/button").click()
    time.sleep(2)
    driver.find_element("id", "id_username").send_keys("testuser")
    driver.find_element("xpath", "/html/body/div/div[2]/div[1]/form/p/input[1]").send_keys("this is a test tweet")
    driver.find_element("xpath", "/html/body/div/div[2]/div[1]/form/p/input[2]").click()
    time.sleep(2)
    tweet = driver.find_element("xpath", "/html/body/div/div[2]/ul/li[2]/p")
    return tweet


def test_signup(signUp):
    assert "Log In" in signUp

def test_login(logIn):
    assert "My Timeline" in logIn

def test_post_tweet(postTweet):
    assert "this is a test tweet" in postTweet