class Volunteer(Assistant):
	__ID = 1
	__LOGO_PATH = os.path.join(Config.RES_PATH, 'images', 'logogran.png')
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
		Tools.draw_text(self.card, self.name, Card.NAME_POS, Config.FONT)

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
