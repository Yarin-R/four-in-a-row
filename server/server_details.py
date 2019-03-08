import threading

class Server_Details:
    def __init__(self):
        self.lock = threading.Lock()
        self.waiting_for_game_players = []
        self.games = []
        self.logged_in_players = []

    def find_player_in_games(self, username):
        for g in self.games:
            if username == g.player_one or username == g.player_two:
                return g
        return False

    def remove_player_from_waiting(self, player):
        self.lock.acquire()
        try:
            self.waiting_for_game_players.remove(player)
        finally:
            self.lock.release()


