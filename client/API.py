"""
API Module
Client will contact other players and the server using this module
* API class is the major class
* GameClosedException is an Exception class being thrown to the Game class
"""
import socket


# Creating an exception for game closing situation
class GameClosedException(Exception):
    pass


class API:
    """
    API Class
    Contains information about the server, cookie, logged_in state and the connection socket
    Allows Graphics and Game modules to contact the server
    For example:
    * Graphics would request leaderboard data to render to the user
    * Game would request a game room and a state of a given game
    """
    def __init__(self):
        """
        Initializing memebrs
        """
        # Cookie being used in the communication protocol
        # It helps the server to identify us without sending
        # the password each request
        self.cookie = ""

        # Logged in state
        self.logged_in = False

        # Server details: socket, address, port
        self.address = "yarin-four-game.tk"
        self.port = 9999
        self.sock = None

        # Username information
        self.username = None

        return

    def request(self, cmd, params):
        """
        Basic method, sending a command and corresponding command parameters
        :param cmd: command requested by the client
        :param params: parameters of the command
        :return: answer from the server, string
        """
        if not self.sock:
            # Create a new socket for the first connection
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((self.address, self.port))

        try:
            # Send a request
            self.sock.send("{0}|{1}|{2}".format(self.cookie, cmd, params))
            data = self.sock.recv(1024)
            return data

        except Exception as e:
            print "API Exception: {}".format(e)
            # Reset the connection
            self.sock = None

            # Not a recursion! just one step...
            # Create the request again
            self.request(cmd, params)

    def get_my_username(self):
        """
        Get username, should be saved here
        :return: username or None
        """
        return self.username

    def get_my_score(self):
        """
        Request logged in player score from the server
        :return: score, int. Upon failure, returns -1
        """
        response = self.request("GETSCORE", "")
        resp_array = response.split("|")
        if resp_array[0] == "GETSCORE":
            return int(resp_array[1])

        return -1

    def get_leaderboard(self):
        """
        Get top 5 players and their score
        :return:
        """
        data = self.request("GETLEADERBOARD", "")
        resp_array = data.split("|")
        return resp_array[1].split(',')

    def log_in(self, username, password):
        """
        Log in operation, using username and password
        return boolean upon success or failure
        Get cookie upon success to being identified by the server each request
        Pre-auth request

        :param username: username, string
        :param password: password, string
        :return: boolean, true upon success, false upon failure
        """
        response = self.request("GETAUTH", username + ":" + password)
        resp_array = response.split("|")

        if resp_array[0] == "AUTH_SUCCESS":
            self.cookie = resp_array[1]
            self.username = username
            return True
        else:
            return False

    def register(self, username, password):
        """
        Register operation, using username and password
        return boolean upon success or failure
        Just creating the user, not logging in!
        Pre-auth request

        :param username: username, string
        :param password: password, string
        :return: boolean, true upon success, false upon failure
        """
        response = self.request("REGISTERAUTH", username + ":" + password)
        resp_array = response.split("|")

        if resp_array[0] == "REGISTER_SUCCESS":
            return True
        else:
            return False

    def start_game(self):
        """
        Start a game, will add the user to the waiting list on the server
        If the server have found a competitor, "JOINED_GAME", the user will join the game
        """
        data = self.request("STARTGAME", "")
        if "|" in data:
            resp_array = data.split("|")
        else:
            resp_array = []
            resp_array.append(data)

        if resp_array[0] == "JOINED_GAME":
            return True, resp_array[1]
        elif resp_array[0] == "JOINED_LIST":
            return False, False

    def join_game(self):
        """
        Similar to start_game, but when the user is already listed on the waiting list
        """
        data = self.request("JOINGAME", "")
        if "|" in data:
            resp_array = data.split("|")
        else:
            resp_array = []
            resp_array.append(data)

        if resp_array[0] == "JOINED_GAME":
            return True, resp_array[1]
        elif resp_array[0] == "WAITING_GAME":
            return False, False

    def game_get_board(self, ignore_winner=False):
        """
        Get the current game board. If one of the players have won, it will return WINNER and the username
        of the winner.
        :param ignore_winner: Ignore winner information, just get the board (Even if won/lost)
        """
        # Getting the board or the if you are the winner or not
        if ignore_winner:
            data = self.request("GAME_BOARD", "IGNORE_WINNER")
        else:
            data = self.request("GAME_BOARD", "")

        resp_array = data.split("|")

        if resp_array[0] == "GAME_CLOSED":
            raise GameClosedException(resp_array[1])

        if resp_array[1].startswith("WINNER"):
            username_winner = resp_array[1].split(",")[1]

            return username_winner, ",".join(resp_array[1].split(",")[2:])
        else:
            return False, resp_array[1]

    def game_get_turn(self):
        """
        Check the server if the competitor made his/her move
        True upon yes, False upon no
        """

        data = self.request("GAME_IF_TURN", "")
        resp_array = data.split("|")

        if resp_array[0] == "INVALID_GAME_REQUEST":
            raise GameClosedException("GAME_CLOSED")

        if resp_array[0] == "GAME_CLOSED":
            raise GameClosedException(resp_array[1])

        if resp_array[1] == "True":
            return True

        else:
            return False

    def game_close(self):
        """
        Send the server a notification about game closure
        :return: True, always.
        """
        self.request("GAME_CLOSE", "")
        return True

    def game_do_turn(self, col):
        """
        Make a move, send the server a column that have been picked
        :param col: column on a game move
        :return:
        """
        data = self.request("GAME_DO_TURN", str(col))
        resp_array = data.split("|")

        if resp_array[0] == "GAME_CLOSED":
            raise GameClosedException(resp_array[1])

        return resp_array[1]

    def game_get_competitor(self):
        """
        Get the username of the competitor
        :return: string, username of the competitor
        """
        data = self.request("GAME_GET_COMPETITOR", "")
        resp_array = data.split("|")

        if resp_array[0] == "GAME_CLOSED":
            raise GameClosedException(resp_array[1])

        return resp_array[1]
