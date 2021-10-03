class Contestant(Assistant):
	__CRYPT_ID = False
	__TYPE = 'HACKER'
	__FIREBASE = None
	__FIRE_PATH = Config.DB_PATH

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
		Tools.draw_text(self.card, self.name, Card.NAME_POS, Config.FONT)
		Tools.draw_text(self.card, self.nick, Card.NICK_POS, Config.FONT)

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
			if (id is None and name is None) or (id is not None and usr.id == id) or (
					name is not None and name == usr.to_dict()['fullName']):
				users.append(Contestant(usr.id, usr.to_dict()))
			if Config.TEST or (id is not None and usr.id == id) or (
					name is not None and name == usr.to_dict()['fullName']):
				break
		return users
