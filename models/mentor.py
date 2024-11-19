import os
import Config
import tools
from models.assistant import Assistant
from models.card import Card

from PIL import Image


class Mentor(Assistant):
	__ID:int = 1
	__LOGO_PATH:str = os.path.join(Config.RES_PATH, 'editions', Config.EDITION, 'images', 'logogran.png')
	__TYPE:str = 'Mentor/a'
	__DATA:str = 'mentors'

	def __init__(self, name:str):
		super().__init__('M' + str(Mentor.__ID), Mentor.__TYPE, name)
		Mentor.__ID += 1

	def generate_card(self, rgb_back=(255, 255, 255)):
		self.card = Image.open(Config.BAK_PATH_STAFF)
		tools.draw_text(self.card, self.type, Card.TYPE_POS, Config.TYPE_FONT, Config.DARK_FONT_COLOR)
		if self.type == '':
			self.smallen()
		image = Image.open(Mentor.__LOGO_PATH).convert("RGBA")
		image = tools.scale(image, Card.QR_SIZE)
		self.card.paste(image, Card.QR_POS)
		tools.centrate_text_relative(self.card, " ".join(self.name.split(" ")[:2]).strip(),Config.BOLD_NAME_FONT, Card.NAME_POS, Card.QR_SIZE * 3, Config.DARK_FONT_COLOR)
		self.smallen()

	@staticmethod
	def get_data(name=None):
		res = []
		data = tools.DataFile.get_content(Mentor._DATA_FILE, 'JSON')
		for u in data[Mentor.__DATA]:
			if name is None or name == u['name']:
				res.append(Mentor(u['name']))
			if Config.TEST or (name is not None and name == u['name']):
				break
		return res