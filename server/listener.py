"""
Listener module
Being called and created once by the main module and function, main()
"""

import socket
from client_handler import Client_Handler
import threading
import logger
import server_details


class Listener:
    """
    Listener class, holding the socket open and redirecting new connection
    to the corresponding class in a new thread
    """
    def __init__(self):
        # Listening information, default on 9999 to everyone
        self.address = "0.0.0.0"
        self.port = 9999

        # Max amount of players
        self.max_players = 20

        # One logger class for all the server class instances
        self.logger = logger.Logger("Listener")

        # Creating a shared Server_Details instance to hold important information
        # Across all threads
        self.server_details = server_details.Server_Details()

    def listen(self):
        """
        Main function of Listener, listening on a post and redirecting created connection
        to a new Client_Handler class (sharing server_details reference)
        :return: Never returns. If returns, program has been killed or exited
        """
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
