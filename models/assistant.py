
import os

import Config
from models.card import Card
import tools

from PIL import Image

class Assistant(object):
	__ID:int = 1
	__DATA:str = 'empty'
	_DATA_FILE:str = Config.DATA_PATH

	def __init__(self, id:str, type:str='', name:str=None):
		self.id = id
		self.type = type
		self.name = name
		self.card = None
		self.qr = None
		self.code = None

	def show(self):
		self.card.show()

	def save(self):
		self.card.save(os.path.join(Config.OUT_PATH, str(self.id) + '.png'))

	def generate_qr(self, crypt_id=False):
		if self.code:
			self.qr = tools.generate_qr(self.code, Card.QR_PIX_SIZE, Card.QR_BORDER_SIZE)
		else:
			self.qr = tools.generate_qr(self.id, Card.QR_PIX_SIZE, Card.QR_BORDER_SIZE)
		self.qr = tools.scale(self.qr, Card.QR_SIZE, False)

	def generate_card(self, rgb_back=(255, 255, 255), template=Config.BAK_PATH_CONTESTANT):
		self.card = Image.open(template)
		tools.draw_text(self.card, self.type, Card.TYPE_POS, Config.TYPE_FONT, Config.WHITE_FONT_COLOR)
		if self.type == '':
			self.smallen()

	def smallen(self):
		return
		blank = Image.new('RGB', (1082, 782),(255,255,255))
		blank.paste(self.card, (0, 0))
		self.card = blank

	@staticmethod
	def get_data():
		data = tools.DataFile.get_content(Assistant._DATA_FILE, 'JSON')
		num = data[Assistant.__DATA]
		res = []
		for _ in range(num):
			res.append(Assistant('A' + str(Assistant.__ID)))
			Assistant.__ID += 1
			if Config.TEST:
				break
		return res
