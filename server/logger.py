"""
Using logging module to implement our logging system
"""
import logging


class Logger:
	"""
	Simple logger class, using the original python-ic logger module
	"""
	def __init__(self, log_class):
		"""
		Initializing Logger members
		:param log_class: shared log_class
		"""
		self.log_class = log_class

		# Configure the required format, save to server.log
		logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', level=logging.DEBUG, filename="server.log")
		logging.getLogger().addHandler((logging.StreamHandler()))

	def info(self, msg):
		"""
		Logging
		:param msg: Message to log
		"""
		logging.info("[{0}] {1}".format(self.log_class, msg))

	def debug(self, msg):
		"""
		Logging
		:param msg: Message to log
		"""
		logging.debug("[{0}] {1}".format(self.log_class, msg))

	def warning(self, msg):
		"""
		Logging
		:param msg: Message to log
		"""
		logging.warning("[{0}] {1}".format(self.log_class, msg))

	def error(self, msg):
		"""
		Logging
		:param msg: Message to log
		"""
		logging.error("[{0}] {1}".format(self.log_class, msg))

	def critical(self, msg):
		"""
		Logging
		:param msg: Message to log
		"""
		logging.critical("[{0}] {1}".format(self.log_class, msg))
