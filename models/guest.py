import os
from config.settings import settings
from config.paths import paths
from config.constants import DARK_FONT_COLOR
from models.card import Card
import tools
from models.assistant import Assistant
from PIL import Image

class Guest(Assistant):
	__ID:int = 1
	__TYPE:str = 'Convidat'
	__DATA:str = 'guests'

	def __init__(self, name:str, mtype:str='', logo:str='', has_qr:bool=False):
		super().__init__('HackEPS_Guest_' + str(Guest.__ID), (mtype, Guest.__TYPE)[mtype == ''], name)
		Guest.__ID += 1
		self.has_qr = has_qr
		self.logo = logo
		if has_qr:
			self.generate_qr(True)
		if not logo == '':
			self.logopath = os.path.join(paths.res_path, settings.EDITIONS_FOLDER, settings.EDITION, 'images', logo)

	def generate_card(self, rgb_back=(255, 255, 255)):
		self.card = Image.open(paths.bak_path_staff)
		tools.draw_text(self.card, self.type, Card.TYPE_POS, paths.type_font, DARK_FONT_COLOR)
		if self.type == '':
			self.smallen()
		if self.logo != '':
			logo = Image.open(self.logopath).convert("RGBA")
			logo = tools.scale(logo, Card.QR_SIZE)
			self.card.paste(logo, Card.QR_POS)
		elif self.has_qr:
			self.card.paste(self.qr, Card.QR_POS)
		if self.name != '':
			tools.centrate_text_relative(self.card, " ".join(self.name.split(" ")[:2]).strip(), paths.bold_name_font, Card.NAME_POS, Card.QR_SIZE * 3, DARK_FONT_COLOR)
		self.smallen()

	@staticmethod
	def get_data(name=None):
		res = []
		data = tools.DataFile.get_content(Guest._DATA_FILE, 'JSON')
		for u in data[Guest.__DATA]:
			if name is None or u['name'] == name:
				res.append(Guest(u['name'], u['type'], u['logo'], u['qr']))
			if settings.TEST or (name is not None and u['name'] == name):
				break
		return res