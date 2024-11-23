import os
from PIL import Image
import Config
import tools
from models.assistant import Assistant
from models.card import Card


class Organizer(Assistant):
	__ID:int = 1
	__LOGO_PATH:str = os.path.join(Config.RES_PATH, 'editions', Config.EDITION, 'images', 'logogran.png')
	__TYPE:str = 'Staff'
	__DATA:str = 'organizers'

	def __init__(self, name):
		super().__init__('O' + str(Organizer.__ID), Organizer.__TYPE, name)
		Organizer.__ID += 1

	def generate_card(self, rgb_back=(255, 255, 255)):
		self.card = Image.open(Config.BAK_PATH_STAFF)
		tools.draw_text(self.card, self.type, Card.TYPE_POS, Config.TYPE_FONT, Config.DARK_FONT_COLOR)
		if self.type == '':
			self.smallen()
		image = Image.open(Organizer.__LOGO_PATH).convert("RGBA")
		image = tools.scale(image, Card.QR_SIZE)
		self.card.paste(image, Card.QR_POS)
		tools.centrate_text_relative(self.card, " ".join(self.name.split(" ")[:2]).strip(),Config.BOLD_NAME_FONT, Card.NAME_POS, Card.QR_SIZE * 3, Config.DARK_FONT_COLOR)
		# Tools.draw_text(self.card, self.name, Card.NAME_POS, Config.NAME_FONT, Config.WHITE_FONT_COLOR, False)
		self.smallen()

	@staticmethod
	def get_data(name=None):
		res = []
		data = tools.DataFile.get_content(Organizer._DATA_FILE, 'JSON')
		for u in data[Organizer.__DATA]:
			if name is None or u['name'] == name:
				res.append(Organizer(u['name']))
			if Config.TEST or (name is not None and u['name'] == name):
				break
		return res