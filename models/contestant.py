import Config
import tools
from api_connector import get_accepted
from models.assistant import Assistant
from models.card import Card


class Contestant(Assistant):
	__CRYPT_ID = False
	__TYPE:str = 'Participant'
	__FIREBASE = None
	__FIRE_PATH:str = Config.DB_PATH_T if Config.TEST else Config.DB_PATH

	def __init__(self, id, data):
		super().__init__(id, Contestant.__TYPE)
		self.code = data['code']
		self.generate_qr()
		self.name = data['name']
		self.nick = '\"' + data['nickname'] + '\"'
		if Config.TEST:
			Contestant.__FIRE_PATH = Config.DB_PATH_T

	def generate_card(self, rgb_back=(255, 255, 255)):
		super().generate_card(rgb_back, Config.BAK_PATH_CONTESTANT)
		self.card.paste(self.qr, Card.QR_POS)
		tools.centrate_text_relative(self.card, " ".join(self.name.split(" ")[:2]).strip(), Config.BOLD_NAME_FONT, Card.NAME_POS, Card.QR_SIZE * 3, Config.WHITE_FONT_COLOR)
		self.smallen()

	# @staticmethod
	# def __firebase_init(cred):
	# 	if Contestant.__FIREBASE is None:
	# 		Contestant.__FIREBASE = firebase_admin.initialize_app(cred)
	# 	return Contestant.__FIREBASE

	@staticmethod
	def get_data(id=None, name=None):
		# cred = firebase_admin.credentials.Certificate(Config.DB_CERT_PATH)
		# Contestant.__firebase_init(cred)
		# db = firestore.client()
		# users_ref = db.collection(Contestant.__FIRE_PATH)
		# usrs = users_ref.stream()
		usrs = get_accepted()

		users = [
		    Contestant(usr['id'], usr) 
		    for usr in usrs 
		    if (
		        (id is None and name is None) 
		        or (id is not None and usr['id'] == id) 
		        or (name is not None and name == usr['name'])
		    )
		]

		return users
