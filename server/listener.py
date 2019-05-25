import socket
from client_handler import Client_Handler
import threading
import logger
import server_details


class Listener():
    def __init__(self):
        self.address = "127.0.0.1"
        self.port = 9999
        self.max_players = 20
        self.logger = logger.Logger("Listener")
        self.server_details = server_details.Server_Details()

    def listen(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((self.address, self.port))
        s.listen(self.max_players)
        self.logger.debug("bind and listen successfully on " + self.address + " " + str(self.port))

        while True:
            self.logger.info("Accepting connection")
            c_socket, c_addr = s.accept()
            self.logger.info("Accepted connection from " + str(c_addr))
            c_handler = Client_Handler(c_socket, c_addr, self.server_details)
            threading.Thread(target=c_handler.handle).start()
