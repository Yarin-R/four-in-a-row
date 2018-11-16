import time
from logger import Logger

class Client_Handler():
	def __init__(self, c_socket, c_addr):
		self.player = None
		self.state = "INIT"
		self.c_socket = c_socket
		self.c_addr = c_addr
		self.logger = Logger("Client_Handler")

	def handle(self):
		while True:
			self.logger.info("Handling client..." + str(self.c_addr))
			time.sleep(5)