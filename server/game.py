import random


class Game:
    def __init__(self, player_one, player_two):
        # player one is blue, player two is red
        self.player_one = player_one
        self.player_two = player_two
        self.game_board = []
        self.turn = self.player_one  # starting from player one
        self.game_id = random.randint(0, 10000)
        self.game_close_reason = None

        self.create_board()

    def get_winner(self):
        for i in range(0, 7):
            for j in range(0, 7):
                if self.check_winner(i, j):
                    if self.game_board[j][i] == 'B':
                        return self.player_one
                    else:
                        return self.player_two

        return False

    def check_winner(self, x, line):
        try:
            if self.game_board[line][x] is "R" or self.game_board[line][x] is "B":
                kind = self.game_board[line][x]
                if kind is self.game_board[line][x + 1] and kind is self.game_board[line][x + 2] and kind is self.game_board[line][x + 3]:
                    return True
                if kind is self.game_board[line + 1][x + 1] and kind is self.game_board[line + 2][x + 2] and kind is self.game_board[line + 3][
                    x + 3]:
                    return True
                if kind is self.game_board[line + 1][x] and kind is self.game_board[line + 2][x] and kind is self.game_board[line + 3][x]:
                    return True
                if kind is self.game_board[line + 1][x - 1] and kind is self.game_board[line + 2][x - 2] and kind is self.game_board[line + 3][
                    x - 3]:
                    return True
        except Exception as e:
            pass
        return False

    def get_board(self):
        # return formatted board
        # Everything is reversed, just the client gui is ok

        s = ""
        for line_array in self.game_board:
            for j in line_array:
                s += j
            s += ","

        return s[:-1]

    def get_player_color(self, player_username):
        if player_username == self.player_one:
            return "B"
        else:
            return "R"

    def set_next_turn(self, current_player):
        if current_player == self.player_one:
            self.turn = self.player_two
        else:
            self.turn = self.player_one

        return

    def do_turn(self, player_username, col):
        # do the turn
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
        self.game_board = []
        for i in range(0, 7):
            self.game_board.append([])
            for j in range(0, 7):
                self.game_board[i].append("-")
        return

    def get_able_line(self, x):
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
        if line > 6:
            return False

        return self.game_board[line][x] == '-'

