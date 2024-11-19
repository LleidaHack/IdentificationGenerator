import base64
import os
import Config
from api_connector import get_by_tier
import requests
from io import BytesIO
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
		self.logo = image

	def generate_card(self, rgb_back=(255, 255, 255)):
		self.card = Image.open(Config.BAK_PATH_EMPRESA)
		tools.draw_text(self.card, self.type, Card.TYPE_POS, Config.TYPE_FONT, Config.DARK_FONT_COLOR)
		if self.type == '':
			self.smallen()
		image = tools.translate_image(self.logo)
		image = tools.scale(image, Card.QR_SIZE, mask_col=(255,204,77))
		self.card.paste(image, Card.QR_POS)
		tools.centrate_text_relative(self.card, " ".join(self.name.split(" ")[:2]).strip(),Config.BOLD_NAME_FONT, Card.NAME_POS, Card.QR_SIZE * 3, Config.DARK_FONT_COLOR)
		self.smallen()

	@staticmethod
	def get_data(name=None):
		res = []
		#data = tools.DataFile.get_content(Company._DATA_FILE, 'JSON')
		tier1=get_by_tier(1)
		for comp in tier1:
			for _ in range(8):
				if name is None or comp['name'] == name:
					res.append(Company(comp['name'], comp['image']))
				if Config.TEST:
					break
			if Config.TEST or (name is not None and comp['name'] == name):
				break
	
		tier2=get_by_tier(2)
		for comp in tier2:
			for _ in range(5):
				if name is None or comp['name'] == name:
					res.append(Company(comp['name'], comp['image']))
				if Config.TEST:
					break
			if Config.TEST or (name is not None and comp['name'] == name):
				break
		return res