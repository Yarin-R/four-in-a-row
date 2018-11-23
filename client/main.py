import Game
import API

api = API.API()

def loop():
    global api

    while True:
        print "Welcome!"
        print "1) Get current playing games"
        print "2) Leaderboard"
        print "3) Start playing!"
        print "4) Exit!"

        try:
            choice = int(raw_input("Enter your choice: "))
        except ValueError:
            print "Not a valid choice, try again"
            continue

        if choice == 1:
            print "playing games..."
            continue

        elif choice == 2:
            print "Leaderboard"
            continue

        elif choice == 3:
            print "waiting for a free game room"
            g = Game.Game(api)
            g.start_game()
            continue

        elif choice == 4:
            print "Thanks"
            return

        else:
            print "Not a valid choice, try again"



def main():
    global api
    # Log in
    username = raw_input("Enter username:")
    password = raw_input("Enter password:")
    result = api.log_in(username, password)

    if result:
        print "Logged in!"
        loop()
    else:
        print "Invalid username or password, exit..."


if __name__ == '__main__':
    main()
