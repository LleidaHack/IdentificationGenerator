import hashlib
import json

import qrcode
from PIL import ImageDraw, ImageFont

import Constants


def draw_text(image, text, pos, font=Constants.FONT):
	ImageDraw.Draw(image).text((pos[0], pos[1]), text, (95, 36, 147), font=font)


def generate_qr(input, size, border_size):
	qr = qrcode.QRCode(
		version=1,
		error_correction=qrcode.constants.ERROR_CORRECT_H,
		box_size=int(size / 25),
		border=border_size)
	qr.add_data(input)
	qr.make(fit=True)
	return qr.make_image()


def crypt(input, method='md5'):
	m = hashlib.new(method)
	m.update(bytes(input, 'utf'))
	return str(m.digest())


class DataFile:
	__contents = {}

	@staticmethod
	def get_content(filepath, type):
		if filepath in DataFile.__contents:
			return DataFile.__contents[filepath]
		else:
			with open(filepath, 'r') as json_file:
				if type == 'JSON':
					data = json.load(json_file)
					DataFile.__contents[filepath] = data
					return data
				else:
					raise Exception(NotImplemented)
	@staticmethod
	def clear_cached_content(filepath):
		if filepath in DataFile.__contents:
			return True
		else:
			return False
	@staticmethod
	def clear_cache():
		DataFile.__contents={}