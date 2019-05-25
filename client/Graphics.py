from Tkinter import *
from PIL import Image, ImageTk
import os
import sys
import API
import Game
import tkMessageBox

# Get an API handler, to contact the server
# We'll use that handler in Game and in Window classes
api = API.API()


class Window(Frame):
    """
    Window(Frame) class is our game GUI, and contains multiple "windows"
    We're doing so by changing the size, background and GUI elements being shown on the screen
    Inheriting from Tkinter's Frame class
    """
    def __init__(self, master=None):
        """
        Initilizing all the GUI variables required
        :param master: root Tk
        """
        Frame.__init__(self, master)

        self.master = master

        # Saving image references so garbage collector won't delete those
        self.image_refs = []

        # workdir for imgs
        self.imgs_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'imgs')

        # GUI elements lists
        self.login_gui_elements = []
        self.main_gui_elements = []
        self.game_gui_elements = []
        self.leaderboard_gui_elements = []

        # Login gui username and password entries
        self.login_entry_username = None
        self.login_entry_password = None

        # Game canvas and variables
        self.game_canvas = None
        self.game_status_line = None
        self.game_timer_label = None
        self.game = None
        self.game_col = None
        self.game_need_new_board = False

        # Board images
        self.p0_rect = None
        self.p1_rect = None
        self.p2_rect = None
        self.board_bg_img = None
        self.main_bg = None
        self.game_bg = None

        # Game status images
        self.game_status_imgs = {}
        self.init_game_status_imgs()

        # Init the window
        self.init_window()

    def init_game_status_imgs(self):
        """
        Initializing all the required status bar messages for the game itself
        :return: None
        """
        im = Image.open(os.path.join(self.imgs_path, 'game_closed.png'))
        resized = im.resize((600, 50), Image.ANTIALIAS)
        self.game_status_imgs["game_closed"] = ImageTk.PhotoImage(resized)

        im = Image.open(os.path.join(self.imgs_path, 'game_over.png'))
        resized = im.resize((600, 50), Image.ANTIALIAS)
        self.game_status_imgs["game_over"] = ImageTk.PhotoImage(resized)

        im = Image.open(os.path.join(self.imgs_path, 'joined_game.png'))
        resized = im.resize((600, 50), Image.ANTIALIAS)
        self.game_status_imgs["joined_game"] = ImageTk.PhotoImage(resized)

        im = Image.open(os.path.join(self.imgs_path, 'make_your_move.png'))
        resized = im.resize((600, 50), Image.ANTIALIAS)
        self.game_status_imgs["make_your_move"] = ImageTk.PhotoImage(resized)

        im = Image.open(os.path.join(self.imgs_path, 'no_free_space_in_this column.png'))
        resized = im.resize((600, 50), Image.ANTIALIAS)
        self.game_status_imgs["no_free_space_column"] = ImageTk.PhotoImage(resized)

        im = Image.open(os.path.join(self.imgs_path, 'waiting_for_a_player.png'))
        resized = im.resize((600, 50), Image.ANTIALIAS)
        self.game_status_imgs["waiting_for_player"] = ImageTk.PhotoImage(resized)

        im = Image.open(os.path.join(self.imgs_path, 'waiting_for_your_competitor.png'))
        resized = im.resize((600, 50), Image.ANTIALIAS)
        self.game_status_imgs["waiting_for_competitor"] = ImageTk.PhotoImage(resized)

        im = Image.open(os.path.join(self.imgs_path, 'you_lost.png'))
        resized = im.resize((600, 50), Image.ANTIALIAS)
        self.game_status_imgs["you_lost"] = ImageTk.PhotoImage(resized)

        im = Image.open(os.path.join(self.imgs_path, 'you_won.png'))
        resized = im.resize((600, 50), Image.ANTIALIAS)
        self.game_status_imgs["you_won"] = ImageTk.PhotoImage(resized)

    def init_window(self):
        """
        Initialize the main window and some board images
        :return:
        """
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
        """
        Get a list of GUI elements and destroy them
        :param elements: list of GUI TK elements
        :return: None
        """
        for element in elements:
            element.destroy()

    def create_board(self, board):
        """
        Takes a logical board, from API (from the server)
        Creates the corresponding images and draw them on the game canvas
        :param board: list of lists, representing game board
        """
        i = 5
        j = 0

        y = 0
        for i in xrange(5, -1, -1):
            x = 0
            for j in xrange(0, 7, 1):
                if board[i][j] == '-':
                    self.game_canvas.create_image(x, y, image=self.p0_rect, anchor='nw')
                elif board[i][j] == 'B':
                    self.game_canvas.create_image(x, y, image=self.p1_rect, anchor='nw')
                elif board[i][j] == 'R':
                    self.game_canvas.create_image(x, y, image=self.p2_rect, anchor='nw')
                x += 90
            y += 76

        self.game_canvas.create_image(0, 0, image=self.board_bg_img, anchor='nw')

    def game_gui(self):
        """
        Assemble game gui
        """
        self.master.geometry("800x600")

        # Background image
        im = Image.open(os.path.join(self.imgs_path, "bg_game.png"))
        resized = im.resize((800, 600), Image.ANTIALIAS)
        self.game_bg = ImageTk.PhotoImage(resized)

        # Configure background as canvas from (0,0) to (800,600)
        c = Canvas(self.master, width=800, height=600)
        c.create_image(0, 0, image=self.game_bg, anchor='nw')
        c.place(x=0, y=0)

        # Configure game status line
        self.game_status_line = Label(self.master)
        self.game_status_line.grid()

        # Configure pop-up game timer label (middle right of the screen)
        self.game_timer_label = Label(self.master, font=("Times", 22), bg="white")
        self.game_timer_label.grid(column=7)

        # Configure game canvas, and bind mouse click to game_board_click()
        self.game_canvas = Canvas(self.master, width=640, height=480)
        self.game_canvas.grid(row=1)
        self.game_canvas.bind("<Button-1>", self.game_board_click)

        # Configure game give up button
        im = Image.open(os.path.join(self.imgs_path, "button_giveup.png"))
        resized = im.resize((180, 39), Image.ANTIALIAS)
        giveup_button = Button(self.master, text="Give up!",
                               command=self.game_giveup_button_click)
        giveup_button.photo_ref = ImageTk.PhotoImage(resized)
        giveup_button.config(image=giveup_button.photo_ref, borderwidth=0, width=180, height=39)
        giveup_button.grid(row=2)

        # save gui elements for login gui
        self.game_gui_elements = [
            self.game_status_line,
            self.game_timer_label,
            self.game_canvas,
            giveup_button
        ]

    def main_gui(self):
        """
        Assemble main gui window - main menu
        """
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

        # Configure welcome and score labels
        label_welcome = Label(self.master, fg="red", font="Times",
                              text="Welcome {username}!".format(username=api.get_my_username()))
        label_welcome.grid(row=1, column=1)

        label_score = Label(self.master, fg="red", font="Times", text="Score: {score}!".format(score=api.get_my_score()))
        label_score.grid(row=2, column=1)

        # Configure play button
        im = Image.open(os.path.join(self.imgs_path, "button_play_bg.png"))
        resized = im.resize((180, 39), Image.ANTIALIAS)
        play_button = Button(self.master, fg="red",
                             command=self.main_play_button_click)
        play_button.photo_ref = ImageTk.PhotoImage(resized)
        play_button.config(image=play_button.photo_ref, borderwidth=0, width=180, height=39)
        play_button.grid(row=3, column=1)

        # Configure leaderboard button
        im = Image.open(os.path.join(self.imgs_path, "button_leaderboard_bg.png"))
        resized = im.resize((180, 39), Image.ANTIALIAS)
        leaderboard_button = Button(self.master, text="Leaderboard",
                                    command=self.main_leaderboard_button_click)
        leaderboard_button.photo_ref = ImageTk.PhotoImage(resized)
        leaderboard_button.config(image=leaderboard_button.photo_ref, borderwidth=0, width=180, height=39)
        leaderboard_button.grid(row=4, column=1)

        # Configure exit button
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
        """
        Assemble leaderboard window
        Show top 5 players
        :param leaderboard_arr: list of tuples, (name, score), first one is top 1
        """
        self.master.geometry("640x400")

        # Background canvas
        c = Canvas(self.master, width=640, height=400)
        c.create_image(0, 0, image=self.main_bg, anchor='nw')
        c.place(x=0, y=0)

        # Places labels
        place_1_label = Label(self.master, text=leaderboard_arr[0],
                              font=("Times", 22), bg="white")
        place_2_label = Label(self.master, text=leaderboard_arr[1],
                              font=("Times", 22), bg="white")
        place_3_label = Label(self.master, text=leaderboard_arr[2],
                              font=("Times", 22), bg="white")
        place_4_label = Label(self.master, text=leaderboard_arr[3],
                              font=("Times", 22), bg="white")
        place_5_label = Label(self.master, text=leaderboard_arr[4],
                              font=("Times", 22), bg="white")

        # Place them on the window itself
        place_1_label.grid(row=1, column=1)
        place_2_label.grid(row=2, column=1)
        place_3_label.grid(row=3, column=1)
        place_4_label.grid(row=4, column=1)
        place_5_label.grid(row=5, column=1)

        # Configure exit button
        im = Image.open(os.path.join(self.imgs_path, "button_exit_bg.png"))
        resized = im.resize((180, 39), Image.ANTIALIAS)
        exit_button = Button(self.master, text="Exit", fg="red", font="Times",
                             command=self.leaderboard_exit_button_click)
        exit_button.photo_ref = ImageTk.PhotoImage(resized)
        exit_button.config(image=exit_button.photo_ref, borderwidth=0, width=180, height=39)
        exit_button.grid(row=6, column=1)

        # Save refenrences to GUI elements
        self.leaderboard_gui_elements = [
            place_1_label, place_2_label, place_3_label,
            place_4_label, place_5_label,
            exit_button
        ]

    def login_gui(self):
        """
        Assemble login GUI window
        First window that will pop up to the user
        Can't go to the main window without proper login
        """
        self.master.geometry("240x100")

        # Labels and entires
        label_welcome = Label(self.master, text="Welcome aboard. Please log in")
        label_username = Label(self.master, text="Username")
        label_password = Label(self.master, text="Password")
        self.login_entry_username = Entry(self.master)
        self.login_entry_password = Entry(self.master, show="*")

        # Place them on the window itself
        label_welcome.grid(columnspan=2)
        label_username.grid(row=1, sticky=E)
        label_password.grid(row=2, sticky=E)
        self.login_entry_username.grid(row=1, column=1)
        self.login_entry_password.grid(row=2, column=1)

        # Login and register buttons
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
        """
        leaderboard exit button click
        removes the leaderboard GUI elements
        then go to main menu
        """
        self.gui_elements_remove(self.leaderboard_gui_elements)
        self.main_gui()

    def game_giveup_button_click(self):
        """
        Call the API and let the server know that the user closes the game
        Then remove the game gui elements from the window
        and move to the main menu
        """
        api.game_close()
        self.gui_elements_remove(self.game_gui_elements)
        self.main_gui()

    def main_leaderboard_button_click(self):
        """
        Go to the leaderboard window from the main menu
        :return:
        """
        arr = api.get_leaderboard()
        self.gui_elements_remove(self.main_gui_elements)
        self.leaderboard_gui(arr)

    def main_play_button_click(self):
        """
        Go to the game window form the main menu
        :return:
        """
        self.gui_elements_remove(self.main_gui_elements)
        self.game_gui()

        # Create a game
        self.game = Game.Game(api, self.game_status_line, self.game_status_imgs,
                              self.game_timer_label)
        # Loop until the game starts
        self.start_game_interval()

    def start_game_interval(self):
        """
        1. Trying to join a game
        2. On success, show a message box
            a. Get a board and display it
            b. Start a game interval, call game_interval()
        """
        # Try to join a game
        self.game.start_game()
        if not self.game.game_id:
            # Try that again in 1 sec
            self.after(1000, self.start_game_interval)
        else:
            # Found a matching game!
            tkMessageBox.showinfo("Four-in-a-row",
                                  "Starting game against " + self.game.another_player)
            self.game_need_new_board = True

            # For basic board render
            self.game.get_board()
            self.display_game_board()

            # Start the game itself
            self.game_interval()

    def game_interval(self):
        """
        Using Game class, we're playing!
        Handle Game's defines and states and show the corresponding data to the player
        """
        # Make a move and check the result
        status = self.game.game(self.game_col, self.game_need_new_board)
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
        """
        Display the board, after getting it
        """
        self.create_board(self.game.board)

    def game_board_click(self, event):
        """
        Detect which column have been clicked on the board itself
        :param event: Mouse click event
        """
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

        # DEBUG
        # print "click {x},{y}, col={col}".format(x=event.x, y=event.y, col=self.game_col)

    def main_exit_button_click(self):
        """
        Main menu exit button
        close the application
        """
        tkMessageBox.showinfo("Bye-bye", "Thank you! Exiting...")
        sys.exit()

    def login_login_button_click(self):
        """
        Get the username and password strings from the GUI
        Using the API, try to log in and get a cookie
        """
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
        """
        Get the username and password strings from the GUI
        Using the API, try to register
        """
        global api

        username = self.login_entry_username.get()
        password = self.login_entry_password.get()

        result = api.register(username, password)

        if result:
            tkMessageBox.showinfo("Four-in-a-row", "Great, please log in!")

        else:
            tkMessageBox.showerror("Four-in-a-row",
                                   "Bad registration")


def start_graphics():
    """
    Starting the game's GUI
    :return: None
    """

    # Create the window and the app
    root = Tk()
    root.geometry("650x480")
    root.resizable(0, 0)
    app = Window(root)

    # Call the login GUI
    app.login_gui()

    # Call TK's main loop
    root.mainloop()


