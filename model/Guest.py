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
		Tools.draw_text(self.card, self.name, Card.NAME_POS, Config.FONT)

	@staticmethod
	def get_data(name=None):
		res = []
		data = Tools.DataFile.get_content(Guest._DATA_FILE, 'JSON')
		for u in data[Guest.__DATA]:
			if name is None or u['name'] == name:
				res.append(Guest(u['name'], u['type'], u['qr']))
			if Config.TEST or (name is not None and u['name'] == name):
				break
		return res