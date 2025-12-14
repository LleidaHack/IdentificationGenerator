from config.settings import settings
from config.paths import paths
from config.constants import WHITE_FONT_COLOR
import tools

from models.assistant import Assistant
from models.card import Card


class Contestant(Assistant):
	__CRYPT_ID = False
	__TYPE:str = 'Participant'
	__FIREBASE = None
	__FIRE_PATH:str = settings.db_path

	def __init__(self, id, data):
		super().__init__(id, Contestant.__TYPE)
		self.code = data['code']
		self.generate_qr()
		self.name = data['name']
		self.nick = '\"' + data['nickname'] + '\"'

	def generate_card(self, rgb_back=(255, 255, 255)):
		super().generate_card(rgb_back, paths.bak_path_contestant)
		self.card.paste(self.qr, Card.QR_POS)
		tools.centrate_text_relative(self.card, " ".join(self.name.split(" ")[:2]).strip(), paths.bold_name_font, Card.NAME_POS, Card.QR_SIZE * 3, WHITE_FONT_COLOR)
		self.smallen()

	# @staticmethod
	# def __firebase_init(cred):
	# 	if Contestant.__FIREBASE is None:
	# 		Contestant.__FIREBASE = firebase_admin.initialize_app(cred)
	# 	return Contestant.__FIREBASE


