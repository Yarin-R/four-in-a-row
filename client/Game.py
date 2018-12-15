import time
import pprint


class Game:
    def __init__(self, api):
        self.board = []
        self.api = api
        self.game_id = False
        self.another_player = False
        return
    
    def start_game(self):
        result, game_id = self.api.start_game()
        if result:
            print "Join game! " + str(game_id)
            return

        else:
            while True:
                print "Waiting for players..."
                result, game_id = self.api.join_game()
                if result:
                    print "Join game! " + str(game_id)
                    self.game_id = game_id
                    return
                else:
                    time.sleep(3)

    def set_board(self, board):
        board_lines = board.split(",")
        self.board = []
        for i in xrange(len(board_lines)):
            self.board.append(list(board_lines[i]))
        return

    def game(self):
        print "Starting game against " + self.api.game_get_competitor()
        while True:
            if self.api.game_get_turn():
                is_winner, data = self.api.game_get_board()
                if is_winner:
                    print "Winner is " + data
                    return
                else:
                    self.set_board(data)

                print "It's your turn, go ahead:"
                self.display_board()
                try:
                    col = int(raw_input("Enter Column: "))

                except Exception:
                    print "Invalid choice, try again..."
                    continue

                if self.api.game_do_turn(int(col)) == "OK":
                    print "Okay"
                else:
                    print "No space left, try another column..."
            else:
                # not my turn
                time.sleep(0.5)
                print "Waiting for your competitor..."
                # trying again...
    
    def display_board(self):
        # todo Reverse!
        pprint.pprint(self.board)
        return
