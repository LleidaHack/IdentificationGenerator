import os
from PIL import Image
from config.settings import settings
from config.paths import paths
from config.constants import DARK_FONT_COLOR
import tools
from models.assistant import Assistant
from models.card import Card


class Organizer(Assistant):
	__ID:int = 1
	__LOGO_PATH:str = os.path.join(paths.res_path, 'editions', settings.EDITION, 'images', 'logogran.png')
	__TYPE:str = 'Staff'
	__DATA:str = 'organizers'

	def __init__(self, name):
		super().__init__('O' + str(Organizer.__ID), Organizer.__TYPE, name)
		Organizer.__ID += 1

	def generate_card(self, rgb_back=(255, 255, 255)):
		self.card = Image.open(paths.bak_path_staff)
		tools.draw_text(self.card, self.type, Card.TYPE_POS, paths.type_font, DARK_FONT_COLOR)
		if self.type == '':
			self.smallen()
		image = Image.open(Organizer.__LOGO_PATH).convert("RGBA")
		image = tools.scale(image, Card.QR_SIZE)
		self.card.paste(image, Card.QR_POS)
		tools.centrate_text_relative(self.card, " ".join(self.name.split(" ")[:2]).strip(), paths.bold_name_font, Card.NAME_POS, Card.QR_SIZE * 3, DARK_FONT_COLOR)
		# Tools.draw_text(self.card, self.name, Card.NAME_POS, Config.NAME_FONT, Config.WHITE_FONT_COLOR, False)
		self.smallen()

	@staticmethod
	def get_data(name=None):
		res = []
		data = tools.DataFile.get_content(Organizer._DATA_FILE, 'JSON')
		for u in data[Organizer.__DATA]:
			if name is None or u['name'] == name:
				res.append(Organizer(u['name']))
			if settings.TEST or (name is not None and u['name'] == name):
				break
		return res