import API

class Player:
	def __init__(self):
		self.playerid = 0
		self.name = ""
		self.score = 0

	def refresh_player_info():
		API.get_player_info(self.playerid)