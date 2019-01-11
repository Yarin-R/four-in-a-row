from Tkinter import *
from PIL import Image, ImageTk
import os

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

        path = '/home/yarin/Desktop/four-in-a-row/client/imgs'

        # background
        im = Image.open(os.path.join(path, 'bg.png'))
        resized = im.resize((450, 450), Image.ANTIALIAS)
        tkimage = ImageTk.PhotoImage(resized)
        l = Label(self.master)
        l.image = tkimage
        l.configure(image=l.image)
        l.place(x=0, y=0)

        im = Image.open(os.path.join(path, 'player1.png'))
        resized = im.resize((64, 64), Image.ANTIALIAS)
        tkimage = ImageTk.PhotoImage(resized)

        board = []
        for i in xrange(7):
            line = []
            for j in xrange(7):
                l = Label(self.master)
                l.image = tkimage
                l.configure(image=l.image)
                l.grid(row=i, column=j)
                line.append(l)
            board.append(line)

        return board



    def player_one_turn(self, row, line):
        pass


root = Tk()
root.geometry("640x480")
root.resizable(0, 0)
app = Window(root)

app.create_board()

root.mainloop()
