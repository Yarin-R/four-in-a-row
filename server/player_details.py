"""
Small player_details module
"""


class Player_Details():
    """
    Small information class
    Contains information about a player
    instance is being created by Client_Handler class, for each client
    """
    def __init__(self):
        # boolean, logged_in
        self.logged_in = False

        # Username, string
        self.username = ""

        # Reference to a instance of Game, or None
        self.game = None

        # Integer, score of the user
        self.score = None
