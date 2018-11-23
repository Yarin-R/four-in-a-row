import random


class Game:
    def __init__(self, player_one, player_two):
        self.player_one = player_one
        self.player_two = player_two
        self.game_board = []
        self.turn = "1"  # starting from player one
        self.game_id = random.randint(0, 10000)
