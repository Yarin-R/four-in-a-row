class Server_Details:
    def __init__(self):
        self.waiting_for_game_players = []
        self.games = []

    def find_player_in_games(self, username):
        for g in self.games:
            if username == g.player_one or username == g.player_two:
                return g
        return False
