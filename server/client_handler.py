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
                self.logger.info("Client " + str(self.c_addr) + " blank data, disconnecting...")

                # If in game, remove
                g = self.server_details.find_player_in_games(self.player.username)
                if g:
                    g.game_close_reason = "PLAYER_DISCONNECTED"

                # If in waiting list, remove
                if self.player.username in self.server_details.waiting_for_game_players:
                    self.server_details.waiting_for_game_players.remove(self.player.username)
                    print repr(self.server_details.games)
                    print repr(self.server_details.waiting_for_game_players)
                    self.logger.info("Client " + str(self.c_addr) + " removed from waiting list")

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

            if cmd == "REGISTERAUTH":
                auth_details = params.split(":")
                if len(auth_details) != 2:
                    self.logger.warning("Invalid auth_details")
                    continue
                username = auth_details[0]
                password = auth_details[1]
                result = self.auth_handler.register(username, password)
                if result:
                    self.c_socket.send("REGISTER_SUCCESS")
                    self.logger.info("Client " + username + " successfully registered!")
                    continue
                else:
                    self.c_socket.send("REGISTER_FAILURE")
                    self.logger.info("Client " + username + " failed registration, try another username")
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
                print repr(self.server_details.games)
                print repr(self.server_details.waiting_for_game_players)
                if self.player.username not in self.server_details.waiting_for_game_players:
                    player_game = self.server_details.find_player_in_games(self.player.username)
                    if player_game:
                        self.player.game = player_game
                        game_id = player_game.game_id
                        self.c_socket.send("JOINED_GAME|" + str(game_id))
                        self.logger.info("Client " + str(self.c_addr) + " joined game " + str(game_id))
                        continue
                    else:
                        self.server_details.waiting_for_game_players.append(self.player.username)
                self.c_socket.send("JOINED_LIST")
                self.logger.info("Client " + str(self.c_addr) + " waiting to play!")
                continue

            if cmd == "JOINGAME":
                # Check if already in a game!
                print repr(self.server_details.games)
                print repr(self.server_details.waiting_for_game_players)
                player_game = self.server_details.find_player_in_games(self.player.username)
                if player_game:
                    game_id = player_game.game_id
                    self.player.game = player_game
                    self.c_socket.send("JOINED_GAME|" + str(game_id))
                    self.logger.info("Client " + str(self.c_addr) + " joined game " + str(game_id))
                    continue
                else:
                    found_game = False
                    for player in self.server_details.waiting_for_game_players:
                        if player != self.player.username:
                            # Found someone else!
                            # Creating a game!
                            new_game = game.Game(self.player.username, player)
                            found_game = True
                            self.player.game = new_game
                            self.server_details.games.append(new_game)
                            self.server_details.waiting_for_game_players.remove(player)
                            self.server_details.waiting_for_game_players.remove(self.player.username)
                            self.c_socket.send("JOINED_GAME|" + str(new_game.game_id))
                            self.logger.info("Client " + str(self.c_addr) + " joined game " + str(new_game.game_id))
                            break
                    if not found_game:
                        self.c_socket.send("WAITING_GAME")
                        self.logger.info("Client " + str(self.c_addr) + " asked for players")
                    continue

            if cmd == "GAME_BOARD":
                if self.player.game:
                    if self.player.game.game_close_reason is not None:
                        self.c_socket.send('GAME_CLOSED|{0}'.format(self.player.game.game_close_reason))
                        self.logger.info("Closing game {0} because {1}".format(self.player.game.game_id,
                                                                               self.player.game.game_close_reason))
                        self.logger.info("Closing game {0} between {1} and {2}".format(self.player.game.game_id,
                                                                                       self.player.game.player_two,
                                                                                       self.player.game.player_two))
                        self.server_details.games.remove(self.player.game)
                        self.player.game = None
                        continue

                    if params == "IGNORE_WINNER":
                        self.c_socket.send("GET_BOARD|" + self.player.game.get_board())
                    else:
                        winner = self.player.game.get_winner()
                        if winner:
                            self.c_socket.send("GET_BOARD|WINNER,{winner},{board}".format(winner=winner,
                                                                                          board=self.player.game.get_board()))
                            self.player.game.game_close_reason = "WINNING|{0}".format(winner)
                        else:
                            self.c_socket.send("GET_BOARD|" + self.player.game.get_board())
                else:
                    self.c_socket.send("INVALID_GAME_REQUEST")
                    self.logger.info("Client " + str(self.c_addr) + "invalid game request")
                continue

            if cmd == "GAME_GET_COMPETITOR":
                if self.player.game:
                    if self.player.game.game_close_reason is not None:
                        self.c_socket.send('GAME_CLOSED|{0}'.format(self.player.game.game_close_reason))
                        self.logger.info("Closing game {0} because {1}".format(self.player.game.game_id,
                                                                               self.player.game.game_close_reason))
                        self.logger.info("Closing game {0} between {1} and {2}".format(self.player.game.game_id,
                                                                                       self.player.game.player_two,
                                                                                       self.player.game.player_two))
                        self.server_details.games.remove(self.player.game)
                        self.player.game = None
                        continue

                    if self.player.game.player_one == self.player.username:
                        competitor = self.player.game.player_two
                    else:
                        competitor = self.player.game.player_one
                    self.c_socket.send("GET_COMPETITOR|" + competitor)
                else:
                    self.c_socket.send("INVALID_GAME_REQUEST")
                    self.logger.info("Client " + str(self.c_addr) + " invalid game request")
                continue

            if cmd == "GAME_IF_TURN":
                if self.player.game:
                    if self.player.game.game_close_reason is not None:
                        self.c_socket.send('GAME_CLOSED|{0}'.format(self.player.game.game_close_reason))
                        self.logger.info("Closing game {0} because {1}".format(self.player.game.game_id,
                                                                               self.player.game.game_close_reason))
                        self.logger.info("Closing game {0} between {1} and {2}".format(self.player.game.game_id,
                                                                                       self.player.game.player_two,
                                                                                       self.player.game.player_two))
                        self.server_details.games.remove(self.player.game)
                        self.player.game = None
                        continue

                    if self.player.game.turn == self.player.username:
                        my_turn = "True"
                    else:
                        my_turn = "False"
                    self.c_socket.send("IF_TURN|" + my_turn)
                else:
                    self.c_socket.send("INVALID_GAME_REQUEST")
                    self.logger.info("Client " + str(self.c_addr) + "invalid game request")
                continue

            if cmd == "GAME_DO_TURN":
                if self.player.game:
                    if self.player.game.game_close_reason is not None:
                        self.c_socket.send('GAME_CLOSED|{0}'.format(self.player.game.game_close_reason))
                        self.logger.info("Closing game {0} because {1}".format(self.player.game.game_id,
                                                                               self.player.game.game_close_reason))
                        self.logger.info("Closing game {0} between {1} and {2}".format(self.player.game.game_id,
                                                                                       self.player.game.player_two,
                                                                                       self.player.game.player_two))
                        self.server_details.games.remove(self.player.game)
                        self.player.game = None
                        continue

                    result_string = self.player.game.do_turn(self.player.username, int(params))
                    self.c_socket.send("DO_TURN|" + result_string)
                else:
                    self.c_socket.send("INVALID_GAME_REQUEST")
                    self.logger.info("Client " + str(self.c_addr) + "invalid game request")
                continue

            # Else
            else:
                self.c_socket.send("INVALID_REQUEST")
                self.logger.info("Client " + str(self.c_addr) + "invalid request")

