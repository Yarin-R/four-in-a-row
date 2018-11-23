# API
import socket

class API:
    def __init__(self):
        self.cookie = ""
        self.logged_in = False
        self.address = "127.0.0.1"
        self.port = 9999
        self.sock = None
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

    def get_leaderboard(self):
        # return a list of players
        pass

    def log_in(self, username, password):
        response = self.request("GETAUTH", username + ":" + password)
        resp_array = response.split("|")

        if resp_array[0] == "AUTH_SUCCESS":
            # todo check if cookie exists
            self.cookie = resp_array[1]
            return True
        else:
            return False

    def start_game(self):
        data = self.request("STARTGAME", "")
        resp_array = data.split("|")
        if resp_array[0] == "JOINED_GAME":
            return True, resp_array[1]
        elif resp_array[0] == "JOINED_LIST":
            return False, False

    def join_game(self):
        data = self.request("JOINGAME", "")
        resp_array = data.split("|")
        if resp_array[0] == "JOINED_GAME":
            return True, resp_array[1]
        elif resp_array[0] == "JOINED_LIST":
            return False, False
