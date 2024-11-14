import os
import Config
import tools
from models.assistant import Assistant

from PIL import Image

from models.card import Card

class Company(Assistant):
	__ID:int = 1
	__TYPE:str = 'Empresa'
	__DATA:str = 'companies'

	def __init__(self, name:str, image):
		super().__init__('C' + str(Company.__ID), Company.__TYPE, name)
		Company.__ID += 1
		self.logopath = os.path.join(Config.RES_PATH, Config.EDITIONS_FOLDER, Config.EDITION, 'images', image)

	def generate_card(self, rgb_back=(255, 255, 255)):
		super().generate_card(rgb_back, Config.BAK_PATH_EMPRESA)
		image = Image.open(self.logopath).convert("RGBA")  # .resize((550,350), Image.ANTIALIAS)
		image = tools.scale(image, Card.QR_SIZE)
		self.card.paste(image, Card.QR_POS)
		tools.centrate_text_relative(self.card, " ".join(self.name.split(" ")[:2]).strip(),Config.BOLD_NAME_FONT, Card.NAME_POS, Card.QR_SIZE * 3, Config.DARK_FONT_COLOR)
		self.smallen()

	@staticmethod
	def get_data(name=None):
		res = []
		data = tools.DataFile.get_content(Company._DATA_FILE, 'JSON')
		for u in data[Company.__DATA]:
			for _ in range(u['number_of_cards']):
				if name is None or u['name'] == name:
					res.append(Company(u['name'], u['logo']))
				if Config.TEST:
					break
			if Config.TEST or (name is not None and u['name'] == name):
				break
		return res