import os

import firebase_admin
from PIL import Image
from firebase_admin import firestore

import Constants
import Tools


class Card:
	QR_PIX_SIZE = 1
	QR_POS = (1202, 156)
	# QR_POS = (1221, 176)
	QR_SIZE = (617, 617)
	# QR_SIZE = (580, 580)
	QR_BORDER_SIZE = 0
	TYPE_POS = (1198, 970)
	NAME_POS = (1198, 800)
	NICK_POS = (1198, 870)
	LOGO_POS = (920, 250)
	LOGO_SIZE = (550, 350)


class Assistant(object):
	__ID = 1
	__DATA = 'empty'
	_DATA_FILE = os.path.join(Constants.RES_FOLDER, Constants.DATA_FILE)

	def __init__(self, id, type='', name=None):
		self.id = id
		self.type = type
		self.name = name
		self.card = None
		self.qr = None

	def show(self):
		self.card.show()

	def save(self):
		self.card.save(os.path.join(Constants.OUT_FOLDER, self.id + '.png'))

	def generate_qr(self, crypt_id=False):
		self.qr = Tools.generate_qr((self.id, Tools.crypt(self.id))[crypt_id], Card.QR_PIX_SIZE, Card.QR_BORDER_SIZE)
		self.qr = Tools.scale(self.qr, Card.QR_SIZE, False)

	def generate_card(self, rgb_back=(255, 255, 255)):
		self.card = Image.open(os.path.join(Constants.RES_FOLDER, Constants.BAK_PATH))
		Tools.draw_text(self.card, self.type, Card.TYPE_POS)

	@staticmethod
	def get_data():
		data = Tools.DataFile.get_content(Assistant._DATA_FILE, 'JSON')
		num = data[Assistant.__DATA]
		res = []
		for i in range(num):
			res.append(Assistant('A' + str(Assistant.__ID)))
			Assistant.__ID += 1
			if Constants.TEST:
				break
		return res


class Guest(Assistant):
	__ID = 1
	__TYPE = 'INVITADO'
	__DATA = 'guests'

	def __init__(self, name, mtype=None, has_qr=False):
		super().__init__('G' + str(Guest.__ID), (mtype, Guest.__TYPE)[mtype is None], name)
		Guest.__ID += 1
		self.has_qr = has_qr
		if has_qr:
			self.generate_qr(True)

	def generate_card(self, rgb_back=(255, 255, 255)):
		super().generate_card(rgb_back)
		if self.has_qr:
			self.card.paste(self.qr, Card.QR_POS)
		Tools.draw_text(self.card, self.name, Card.NAME_POS)

	@staticmethod
	def get_data():
		res = []
		data = Tools.DataFile.get_content(Guest._DATA_FILE, 'JSON')
		for u in data[Guest.__DATA]:
			res.append(Guest(u['name'], u['type'], u['qr']))
			if Constants.TEST:
				break
		return res


class Company(Assistant):
	__ID = 1
	__TYPE = ''
	__DATA = 'companies'

	def __init__(self, name, image):
		super().__init__('C' + str(Company.__ID), Company.__TYPE, name)
		Company.__ID += 1
		self.logopath = os.path.join(Constants.RES_FOLDER, 'images', image)

	def generate_card(self, rgb_back=(255, 255, 255)):
		super().generate_card(rgb_back)
		Tools.draw_text(self.card, self.name, Card.NAME_POS)
		image = Image.open(self.logopath).convert("RGBA")  # .resize((550,350), Image.ANTIALIAS)
		image = Tools.scale(image, Card.QR_SIZE)
		self.card.paste(image, Card.QR_POS)

	@staticmethod
	def get_data():
		res = []
		data = Tools.DataFile.get_content(Company._DATA_FILE, 'JSON')
		for u in data[Company.__DATA]:
			for i in range(u['number_of_cards']):
				res.append(Company(u['name'], u['logo']))
				if Constants.TEST:
					break
			if Constants.TEST:
				break
		return res


class Volunteer(Assistant):
	__ID = 1
	__LOGO_PATH = os.path.join(Constants.RES_FOLDER, 'images', 'logogran.png')
	__TYPE = 'VOLUNTARIA/O'
	__DATA = 'volunteers'

	def __init__(self, name):
		super().__init__('V' + str(Volunteer.__ID), Volunteer.__TYPE, name)
		Volunteer.__ID += 1

	def generate_card(self, rgb_back=(255, 255, 255)):
		super().generate_card(rgb_back)
		image = Image.open(Volunteer.__LOGO_PATH).convert("RGBA")
		image = Tools.scale(image, Card.QR_SIZE)
		self.card.paste(image, Card.QR_POS)
		Tools.draw_text(self.card, self.name, Card.NAME_POS)

	@staticmethod
	def get_data():
		res = []
		data = Tools.DataFile.get_content(Volunteer._DATA_FILE, 'JSON')
		for u in data[Volunteer.__DATA]:
			res.append(Volunteer(u['name']))
			if Constants.TEST:
				break
		return res


class Organizer(Assistant):
	__ID = 1
	__LOGO_PATH = os.path.join(Constants.RES_FOLDER, 'images', 'logogran.png')
	__TYPE = 'ORGANIZACIÓN'
	__DATA = 'organizers'

	def __init__(self, name):
		super().__init__('O' + str(Organizer.__ID), Organizer.__TYPE, name)
		Organizer.__ID += 1

	def generate_card(self, rgb_back=(255, 255, 255)):
		super().generate_card(rgb_back)
		image = Image.open(Organizer.__LOGO_PATH).convert("RGBA")
		image = Tools.scale(image, Card.QR_SIZE)
		self.card.paste(image, Card.QR_POS)
		Tools.draw_text(self.card, self.name, Card.NAME_POS)

	@staticmethod
	def get_data():
		res = []
		data = Tools.DataFile.get_content(Organizer._DATA_FILE, 'JSON')
		for u in data[Organizer.__DATA]:
			res.append(Organizer(u['name']))
			if Constants.TEST:
				break
		return res


class Contestant(Assistant):
	__CRYPT_ID = False
	__TYPE = 'HACKER'

	def __init__(self, id, data):
		super().__init__(id, Contestant.__TYPE)

		self.generate_qr()
		self.name = data['fullName']
		self.nick = '\"' + data['nickname'] + '\"'

	def generate_card(self, rgb_back=(255, 255, 255)):
		super().generate_card(rgb_back)
		self.card.paste(self.qr, Card.QR_POS)
		Tools.draw_text(self.card, self.name, Card.NAME_POS)
		Tools.draw_text(self.card, self.nick, Card.NICK_POS)

	@staticmethod
	def get_data(cert):
		cred = firebase_admin.credentials.Certificate(cert)
		firebase_admin.initialize_app(cred)
		db = firestore.client()
		users_ref = db.collection(Constants.DB_PATH)
		usrs = users_ref.stream()
		users = []
		for usr in usrs:
			users.append(Contestant(usr.id, usr.to_dict()))
			if Constants.TEST:
				break
		return users
