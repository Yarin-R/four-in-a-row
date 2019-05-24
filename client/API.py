# API
import socket


# Creating an exception for game closing situation
class GameClosedException(Exception):
    pass


class API:
    def __init__(self):
        self.cookie = ""
        self.logged_in = False
        self.address = "yarin-four-game.tk"
        self.port = 9999
        self.sock = None
        self.username = None
        return

    def request(self, cmd, params):
        if not self.sock:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((self.address, self.port))

        try:
            # request
            self.sock.send("{0}|{1}|{2}".format(self.cookie, cmd, params))
            data = self.sock.recv(1024)
            return data
        except Exception as e:
            print e
            self.sock = None

            # Not a recursion! just one step...
            self.request(cmd, params)

    def get_player_info(self):
        # Asking the server for current player info!
        pass

    def get_my_username(self):
        return self.username

    def get_my_score(self):
        response = self.request("GETSCORE", "")
        resp_array = response.split("|")
        if resp_array[0] == "GETSCORE":
            return int(resp_array[1])

        return -1

    def get_leaderboard(self):
        # return a list of players
        data = self.request("GETLEADERBOARD", "")
        resp_array = data.split("|")
        return resp_array[1].split(',')

    def log_in(self, username, password):
        response = self.request("GETAUTH", username + ":" + password)
        resp_array = response.split("|")

        if resp_array[0] == "AUTH_SUCCESS":
            self.cookie = resp_array[1]
            self.username = username
            return True
        else:
            return False

    def register(self, username, password):
        response = self.request("REGISTERAUTH", username + ":" + password)
        resp_array = response.split("|")

        if resp_array[0] == "REGISTER_SUCCESS":
            return True
        else:
            return False

    def start_game(self):
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
        # Getting the board or the if you are the winner or not
        if ignore_winner:
            data = self.request("GAME_BOARD", "IGNORE_WINNER")
        else:
            data = self.request("GAME_BOARD", "")

        resp_array = data.split("|")
        if resp_array[0] == "GAME_CLOSED":
            raise GameClosedException(resp_array[1])
        if resp_array[1].startswith("WINNER"):
            # do something about winner
            username_winner = resp_array[1].split(",")[1]

            return username_winner, ",".join(resp_array[1].split(",")[2:])
        else:
            return False, resp_array[1]

    def game_get_turn(self):
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
        data = self.request("GAME_CLOSE", "")
        return True

    def game_do_turn(self, col):
        data = self.request("GAME_DO_TURN", str(col))
        resp_array = data.split("|")
        if resp_array[0] == "GAME_CLOSED":
            raise GameClosedException(resp_array[1])

        return resp_array[1]

    def game_get_competitor(self):
        data = self.request("GAME_GET_COMPETITOR", "")
        resp_array = data.split("|")
        if resp_array[0] == "GAME_CLOSED":
            raise GameClosedException(resp_array[1])
        return resp_array[1]
