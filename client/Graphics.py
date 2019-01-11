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
        self.image_refs = []

    def init_window(self):
        self.master.title("Four in a Row")

    def create_board(self):

        path = '/home/yarin/Desktop/four-in-a-row/client/imgs'
        c = Canvas(self.master, width=640, height=480)
        c.grid()



        # player1
        im = Image.open(os.path.join(path, 'player1_rect.png'))
        resized = im.resize((90, 76), Image.ANTIALIAS)
        p1_rect = ImageTk.PhotoImage(resized)
        self.image_refs.append(p1_rect)

        im = Image.open(os.path.join(path, 'player2_rect.png'))
        resized = im.resize((90, 76), Image.ANTIALIAS)
        p2_rect = ImageTk.PhotoImage(resized)
        self.image_refs.append(p2_rect)

        im = Image.open(os.path.join(path, 'player0_rect.png'))
        resized = im.resize((90, 76), Image.ANTIALIAS)
        p0_rect = ImageTk.PhotoImage(resized)
        self.image_refs.append(p0_rect)

        #c.create_image(0, 0, image=tkimage, anchor='nw')
        b = True
        # loop
        for x in xrange(0, (640 / 7) * 6, 90):
            b = not b
            for y in xrange(0, (457 / 7) * 6, 76):
                if b:
                    c.create_image(x, y, image=p1_rect, anchor='nw')
                else:
                    c.create_image(x, y, image=p0_rect, anchor='nw')
                b = not b
        #"""
        # background
        im = Image.open(os.path.join(path, 'bg.png'))
        resized = im.resize((640, 457), Image.ANTIALIAS)
        tkimage = ImageTk.PhotoImage(resized)
        self.image_refs.append(tkimage)
        c.create_image(0, 0, image=tkimage, anchor='nw')
        #"""





        """
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
        """



    def player_one_turn(self, row, line):
        pass


root = Tk()
root.geometry("650x480")
root.resizable(0, 0)
app = Window(root)

app.create_board()

root.mainloop()
