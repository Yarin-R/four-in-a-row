import uuid
import sqlite3
import hashlib


class Auth_Handler:
	def __init__(self):
		pass

	def create_cookie(self, username):
		cookie = str(uuid.uuid4())[24:]
		with open('cookies/{0}.cookie'.format(cookie), 'w') as f:
			f.write(username)

		return cookie

	def check_cookie_username(self, cookie, username):
		with open('cookies/{0}.cookie'.format(cookie)) as f:
			data = f.readlines()

		if data == username:
			return True
		else:
			return False

	def check_cookie(self, cookie):
		try:
			with open('cookies/{0}.cookie'.format(cookie)) as f:
				data = f.readlines()

			return data
		except Exception:
			return False

	def log_in(self, username, password):
		salt = "uo8na2uno8dujioaj8sdoj$$81s9"
		# Will check against file of registered users
		# returns True/False and a cookie!

		conn = sqlite3.connect('users.db')
		c = conn.cursor()
		c.execute("SELECT * FROM USERS where username=?", (username,))
		line = c.fetchone()
		conn.commit()
		conn.close()

		if line:
			# got the user
			if line[1] == hashlib.sha256(salt + password).hexdigest():
				return True, self.create_cookie(username)

		return False, None

	def register(self, username, password):
		salt = "uo8na2uno8dujioaj8sdoj$$81s9"

		if username == '' or password == '':
			return False

		conn = sqlite3.connect('users.db')
		c = conn.cursor()
		c.execute("SELECT * FROM USERS where username=?", (username,))
		line = c.fetchone()
		conn.commit()
		conn.close()

		if line:
			return False

		# Users does not exist
		password_hash = hashlib.sha256(salt + password).hexdigest()
		conn = sqlite3.connect('users.db')
		c = conn.cursor()
		c.execute("INSERT INTO USERS VALUES (?, ?, ?)", (username, password_hash,0,))
		conn.commit()
		conn.close()

		return True

	def get_username_score(self, username):
		conn = sqlite3.connect('users.db')
		c = conn.cursor()
		c.execute("SELECT * FROM USERS where username=?", (username,))
		line = c.fetchone()
		conn.commit()
		conn.close()

		if line:
			# got the user
			return int(line[2])

		return None

	def update_username_score(self):
		pass


