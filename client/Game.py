class Game:
    def __init__(self):
        self.board = []
        return
    
    
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