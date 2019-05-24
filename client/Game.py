import pprint
import API
import time

class Game:
    def __init__(self, api, game_status_line, game_status_imgs, game_timer_label):
        self.board = []
        self.api = api
        self.game_id = None
        self.another_player = None
        self.game_status_line = game_status_line
        self.game_status_imgs = game_status_imgs
        self.game_timer_label = game_timer_label
        self.time_wait = None
        return

    def print_time(self, text):
        try:
            if text is None:
                self.game_timer_label["text"] = ""
            else:
                self.game_timer_label["text"] = "{time}s".format(time=text)
        except Exception as e:
            print "print_timer exception: " + e.message

    def print_status(self, text):
        try:
            print text
            self.game_status_line.config(image=self.game_status_imgs[text], borderwidth=0, width=600, height=50)
            self.game_status_line.image = self.game_status_imgs[text]

        except Exception as e:
            print "print_status exception: {}".format(e.message)

    def start_game(self):
        self.game_id = None
        result, game_id = self.api.start_game()
        if result:
            self.print_status("joined_game")
            self.game_id = game_id
            self.another_player = self.api.game_get_competitor()
            return

        else:
            self.print_status("waiting_for_player")
            result, game_id = self.api.join_game()
            if result:
                self.print_status("joined_game")
                self.game_id = game_id
                self.another_player = self.api.game_get_competitor()
                return

    def set_board(self, board):
        board_lines = board.split(",")
        self.board = []
        for i in xrange(len(board_lines)):
            self.board.append(list(board_lines[i]))
        return

    def get_board(self):
        is_winner, data = self.api.game_get_board(ignore_winner=True)
        self.set_board(data)

    def printable_time_left(self):
        max_time = 59
        diff_time = int(round(time.time() - self.time_wait))
        # For now, max is 59 seconds
        if diff_time > max_time:
            self.api.game_close()
            raise API.GameClosedException("TIME_UP")
        else:
            return max_time - diff_time

    def game(self, col=None, need_new_board=True):
        # print "Starting game against " + self.api.game_get_competitor()
        try:
            if self.api.game_get_turn():
                winner, data = self.api.game_get_board()
                self.set_board(data)
                if winner:
                    if winner == self.another_player:
                        self.print_status("you_lost")
                    else:
                        self.print_status("you_won")
                    return "WINNER"

                if need_new_board:
                    self.print_status("make_your_move")
                    self.time_wait = time.time()
                    return "DISPLAY"

                if col is None:
                    self.print_status("make_your_move")
                    self.print_time(self.printable_time_left())
                    return "PLAY"
                else:
                    if self.api.game_do_turn(int(col)) == "OK":
                        self.print_time(None)
                        self.print_status("waiting_for_competitor")
                        self.get_board()
                        return "WAIT"
                    else:
                        self.print_status("no_free_space_column")
                        return "PLAY"

            else:
                # not my turn
                self.print_status("waiting_for_competitor")
                # Sleep in graphics class

                return "WAIT"
                # trying again...
        except API.GameClosedException as e:
            if e.message.split(',')[0] == "WINNING":
                excp_message = e.message.split(',')
                if len(excp_message) == 2:
                    winner = excp_message[1]
                else:
                    winner = e.message

                # print winner
                if winner == self.another_player:
                    self.print_status("you_lost")
                else:
                    self.print_status("you_won")
                return "WINNER"
            else:
                self.print_status("game_closed")
                return "CLOSED"

    def display_board(self):
        #pprint.pprint(self.board)
        return
