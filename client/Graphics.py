from Tkinter import *
from PIL import Image, ImageTk
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600


class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.init_window()

    def init_window(self):
        self.master.title("Four in a Row")

    def create_board(self):
        im = Image.open('circle.png')
        resized = im.resize((230, 216), Image.ANTIALIAS)
        tkimage = ImageTk.PhotoImage(resized)

        board = []
        for i in xrange(7):
            line = []
            for j in xrange(7):
                l = Label(self.master, image=tkimage)
                l.grid(row=i, column=j)
                line.append(l)
            board.append(line)

        return board
    def player_one_turn(self, row, line):


root = Tk()
root.geometry("2100x1500")
root.resizable(0, 0)
app = Window(root)

app.create_board()

root.mainloop()
