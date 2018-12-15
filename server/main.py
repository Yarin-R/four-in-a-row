from listener import Listener
import sys


def main():
	l = Listener()
	try:
		l.listen()
	except Exception as e:
		print e
		sys.exit()


if __name__ == "__main__":
	main()
