"""
Thread-Safe module for cross-threads information
The data here is shared across all the users
Therefore, locking mechanisms are in use

Please double think about race-conditioning cases when editing code here!
"""
import threading


class Server_Details:
    """
    Shared class between all Client_Handlers
    Created by the Listener once, and one reference is being injected to each Client_Handler
    """
    def __init__(self):
        """
        Initializing members
        """
        # Thread-safe locking
        self.lock = threading.Lock()

        # List of waiting players, must be synced across threads
        self.waiting_for_game_players = []

        # List of games, must be synced across threads
        self.games = []

        # List of logged in players, must be synced across threads
        self.logged_in_players = []

    def find_player_in_games(self, username):
        """
        Find a player in the games list
        :param username: queried username
        :return: reference to a Game instance, false upon failure
        """
        for g in self.games:
            if username == g.player_one or username == g.player_two:
                return g
        return False

    def remove_player_from_waiting(self, player):
        """
        Remove a player from the waiting list (gave up, or joined game)
        :param player: string, username of a player
        """

        self.lock.acquire()
        try:
            self.waiting_for_game_players.remove(player)
        finally:
            self.lock.release()


