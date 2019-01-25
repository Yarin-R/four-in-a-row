from Tkinter import *
from PIL import Image, ImageTk
import os
import sys
import API
import Game
import tkMessageBox

api = API.API()


class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.image_refs = []
        self.login_gui_elements = []
        self.main_gui_elements = []
        self.game_gui_elements = []
        self.login_entry_username = None
        self.login_entry_password = None
        self.game_canvas = None

        # Board images
        self.p0_rect = None
        self.p1_rect = None
        self.p2_rect = None
        self.board_bg_img = None

        # Init the window
        self.init_window()

    def init_window(self):
        self.master.title("Four in a Row")

        # TODO set dynamically
        path = '/home/yarin/Desktop/four-in-a-row/client/imgs'

        # Create images for board
        im = Image.open(os.path.join(path, 'player1_rect.png'))
        resized = im.resize((90, 76), Image.ANTIALIAS)
        self.p1_rect = ImageTk.PhotoImage(resized)

        im = Image.open(os.path.join(path, 'player2_rect.png'))
        resized = im.resize((90, 76), Image.ANTIALIAS)
        self.p2_rect = ImageTk.PhotoImage(resized)

        im = Image.open(os.path.join(path, 'player0_rect.png'))
        resized = im.resize((90, 76), Image.ANTIALIAS)
        self.p0_rect = ImageTk.PhotoImage(resized)

        # board background
        im = Image.open(os.path.join(path, 'bg.png'))
        resized = im.resize((640, 457), Image.ANTIALIAS)
        tkimage = ImageTk.PhotoImage(resized)
        self.board_bg_img = tkimage

    def gui_elements_remove(self, elements):
        for element in elements:
            element.destroy()

    def create_board(self):

        # TODO demo, get a board and create the graphics for it as function
        b = True
        # loop
        for x in xrange(0, (640 / 7) * 6, 90):
            b = not b
            for y in xrange(0, (457 / 7) * 6, 76):
                if b:
                    self.game_canvas.create_image(x, y, image=self.p2_rect, anchor='nw')
                else:
                    self.game_canvas.create_image(x, y, image=self.p0_rect, anchor='nw')
                b = not b

        self.game_canvas.create_image(0, 0, image=self.board_bg_img, anchor='nw')

    def game_gui(self):
        self.master.geometry("800x600")

        label_status = Label(self.master, text="Status of the game!")
        label_status.grid()

        self.game_canvas = Canvas(self.master, width=640, height=480)
        self.game_canvas.grid(row=1)

        # todo apply command attribute
        giveup_button = Button(self.master, text="Give up!",
                               command=self.game_giveup_button_click)
        giveup_button.grid(row=2)

        # save gui elements for login gui
        self.game_gui_elements = [
            label_status,
            self.game_canvas,
            giveup_button
        ]

    def main_gui(self):
        self.master.geometry("240x100")

        label_welcome = Label(self.master, text="Welcome User!")

        label_welcome.grid()

        # todo apply command attribute
        play_button = Button(self.master, text="Play!",
                             command=self.main_play_button_click)
        play_button.grid(row=1)
        exit_button = Button(self.master, text="Exit",
                             command=self.main_exit_button_click)
        exit_button.grid(row=2)

        # save gui elements for login gui
        self.main_gui_elements = [
            label_welcome,
            play_button, exit_button
        ]

    def login_gui(self):
        self.master.geometry("240x100")

        label_welcome = Label(self.master, text="Welcome aboard. Please log in")
        label_username = Label(self.master, text="Username")
        label_password = Label(self.master, text="Password")
        self.login_entry_username = Entry(self.master)
        self.login_entry_password = Entry(self.master, show="*")

        label_welcome.grid(columnspan=2)
        label_username.grid(row=1, sticky=E)
        label_password.grid(row=2, sticky=E)
        self.login_entry_username.grid(row=1, column=1)
        self.login_entry_password.grid(row=2, column=1)

        # todo apply command attribute
        login_button = Button(self.master, text="Login",
                              command=self.login_login_button_click)
        login_button.grid(row=3, sticky=E)
        register_button = Button(self.master, text="Register",
                                 command=self.login_register_button_click)
        register_button.grid(row=3, column=1, sticky=W)

        # save gui elements for login gui
        self.login_gui_elements = [
            label_welcome, label_username, label_password,
            self.login_entry_username, self.login_entry_password,
            login_button, register_button
        ]

    def game_giveup_button_click(self):
        # just swapping to the main gui
        self.gui_elements_remove(self.game_gui_elements)
        self.main_gui()

    def main_play_button_click(self):
        self.gui_elements_remove(self.main_gui_elements)
        self.game_gui()

    def main_exit_button_click(self):
        tkMessageBox.showinfo("Bye-bye", "Thank you! Exiting...")
        #todo check about timer for that
        sys.exit()

    def login_login_button_click(self):
        global api

        username = self.login_entry_username.get()
        password = self.login_entry_password.get()

        result = api.log_in(username, password)

        if result:
            tkMessageBox.showinfo("Four-in-a-row", "Logged in!")
            self.gui_elements_remove(self.login_gui_elements)
            self.main_gui()

        else:
            tkMessageBox.showerror("Four-in-a-row",
                                   "Invalid username or password, exit...")

    def login_register_button_click(self):
        global api

        username = self.login_entry_username.get()
        password = self.login_entry_password.get()

        result = api.register(username, password)

        if result:
            tkMessageBox.showinfo("Four-in-a-row", "Great, please log in!")

        else:
            tkMessageBox.showerror("Four-in-a-row",
                                   "Bad registration")




    def player_one_turn(self, row, line):
        pass


def start_graphics():
    root = Tk()
    root.geometry("650x480")
    root.resizable(0, 0)
    app = Window(root)

    app.login_gui()
    root.mainloop()


start_graphics()
