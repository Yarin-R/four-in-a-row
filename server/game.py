"""
Game module, holding the Game class
Taking care of every logic that Game needs to hold
"""
import random


class Game:
    """
    Game class
    Taking care of every logic that Game needs to hold
    """
    def __init__(self, player_one, player_two):
        """
        Initializing members of the class

        :param player_one: username
        :param player_two: username
        """
        # player one is blue, player two is red
        self.player_one = player_one
        self.player_two = player_two

        # List of lists, game board
        self.game_board = []

        # Who is making the current turn
        self.turn = self.player_one  # starting from player one

        # Randomize a game id
        self.game_id = random.randint(0, 10000)

        # Reason of a closed game
        self.game_close_reason = None

        # Create an empty board and initialize game_board
        self.create_board()

    def get_winner(self):
        """
        Get the winner, by username
        If no winner, then return False
        """
        for i in range(0, 6):
            for j in range(0, 7):
                if self.check_winner(i, j):
                    if self.game_board[j][i] == 'B':
                        return self.player_one
                    else:
                        return self.player_two

        return False

    def check_winner(self, x, line):
        """
        Helper function for get_winner function
        :param x: column
        :param line: row
        :return: True if found four in a row
        """
        try:
            if self.game_board[line][x] is "R" or self.game_board[line][x] is "B":
                kind = self.game_board[line][x]
                try:
                    if kind is self.game_board[line][x + 1] and kind is self.game_board[line][x + 2] and \
                            kind is self.game_board[line][x + 3]:
                        return True
                except Exception:
                    pass

                try:
                    if kind is self.game_board[line + 1][x + 1] and kind is self.game_board[line + 2][x + 2] and \
                            kind is self.game_board[line + 3][x + 3]:
                        return True
                except Exception:
                    pass

                try:
                    if kind is self.game_board[line + 1][x] and kind is self.game_board[line + 2][x] and \
                            kind is self.game_board[line + 3][x]:
                        return True
                except Exception:
                    pass

                try:
                    if kind is self.game_board[line + 1][x - 1] and kind is self.game_board[line + 2][x - 2] \
                            and kind is self.game_board[line + 3][x - 3]:
                        return True
                except Exception:
                    pass

                try:
                    if kind is self.game_board[line - 1][x + 1] and kind is self.game_board[line - 2][x + 2] \
                            and kind is self.game_board[line - 3][x + 3]:
                        return True
                except Exception:
                    pass

                try:
                    if kind is self.game_board[line - 1][x - 1] and kind is self.game_board[line - 2][x - 2] \
                            and kind is self.game_board[line - 3][x - 3]:
                        return True
                except Exception:
                    pass

        except Exception as e:
            pass
        return False

    def get_board(self):
        """
        return formatted board
        Everything is reversed, just the client gui is ok
        """

        s = ""
        for line_array in self.game_board:
            for j in line_array:
                s += j
            s += ","

        return s[:-1]

    def get_player_color(self, player_username):
        """
        Get the player color (blue or red)
        :param player_username: username
        :return: "B" (blue) or "R" (red)
        """
        if player_username == self.player_one:
            return "B"
        else:
            return "R"

    def set_next_turn(self, current_player):
        """
        Get who is doing the next turn
        Set the self.turn member

        :param current_player: who is player now? username, string
        :return: None
        """
        if current_player == self.player_one:
            self.turn = self.player_two
        else:
            self.turn = self.player_one

        return

    def do_turn(self, player_username, col):
        """
        Do a turn, current username and column
        :param player_username: username of player
        :param col: column number
        :return: "OK" on success, "NO_SPACE" on failure (column is full)
        """
        color = self.get_player_color(player_username)
        line = self.get_able_line(col)

        if self.is_able_to_input_to_board(line, col):
            # Performing
            self.game_board[line][col] = color
            self.set_next_turn(player_username)
            return "OK"

        else:
            # False, no space in column
            return "NO_SPACE"

    def create_board(self):
        """
        Create an empty game board, list of lists
        Set up self.game_board

        :return: None
        """
        self.game_board = []
        for i in range(0, 6):
            self.game_board.append([])
            for j in range(0, 7):
                self.game_board[i].append("-")
        return

    def get_able_line(self, x):
        """
        Helper function, check the top free row
        :param x: column
        :return: number of the first free row from the bottom for this column
        """
        line = 0
        while True:
            if line < 6:
                if self.game_board[line][x] is "-":
                    break
                line = line + 1
            else:
                break

        return line

    def is_able_to_input_to_board(self, line, x):
        """
        Check if the current column and row are free
        :param line: row
        :param x: column
        :return: True or False, as answer
        """
        if line > 6:
            return False

        return self.game_board[line][x] == '-'

