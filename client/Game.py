import pprint
import API


class Game:
    def __init__(self, api, game_status_line):
        self.board = []
        self.api = api
        self.game_id = None
        self.another_player = None
        self.game_status_line = game_status_line
        return

    def print_status(self, text):
        self.game_status_line["text"] = text
    
    def start_game(self):
        self.game_id = None
        result, game_id = self.api.start_game()
        if result:
            self.print_status("Join game! " + str(game_id))
            self.game_id = game_id
            self.another_player = self.api.game_get_competitor()
            return

        else:
            self.print_status("Waiting for players")
            result, game_id = self.api.join_game()
            if result:
                self.print_status("Join game! " + str(game_id))
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

    def game(self, col=None, need_new_board=True):
        # print "Starting game against " + self.api.game_get_competitor()
        try:
            if self.api.game_get_turn():
                winner, data = self.api.game_get_board()
                self.set_board(data)
                if winner:
                    self.print_status("Winner is " + winner)
                    return "WINNER"

                if need_new_board:
                    self.print_status("It's your turn")
                    return "DISPLAY"

                if col is None:
                    self.print_status("Please make a move")
                    return "PLAY"
                else:
                    if self.api.game_do_turn(int(col)) == "OK":
                        self.print_status("Great move.")
                        self.get_board()
                        return "WAIT"
                    else:
                        self.print_status("No space left, try another column...")
                        return "PLAY"

            else:
                # not my turn
                self.print_status("Waiting for your competitor...")
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
                self.print_status('{winner} won the game!'.format(winner=winner))
                return "WINNER"
            else:
                self.print_status('Game closed because {0}'.format(e.message))
                return "CLOSED"
            # TODO handle game close in graphics
            # TODO another message if winning, etc...
    
    def display_board(self):
        # todo Reverse!
        pprint.pprint(self.board)
        return
