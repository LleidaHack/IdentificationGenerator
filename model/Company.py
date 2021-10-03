class Company(Assistant):
	__ID = 1
	__TYPE = ''
	__DATA = 'companies'

	def __init__(self, name, image):
		super().__init__('C' + str(Company.__ID), Company.__TYPE, name)
		Company.__ID += 1
		self.logopath = os.path.join(Config.RES_PATH, 'images', image)

	def generate_card(self, rgb_back=(255, 255, 255)):
		super().generate_card(rgb_back)
		Tools.draw_text(self.card, self.name, Card.NAME_POS, Config.FONT)
		image = Image.open(self.logopath).convert("RGBA")  # .resize((550,350), Image.ANTIALIAS)
		image = Tools.scale(image, Card.QR_SIZE)
		self.card.paste(image, Card.QR_POS)

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
