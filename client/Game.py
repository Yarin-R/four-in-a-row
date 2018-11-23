import API
import time

class Game:
    def __init__(self, api):
        self.board = []
        self.api = api
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
                    return
                else:
                    time.sleep(3)


    def game(self):
        while True:
            self.display_board()
            col = int(raw_input("Enter Column: "))
            # send to api the requresed column
            # get back the new board game
            # board, isWin = api.getGameStatus()
            # if isWin:
            #   break
    
    def display_board(self):
        print "BOARD"
        return