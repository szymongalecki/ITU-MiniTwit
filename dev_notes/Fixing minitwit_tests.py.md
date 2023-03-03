**Author: Szymon Gałecki**
### TypeError #1 
```python
Traceback (most recent call last):
  File "/Users/szymongalecki/Desktop/CS@ITU/S2/DevOps/itu-minitwit/minitwit_tests.py", line 23, in setUp
    minitwit.init_db()
  File "/Users/szymongalecki/Desktop/CS@ITU/S2/DevOps/itu-minitwit/minitwit.py", line 41, in init_db
    db.cursor().executescript(f.read())
TypeError: executescript() argument must be str, not bytes
```

### Orginal code
```python
def init_db():
	"""Creates the database tables."""
	with closing(connect_db()) as db:
		with app.open_resource('schema.sql') as f:
			db.cursor().executescript(f.read())
		db.commit()
```

### Convert bytes to string
```python
db.cursor().executescript(f.read().decode('utf-8'))
```

### TypeError #2
```python
Traceback (most recent call last):
  File "/Users/szymongalecki/Desktop/CS@ITU/S2/DevOps/itu-minitwit/minitwit_tests.py", line 85, in test_login_logout
    assert 'You were logged in' in rv.data
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
TypeError: a bytes-like object is required, not 'str'
```

### Original code (one of many snippets)
```python
def test_login_logout(self):
	"""Make sure logging in and logging out works"""
	rv = self.register_and_login('user1', 'default')
	assert 'You were logged in' in rv.data
	rv = self.logout()
	assert 'You were logged out' in rv.dat
	rv = self.login('user1', 'wrongpassword')
	assert 'Invalid password' in rv.data
	rv = self.login('user2', 'wrongpassword')
	assert 'Invalid username' in rv.data
```

### Cast the response to string
```python
assert 'You were logged in' in str(rv.data)
```

### Output
```
We got a visitor from: 127.0.0.1
.We got a visitor from: 127.0.0.1
We got a visitor from: 127.0.0.1
We got a visitor from: 127.0.0.1
We got a visitor from: 127.0.0.1
..We got a visitor from: 127.0.0.1
We got a visitor from: 127.0.0.1
We got a visitor from: 127.0.0.1
We got a visitor from: 127.0.0.1
We got a visitor from: 127.0.0.1
We got a visitor from: 127.0.0.1
We got a visitor from: 127.0.0.1
.
----------------------------------------------------------------------
Ran 4 tests in 0.428s

OK
```

