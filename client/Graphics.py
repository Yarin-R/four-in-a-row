from Tkinter import *
from PIL import Image, ImageTk
import os
import sys
import API
import Game
import tkMessageBox
import pprint

api = API.API()


class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.image_refs = []
        self.imgs_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'imgs')
        self.login_gui_elements = []
        self.main_gui_elements = []
        self.game_gui_elements = []
        self.leaderboard_gui_elements = []
        self.login_entry_username = None
        self.login_entry_password = None
        self.game_canvas = None
        self.game_status_line = None
        self.game = None
        self.game_col = None
        self.game_need_new_board = False

        # Board images
        self.p0_rect = None
        self.p1_rect = None
        self.p2_rect = None
        self.board_bg_img = None
        self.main_bg = None

        # Init the window
        self.init_window()

    def init_window(self):
        self.master.title("Four in a Row")

        # Create images for board
        # Blue
        im = Image.open(os.path.join(self.imgs_path, 'player1_rect.png'))
        resized = im.resize((90, 76), Image.ANTIALIAS)
        self.p1_rect = ImageTk.PhotoImage(resized)

        # Red
        im = Image.open(os.path.join(self.imgs_path, 'player2_rect.png'))
        resized = im.resize((90, 76), Image.ANTIALIAS)
        self.p2_rect = ImageTk.PhotoImage(resized)

        im = Image.open(os.path.join(self.imgs_path, 'player0_rect.png'))
        resized = im.resize((90, 76), Image.ANTIALIAS)
        self.p0_rect = ImageTk.PhotoImage(resized)

        # board background
        im = Image.open(os.path.join(self.imgs_path, 'bg.png'))
        resized = im.resize((640, 457), Image.ANTIALIAS)
        tkimage = ImageTk.PhotoImage(resized)
        self.board_bg_img = tkimage

    def gui_elements_remove(self, elements):
        for element in elements:
            element.destroy()

    def create_board(self, board):
        i = 5
        j = 0

        pprint.pprint(board)

        y = 0
        for i in xrange(5, -1, -1):
            x = 0
            for j in xrange(0, 7, 1):
                if board[i][j] == '-':
                    self.game_canvas.create_image(x, y, image=self.p0_rect, anchor='nw')
                    # print "{i}.{j},{x},{y},{c}".format(i=i, j=j, x=x, y=y, c=board[i][j])
                elif board[i][j] == 'B':
                    self.game_canvas.create_image(x, y, image=self.p1_rect, anchor='nw')
                    # print "{i}.{j},{x},{y},{c}".format(i=i, j=j, x=x, y=y, c=board[i][j])
                elif board[i][j] == 'R':
                    self.game_canvas.create_image(x, y, image=self.p2_rect, anchor='nw')
                    # print "{i}.{j},{x},{y},{c}".format(i=i, j=j, x=x, y=y, c=board[i][j])
                x += 90
            y += 76

        self.game_canvas.create_image(0, 0, image=self.board_bg_img, anchor='nw')

    def game_gui(self):
        self.master.geometry("800x600")

        self.game_status_line = Label(self.master, text="Status of the game!")
        self.game_status_line.grid()

        self.game_canvas = Canvas(self.master, width=640, height=480)
        self.game_canvas.grid(row=1)
        self.game_canvas.bind("<Button-1>", self.game_board_click)

        giveup_button = Button(self.master, text="Give up!",
                               command=self.game_giveup_button_click)
        giveup_button.grid(row=2)

        # save gui elements for login gui
        self.game_gui_elements = [
            self.game_status_line,
            self.game_canvas,
            giveup_button
        ]

    def main_gui(self):
        self.master.geometry("640x400")

        # board background
        im = Image.open(os.path.join(self.imgs_path, "bg_main.png"))
        resized = im.resize((640, 400), Image.ANTIALIAS)
        self.main_bg = ImageTk.PhotoImage(resized)
        c = Canvas(self.master, width=640, height=400)
        c.create_image(0, 0, image=self.main_bg, anchor='nw')
        c.place(x=0, y=0)

        # configure grid
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_rowconfigure(6, weight=1)
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_columnconfigure(2, weight=1)

        label_welcome = Label(self.master, fg="red", font="Times",
                              text="Welcome {username}!".format(username=api.get_my_username()))
        label_welcome.grid(row=1, column=1)

        label_score = Label(self.master, fg="red", font="Times", text="Score: {score}!".format(score=api.get_my_score()))
        label_score.grid(row=2, column=1)

        im = Image.open(os.path.join(self.imgs_path, "button_play_bg.png"))
        resized = im.resize((180, 39), Image.ANTIALIAS)

        play_button = Button(self.master, fg="red",
                             command=self.main_play_button_click)
        play_button.photo_ref = ImageTk.PhotoImage(resized)
        play_button.config(image=play_button.photo_ref, borderwidth=0, width=180, height=39)
        play_button.grid(row=3, column=1)

        im = Image.open(os.path.join(self.imgs_path, "button_leaderboard_bg.png"))
        resized = im.resize((180, 39), Image.ANTIALIAS)
        leaderboard_button = Button(self.master, text="Leaderboard",
                                    command=self.main_leaderboard_button_click)
        leaderboard_button.photo_ref = ImageTk.PhotoImage(resized)
        leaderboard_button.config(image=leaderboard_button.photo_ref, borderwidth=0, width=180, height=39)
        leaderboard_button.grid(row=4, column=1)

        im = Image.open(os.path.join(self.imgs_path, "button_exit_bg.png"))
        resized = im.resize((180, 39), Image.ANTIALIAS)
        exit_button = Button(self.master, text="Exit", fg="red", font="Times",
                             command=self.main_exit_button_click)
        exit_button.photo_ref = ImageTk.PhotoImage(resized)
        exit_button.config(image=exit_button.photo_ref, borderwidth=0, width=180, height=39)
        exit_button.grid(row=5, column=1)



        # save gui elements for login gui
        self.main_gui_elements = [
            c,
            label_welcome,
            label_score,
            leaderboard_button,
            play_button, exit_button
        ]

    def leaderboard_gui(self, leaderboard_arr):
        self.master.geometry("800x600")

        label_title = Label(self.master, text="Leaderboard")
        label_title.grid(row=1)
        place_1_label = Label(self.master, text=leaderboard_arr[0])
        place_2_label = Label(self.master, text=leaderboard_arr[1])
        place_3_label = Label(self.master, text=leaderboard_arr[2])
        place_4_label = Label(self.master, text=leaderboard_arr[3])
        place_5_label = Label(self.master, text=leaderboard_arr[4])

        place_1_label.grid(row=2)
        place_2_label.grid(row=3)
        place_3_label.grid(row=4)
        place_4_label.grid(row=5)
        place_5_label.grid(row=6)

        exit_button = Button(self.master, text="Exit",
                             command=self.leaderboard_exit_button_click)
        exit_button.grid(row=7)

        self.leaderboard_gui_elements = [
            label_title,
            place_1_label, place_2_label, place_3_label,
            place_4_label, place_5_label,
            exit_button
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

    def leaderboard_exit_button_click(self):
        self.gui_elements_remove(self.leaderboard_gui_elements)
        self.main_gui()

    def game_giveup_button_click(self):
        # just swapping to the main gui
        api.game_close()
        self.gui_elements_remove(self.game_gui_elements)
        self.main_gui()

    def main_leaderboard_button_click(self):
        arr = api.get_leaderboard()
        self.gui_elements_remove(self.main_gui_elements)
        self.leaderboard_gui(arr)

    def main_play_button_click(self):
        self.gui_elements_remove(self.main_gui_elements)
        self.game_gui()

        # Create a game
        self.game = Game.Game(api, self.game_status_line)
        # Loop until the game starts
        self.start_game_interval()

    def start_game_interval(self):
        # Try to join a game
        self.game.start_game()
        if not self.game.game_id:
            self.after(1000, self.start_game_interval)
        else:
            tkMessageBox.showinfo("Four-in-a-row",
                                  "Starting game against " + self.game.another_player)
            self.game_need_new_board = True

            # For basic board render
            self.game.get_board()
            self.display_game_board()

            self.game_interval()

    def game_interval(self):
        status = self.game.game(self.game_col, self.game_need_new_board)
        print status
        if status == "WINNER":
            self.display_game_board()
            tkMessageBox.showinfo("Four-in-a-row",
                                  "Game Completed!")
        elif status == "DISPLAY":
            self.display_game_board()
            self.game_need_new_board = False
            self.after(300, self.game_interval)
        elif status == "WAIT":
            self.display_game_board()
            self.game_col = None
            self.game_need_new_board = True
            self.after(300, self.game_interval)
        elif status == "PLAY":
            self.after(300, self.game_interval)
        elif status == "CLOSED":
            tkMessageBox.showinfo("Four-in-a-row",
                                  "Game have been closed!")

    def display_game_board(self):
        self.create_board(self.game.board)

    def game_board_click(self, event):
        # Set the right clicked col
        if 0 <= event.x < 95:
            self.game_col = 0
        elif 95 <= event.x < 188:
            self.game_col = 1
        elif 188 <= event.x < 277:
            self.game_col = 2
        elif 277 <= event.x < 367:
            self.game_col = 3
        elif 367 <= event.x < 457:
            self.game_col = 4
        elif 457 <= event.x < 547:
            self.game_col = 5
        elif 547 <= event.x:
            self.game_col = 6

        print "click {x},{y}, col={col}".format(x=event.x, y=event.y, col=self.game_col)

    def main_exit_button_click(self):
        tkMessageBox.showinfo("Bye-bye", "Thank you! Exiting...")
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
