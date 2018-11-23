import uuid


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
		# Will check against file of registered users
		# returns True/False and a cookie!

		# TODO check if user is registered

		return True, self.create_cookie(username)

	def register(self, username, password):
		pass

