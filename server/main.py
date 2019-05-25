"""
Main module
Calling main() function
"""

from listener import Listener
import sys


def main():
	"""
	main function
	Creates the main Listener and calls listen()
	Catches the last exception and exit upon that
	:return: Program returned value
	"""
	l = Listener()
	try:
		l.listen()
	except Exception as e:
		print "Server main() exception: {}".format(e)
		sys.exit()


if __name__ == "__main__":
	main()
