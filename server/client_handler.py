import time
import logger
import player_details

class Client_Handler():
	def __init__(self, c_socket, c_addr):
		self.player = player_details.Player_Details()
		self.state = "INIT"
		self.player.logged_in = False
		self.c_socket = c_socket
		self.c_addr = c_addr
		self.logger = logger.Logger("Client_Handler")

	def handle(self):
		self.logger.info("Handling client..." + str(self.c_addr))
		while True:
			data = self.c_socket.recv(1024)
			if not data:
				self.logger.info("Client " + str(self.c_addr) + "blank data, disconnecting...")
				return

			# Trying to log in
			if data.startswith("GETAUTH"):
				params = data.split("|")[1:]
				if len(params) != 1:
					self.logger.warning("Invalid data upon GETAUTH")
					continue
				auth_details = params[0].split(":")
				if len(auth_details) != 2:
					self.logger.warning("Invalid auth_details")
					continue
				username = auth_details[0]
				password = auth_details[1]
				# TODO Save username password etc...
				if username == "user":
					self.player.logged_in = True
					self.c_socket.send("AUTH_SUCCESS")
					self.logger.info("Client " + username + " successfully logged in!")
				else:
					self.c_socket.send("AUTH_FAILURE")
					self.logger.info("Client " + username + " failed authentication")
					# TODO Check how many times of failure
					# TODO block login if brute force in place


			# GETAUTH|roei:123
			# Check if logged in
			elif not self.player.logged_in:
				self.c_socket.send("SEND_AUTH")

			# Logged in!


			# Else
			else:
				self.c_socket.send("INVALID_REQUEST")
				self.logger.info("Client " + str(self.c_addr) + "invalid request")


			