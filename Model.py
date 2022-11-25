import os

import firebase_admin
from PIL import Image
from firebase_admin import firestore

import Config
import Tools


class Card:
	QR_PIX_SIZE = 1
	QR_POS = (450, 78)
	_QR_SIZE = 267
	QR_SIZE = (_QR_SIZE, _QR_SIZE)
	QR_BORDER_SIZE = 0
	TYPE_POS = (0, 475)
	NAME_POS = (QR_POS[0], 370)
	NICK_POS = (1198, 870)


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

	def show(self):
		self.card.show()

	def save(self):
		self.card.save(os.path.join(Config.OUT_PATH, str(self.id) + '.png'))

	def generate_qr(self, crypt_id=False):
		self.qr = Tools.generate_qr(self.id, Card.QR_PIX_SIZE, Card.QR_BORDER_SIZE)
		self.qr = Tools.scale(self.qr, Card.QR_SIZE, False)

	def generate_card(self, rgb_back=(255, 255, 255)):
		self.card = Image.open(Config.BAK_PATH)
		Tools.draw_text(self.card, self.type, Card.TYPE_POS, Config.TYPE_FONT, Config.WHITE_FONT_COLOR)
		if self.type == '':
			self.smallen()

	def smallen(self):
		blank = Image.new('RGB', (1082, 782),(255,255,255))
		blank.paste(self.card, (0, 0))
		self.card = blank

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


class Guest(Assistant):
	__ID:int = 1
	__TYPE:str = 'CONVIDAT'
	__DATA:str = 'guests'

	def __init__(self, name:str, mtype:str='', logo:str='', has_qr:bool=False):
		super().__init__('HackEPS_Guest_' + str(Guest.__ID), (mtype, Guest.__TYPE)[mtype is ''], name)
		Guest.__ID += 1
		self.has_qr = has_qr
		self.logo = logo
		if has_qr:
			self.generate_qr(True)
		if not logo == '':
			self.logopath = os.path.join(Config.RES_PATH, Config.EDITIONS_FOLDER, Config.EDITION, 'images', logo)

	def generate_card(self, rgb_back=(255, 255, 255)):
		super().generate_card(rgb_back)
		if self.logo is not '':
			logo = Image.open(self.logopath).convert("RGBA")
			logo = Tools.scale(logo, Card.QR_SIZE)
			self.card.paste(logo, Card.QR_POS)
		elif self.has_qr:
			self.card.paste(self.qr, Card.QR_POS)
		if self.name is not '':
			Tools.centrate_text_relative(self.card, self.name,Config.NAME_FONT, Card.NAME_POS, Card.QR_SIZE)
		self.smallen()

	@staticmethod
	def get_data(name=None):
		res = []
		data = Tools.DataFile.get_content(Guest._DATA_FILE, 'JSON')
		for u in data[Guest.__DATA]:
			if name is None or u['name'] == name:
				res.append(Guest(u['name'], u['type'], u['logo'], u['qr']))
			if Config.TEST or (name is not None and u['name'] == name):
				break
		return res


class Company(Assistant):
	__ID:int = 1
	__TYPE:str = 'EMPRESSA'
	__DATA:str = 'companies'

	def __init__(self, name:str, image):
		super().__init__('C' + str(Company.__ID), Company.__TYPE, name)
		Company.__ID += 1
		self.logopath = os.path.join(Config.RES_PATH, Config.EDITIONS_FOLDER, Config.EDITION, 'images', image)

	def generate_card(self, rgb_back=(255, 255, 255)):
		super().generate_card(rgb_back)
		image = Image.open(self.logopath).convert("RGBA")  # .resize((550,350), Image.ANTIALIAS)
		image = Tools.scale(image, Card.QR_SIZE)
		self.card.paste(image, Card.QR_POS)
		Tools.centrate_text_relative(self.card, self.name,Config.NAME_FONT, Card.NAME_POS, Card.QR_SIZE)
		self.smallen()

	@staticmethod
	def get_data(name=None):
		res = []
		data = Tools.DataFile.get_content(Company._DATA_FILE, 'JSON')
		for u in data[Company.__DATA]:
			for _ in range(u['number_of_cards']):
				if name is None or u['name'] == name:
					res.append(Company(u['name'], u['logo']))
				if Config.TEST:
					break
			if Config.TEST or (name is not None and u['name'] == name):
				break
		return res


