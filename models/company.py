import base64
import os
import Config

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
		print("Generating card for company:", self.name)
		self.card = Image.open(Config.BAK_PATH_EMPRESA)
		tools.draw_text(self.card, self.type, Card.TYPE_POS, Config.TYPE_FONT, Config.DARK_FONT_COLOR)
		if self.type == '':
			self.smallen()
		image = tools.translate_image(self.logo)
		image = tools.scale(image, Card.QR_SIZE)
		self.card.paste(image, Card.QR_POS)
		tools.centrate_text_relative(self.card, self.name.strip(),Config.BOLD_NAME_FONT, Card.NAME_POS, Card.QR_SIZE * 3, Config.DARK_FONT_COLOR)
		self.smallen()
