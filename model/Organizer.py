class Organizer(Assistant):
	__ID = 1
	__LOGO_PATH = os.path.join(Config.RES_PATH, 'images', 'logogran.png')
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
		Tools.draw_text(self.card, self.name, Card.NAME_POS, Config.FONT)

	@staticmethod
	def get_data(name=None):
		res = []
		data = Tools.DataFile.get_content(Organizer._DATA_FILE, 'JSON')
		for u in data[Organizer.__DATA]:
			if name is None or u['name'] == name:
				res.append(Organizer(u['name']))
			if Config.TEST or (name is not None and u['name'] == name):
				break
		return res