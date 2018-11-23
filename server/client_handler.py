import time
import logger
import player_details
import auth_handler
import game


class Client_Handler():
    def __init__(self, c_socket, c_addr, server_details):
        self.player = player_details.Player_Details()
        self.state = "INIT"
        self.player.logged_in = False
        self.c_socket = c_socket
        self.c_addr = c_addr
        self.logger = logger.Logger("Client_Handler")
        self.server_details = server_details
        self.auth_handler = auth_handler.Auth_Handler()

    def handle(self):
        self.logger.info("Handling client..." + str(self.c_addr))
        while True:
            data = self.c_socket.recv(1024)

            if not data:
                self.logger.info("Client " + str(self.c_addr) + "blank data, disconnecting...")
                return

            # COOKIE|CMD|PARAMS
            data_splitted = data.split("|")

            if len(data_splitted) != 3:
                self.c_socket.send("INVALID_REQUEST")
                self.logger.info("Client " + str(self.c_addr) + "invalid request")
                continue

            cookie = data_splitted[0]
            cmd = data_splitted[1]
            params = data_splitted[2]

            # Trying to log in
            if cmd == "GETAUTH":
                auth_details = params.split(":")
                if len(auth_details) != 2:
                    self.logger.warning("Invalid auth_details")
                    continue
                username = auth_details[0]
                password = auth_details[1]
                # TODO Save username password etc...
                result, cookie = self.auth_handler.log_in(username, password)
                if result:
                    self.player.logged_in = True
                    self.player.username = username
                    self.c_socket.send("AUTH_SUCCESS|{0}".format(cookie))
                    self.logger.info("Client " + username + " successfully logged in!")
                    continue
                else:
                    self.c_socket.send("AUTH_FAILURE")
                    self.logger.info("Client " + username + " failed authentication")
                    continue
                    # TODO Check how many times of failure
                    # TODO block login if brute force in place

            if self.auth_handler.check_cookie(cookie):
                self.player.logged_in = True
            else:
                self.c_socket.send("INVALID_COOKIE")
                self.logger.info("Client " + str(self.c_addr) + "invalid cookie")
                continue

            # GETAUTH|roei:123
            # Check if logged in
            if not self.player.logged_in:
                self.c_socket.send("SEND_AUTH")
                self.logger.info("Client " + str(self.c_addr) + "not authenticated")
                continue

            # Logged in!
            # Now just the important features
            if cmd == "STARTGAME":
                if self.player.username not in self.server_details.waiting_for_game_players:
                    game_id = self.server_details.find_player_in_games(self.player.username)
                    if game_id:
                        self.c_socket.send("JOINED_GAME|" + game_id)
                        self.logger.info("Client " + str(self.c_addr) + " joined game " + game_id)
                        continue
                    else:
                        self.server_details.waiting_for_game_players.append(self.player.username)
                self.c_socket.send("JOINED_LIST")
                self.logger.info("Client " + str(self.c_addr) + " waiting to play!")
                continue

            if cmd == "JOINGAME":
                # Check if already in a game!
                game_id = self.server_details.find_player_in_games(self.player.username)
                if game_id:
                    self.c_socket.send("JOINED_GAME|" + game_id)
                    self.logger.info("Client " + str(self.c_addr) + " joined game " + game_id)
                    continue
                else:
                    found_game = False
                    for player in self.server_details.waiting_for_game_players:
                        if player != self.player.username:
                            # Found someone else!
                            # Creating a game!
                            new_game = game.Game(self.player.username, player)
                            found_game = True
                            self.server_details.waiting_for_game_players.remove(player)
                            self.server_details.waiting_for_game_players.remove(self.player.username)
                            self.c_socket.send("JOINED_GAME|" + new_game.game_id)
                            self.logger.info("Client " + str(self.c_addr) + " joined game " + game_id)
                            break
                    if not found_game:
                        self.c_socket.send("WAITING_GAME")
                        self.logger.info("Client " + str(self.c_addr) + " asked for players")
                    continue



            # Else
            else:
                self.c_socket.send("INVALID_REQUEST")
                self.logger.info("Client " + str(self.c_addr) + "invalid request")