class Volunteer(Assistant):
	__ID:int = 1
	__LOGO_PATH:str = os.path.join(Config.RES_PATH, 'editions', Config.EDITION, 'images', 'logogran.png')
	__TYPE:str = 'VOLUNTARI/A'
	__DATA:str = 'volunteers'

	def __init__(self, name:str):
		super().__init__('V' + str(Volunteer.__ID), Volunteer.__TYPE, name)
		Volunteer.__ID += 1

	def generate_card(self, rgb_back=(255, 255, 255)):
		super().generate_card(rgb_back)
		image = Image.open(Volunteer.__LOGO_PATH).convert("RGBA")
		image = Tools.scale(image, Card.QR_SIZE)
		self.card.paste(image, Card.QR_POS)
		Tools.centrate_text_relative(self.card, self.name,Config.NAME_FONT, Card.NAME_POS, Card.QR_SIZE)
		self.smallen()

	@staticmethod
	def get_data(name=None):
		res = []
		data = Tools.DataFile.get_content(Volunteer._DATA_FILE, 'JSON')
		for u in data[Volunteer.__DATA]:
			if name is None or name == u['name']:
				res.append(Volunteer(u['name']))
			if Config.TEST or (name is not None and name == u['name']):
				break
		return res

class Mentor(Assistant):
	__ID:int = 1
	__LOGO_PATH:str = os.path.join(Config.RES_PATH, 'editions', Config.EDITION, 'images', 'logogran.png')
	__TYPE:str = 'MENTOR/A'
	__DATA:str = 'mentors'

	def __init__(self, name:str):
		super().__init__('M' + str(Mentor.__ID), Mentor.__TYPE, name)
		Mentor.__ID += 1

	def generate_card(self, rgb_back=(255, 255, 255)):
		super().generate_card(rgb_back)
		image = Image.open(Mentor.__LOGO_PATH).convert("RGBA")
		image = Tools.scale(image, Card.QR_SIZE)
		self.card.paste(image, Card.QR_POS)
		Tools.centrate_text_relative(self.card, self.name,Config.NAME_FONT, Card.NAME_POS, Card.QR_SIZE)
		self.smallen()

	@staticmethod
	def get_data(name=None):
		res = []
		data = Tools.DataFile.get_content(Mentor._DATA_FILE, 'JSON')
		for u in data[Mentor.__DATA]:
			if name is None or name == u['name']:
				res.append(Mentor(u['name']))
			if Config.TEST or (name is not None and name == u['name']):
				break
		return res

class Organizer(Assistant):
	__ID:int = 1
	__LOGO_PATH:str = os.path.join(Config.RES_PATH, 'editions', Config.EDITION, 'images', 'logogran.png')
	__TYPE:str = 'ORGANIZACIÓ'
	__DATA:str = 'organizers'

	def __init__(self, name):
		super().__init__('O' + str(Organizer.__ID), Organizer.__TYPE, name)
		Organizer.__ID += 1

	def generate_card(self, rgb_back=(255, 255, 255)):
		super().generate_card(rgb_back)
		image = Image.open(Organizer.__LOGO_PATH).convert("RGBA")
		image = Tools.scale(image, Card.QR_SIZE)
		self.card.paste(image, Card.QR_POS)
		Tools.centrate_text_relative(self.card, self.name,Config.NAME_FONT, Card.NAME_POS, Card.QR_SIZE)
		# Tools.draw_text(self.card, self.name, Card.NAME_POS, Config.NAME_FONT, Config.WHITE_FONT_COLOR, False)
		self.smallen()

	@staticmethod
	def get_data(name=None):
		res = []
		print(Organizer._DATA_FILE)
		data = Tools.DataFile.get_content(Organizer._DATA_FILE, 'JSON')
		for u in data[Organizer.__DATA]:
			if name is None or u['name'] == name:
				res.append(Organizer(u['name']))
			if Config.TEST or (name is not None and u['name'] == name):
				break
		return res


class Contestant(Assistant):
	__CRYPT_ID = False
	__TYPE:str = 'HACKER'
	__FIREBASE = None
	__FIRE_PATH:str = Config.DB_PATH_T if Config.TEST else Config.DB_PATH

	def __init__(self, id, data):
		super().__init__(id, Contestant.__TYPE)
		self.generate_qr()
		self.name = data['fullName']
		self.nick = '\"' + data['nickname'] + '\"'
		if Config.TEST:
			Contestant.__FIRE_PATH = Config.DB_PATH_T

	def generate_card(self, rgb_back=(255, 255, 255)):
		super().generate_card(rgb_back)
		self.card.paste(self.qr, Card.QR_POS)
		Tools.centrate_text_relative(self.card, self.name,Config.NAME_FONT, Card.NAME_POS, Card.QR_SIZE)
		self.smallen()

	@staticmethod
	def __firebase_init(cred):
		if Contestant.__FIREBASE is None:
			Contestant.__FIREBASE = firebase_admin.initialize_app(cred)
		return Contestant.__FIREBASE

	@staticmethod
	def get_data(id=None, name=None):
		cred = firebase_admin.credentials.Certificate(Config.DB_CERT_PATH)
		Contestant.__firebase_init(cred)
		db = firestore.client()
		users_ref = db.collection(Contestant.__FIRE_PATH)
		usrs = users_ref.stream()
		users = []
		for usr in usrs:
			if ((id is None and name is None) 
				or (id is not None and usr.id == id) 
				or (name is not None and name == usr.to_dict()['fullName'])):
				users.append(Contestant(usr.id, usr.to_dict()))
		return users
