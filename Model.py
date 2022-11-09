import os

import firebase_admin
from PIL import Image
from firebase_admin import firestore

import Config
import Tools

# expositor, organitzador o voluntari

class Card:
	QR_PIX_SIZE = 1
	QR_POS = (1301, 172)
	QR_SIZE = (723, 723)
	QR_BORDER_SIZE = 0
	TYPE_POS = (0, 500)
	# NAME_POS = (500, 1250)
	NAME_POS = (0, 330)
	COMP_NAME_POS = (0, 200)
	# LOGO_POS = (920, 250)
	# LOGO_SIZE = (550, 350)


class Assistant(object):
	__ID = 1
	__DATA = 'empty'
	_DATA_FILE = Config.DATA_PATH

	def __init__(self, id, type='', name=None):
		self.id = id
		self.type = type
		self.name = name
		self.card = None
		self.qr = None

	def show(self):
		self.card.show()

	def save(self):
		# self.card=Tools.scale(self.card, (410,265))
		# self.card=Tools.scale(self.card, (2188,1640))
		self.card.save(os.path.join(Config.OUT_PATH, self.id + '.png'))

	def generate_qr(self, crypt_id=False):
		self.qr = Tools.generate_qr((self.id, Tools.crypt(self.id))[crypt_id], Card.QR_PIX_SIZE, Card.QR_BORDER_SIZE)
		self.qr = Tools.scale(self.qr, Card.QR_SIZE, False)

	def generate_card(self, rgb_back=(255, 255, 255)):
		self.card = Image.open(Config.BAK_PATH)
		Tools.draw_text(self.card, self.type, Card.TYPE_POS, Config.TYPE_FONT, Config.FONT_COLOR)
		img = Image.new('RGB', (1062, 762),(255,255,255))
		img.paste(self.card, (0,0))
		self.card = img

	@staticmethod
	def get_data():
		data = Tools.DataFile.get_content(Assistant._DATA_FILE, 'JSON')
		num = data[Assistant.__DATA]
		res = []
		for _ in range(num):
			res.append(Assistant('A' + str(Assistant.__ID)))
			Assistant.__ID += 1
			if Config.TEST:
				break
		return res

class Volunteer(Assistant):
	__ID = 1
	__LOGO_PATH = os.path.join(Config.RES_PATH, 'editions', Config.EDITION, 'images', 'logogran.png')
	__TYPE = 'VOLUNTARI'
	__DATA = 'volunteers'

	def __init__(self):
		super().__init__('V' + str(Volunteer.__ID), Volunteer.__TYPE)
		Volunteer.__ID += 1

	def generate_card(self, rgb_back=(255, 255, 255)):
		super().generate_card(rgb_back)

	@staticmethod
	def get_data(name=None):
		pass

class Expositor(Assistant):
	__ID = 1
	# __LOGO_PATH = os.path.join(Config.RES_PATH, 'editions', Config.EDITION, 'images', 'logogran.png')
	__TYPE = 'EXPOSITOR'
	__DATA = 'companies'

	def __init__(self):
		super().__init__('E' + str(Expositor.__ID), Expositor.__TYPE)
		Expositor.__ID += 1

	def generate_card(self, rgb_back=(255, 255, 255)):
		super().generate_card(rgb_back)

	@staticmethod
	def get_data(name=None):
		pass

class Colaborator(Assistant):
	__ID = 1
	__TYPE = 'COL·LABORADOR'
	__DATA = 'companies'

	def __init__(self):
		super().__init__('C' + str(Colaborator.__ID), Colaborator.__TYPE)
		Colaborator.__ID += 1

	def generate_card(self, rgb_back=(255, 255, 255)):
		super().generate_card(rgb_back)

	@staticmethod
	def get_data(name=None):
		pass

class Organizer(Assistant):
	__ID = 1
	__TYPE = 'ORGANITZADOR'
	__DATA = 'companies'

	def __init__(self):
		super().__init__('O' + str(Organizer.__ID), Organizer.__TYPE)
		Organizer.__ID += 1

	def generate_card(self, rgb_back=(255, 255, 255)):
		super().generate_card(rgb_back)

	@staticmethod
	def get_data(name=None):
		pass