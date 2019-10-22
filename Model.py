import os

import firebase_admin
from PIL import Image
from firebase_admin import firestore

import Constants
import Tools


class Card:
	QR_POS = (894, 120)
	QR_SIZE = 450
	QR_BORDER_SIZE = 0
	CARD_HEIGTH = 200
	CARD_WIDTH = 200
	TYPE_POS = (894, 980)
	NAME_POS = (894, 780)
	NICK_POS = (894, 850)


class Assistant(object):
	_DATA_FILE = os.path.join(Constants.RES_FOLDER, Constants.DATA_FILE)

	def __init__(self, id, type, name=None):
		self.id = id
		self.type = type
		self.name = name
		self.card = None

	def show(self):
		self.card.show()

	def save(self):
		self.card.save(os.path.join(Constants.OUT_FOLDER, self.id + '.png'))

	def generate_card(self, rgb_back=(255, 255, 255)):
		self.card = Image.open(os.path.join(Constants.RES_FOLDER, Constants.BAK_PATH))
		Tools.draw_text(self.card, self.type, Card.TYPE_POS)

	@staticmethod
	def get_data():
		return []


class Empresa(Assistant):
	ID = 1
	TYPE = ''
	__DATA = 'companies'

	def __init__(self, name):
		super().__init__('E' + str(Empresa.ID), Empresa.TYPE, name)
		Empresa.ID += 1

	def generate_card(self, rgb_back=(255, 255, 255)):
		super().generate_card(rgb_back)
		Tools.draw_text(self.card, self.name, Card.NAME_POS)

	@staticmethod
	def get_data():
		res = []
		data = Tools.DataFile.get_content(Empresa._DATA_FILE, 'JSON')
		for u in data[Empresa.__DATA]:
			for i in range(u['number_of_cards']):
				res.append(Empresa(u['name']))
		return res


class Voluntari(Assistant):
	ID = 1
	TYPE = 'VOLUNTARIADO'
	__DATA = 'volunteers'

	def __init__(self, name):
		super().__init__('V' + str(Voluntari.ID), Voluntari.TYPE, name)
		Voluntari.ID += 1

	def generate_card(self, rgb_back=(255, 255, 255)):
		super().generate_card(rgb_back)
		Tools.draw_text(self.card, self.name, Card.NAME_POS)

	@staticmethod
	def get_data():
		res = []
		data = Tools.DataFile.get_content(Voluntari._DATA_FILE, 'JSON')
		for u in data[Voluntari.__DATA]:
			res.append(Voluntari(u['name']))
		return res


class Organitzador(Assistant):
	ID = 1
	TYPE = 'ORGANIZACIÓN'
	__DATA = 'organizers'

	def __init__(self, name):
		super().__init__('O' + str(Organitzador.ID), Organitzador.TYPE, name)
		Voluntari.ID += 1

	def generate_card(self, rgb_back=(255, 255, 255)):
		super().generate_card(rgb_back)
		Tools.draw_text(self.card, self.name, Card.NAME_POS)

	@staticmethod
	def get_data():
		res = []
		filename = os.path.join(Constants.RES_FOLDER, Organitzador.__DATA)
		with open(filename, 'r') as file:
			content = file.read().splitlines()
		for o in content:
			res.append(Organitzador(o))
		return res


class Concursant(Assistant):
	CRYPT_ID = False
	TYPE = 'HACKER'

	def __init__(self, id, data):
		super().__init__(id, Concursant.TYPE)

		self.qr = Tools.generate_qr((self.id, Tools.crypt(self.id))[Concursant.CRYPT_ID], Card.QR_SIZE,
									Card.QR_BORDER_SIZE)
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
			users.append(Concursant(usr.id, usr.to_dict()))
		return users