import logging


class Logger:
	def __init__(self, log_class):
		self.log_class = log_class
		logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', level=logging.DEBUG, filename="server.log")
		logging.getLogger().addHandler((logging.StreamHandler()))

	def info(self, msg):
		logging.info("[{0}] {1}".format(self.log_class, msg))

	def debug(self, msg):
		logging.debug("[{0}] {1}".format(self.log_class, msg))

	def warning(self, msg):
		logging.warning("[{0}] {1}".format(self.log_class, msg))

	def error(self, msg):
		logging.error("[{0}] {1}".format(self.log_class, msg))

	def critical(self, msg):
		logging.critical("[{0}] {1}".format(self.log_class, msg))
