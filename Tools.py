import hashlib
import json
import os

import qrcode
from PIL import ImageDraw, Image
import Config


def create_dir(path):
	exists = os.path.isdir(path)
	if not exists:
		try:
			os.mkdir(path)
		except OSError:
			raise OSError('dir creation error')


def empty_dir(path, delete_files=True, delete_dirs=True):
	exists = os.path.isdir(path)
	if exists and (delete_files or delete_dirs):
		for root, dirs, files in os.walk(path):
			if delete_files:
				for file in files:
					os.remove(os.path.join(root, file))
			if delete_dirs:
				for dir in dirs:
					os.remove(os.path.join(root, dir))


def draw_text(image, text, pos, font, fill, centrate=True, mayus=True):
	if mayus:
		text = text.upper()
	draw = ImageDraw.Draw(image)
	w, h = draw.textsize(text, font=font)
	if centrate:
		ImageDraw.Draw(image).text(((image.width-w)/2, pos[1]), text, font=font,fill=fill)
	else:
		ImageDraw.Draw(image).text(pos, text, font=font,fill=fill)

def centrate_text_relative(image, text, font, relative_pos, relative_size, mayus=True):
	#centrate relative on x and split in 2 lines if text width is bigger than relative_size
	if mayus:
		text = text.upper()
	draw = ImageDraw.Draw(image)
	w, h = draw.textsize(text, font=font)
	x = relative_pos[0] + (relative_size[0] - w) / 2
	y = relative_pos[1]
	if w > relative_size[0]:
		#split in 2 lines
		words = text.split(' ')
		line1 = ''
		line2 = ''
		for word in words:
			if draw.textsize(line1 + ' ' + word, font=font)[0] < relative_size[0]:
				line1 += ' ' + word
			else:
				line2 += ' ' + word
		x1 = relative_pos[0] + (relative_size[0] - draw.textsize(line1, font=font)[0]) / 2
		x2 = relative_pos[0] + (relative_size[0] - draw.textsize(line2, font=font)[0]) / 2
		draw.text((x1, y), line1, font=font)
		draw.text((x2, y + h), line2, font=font)
	else:
		ImageDraw.Draw(image).text((x, y), text, font=font)

def scale(image, max_size, add_mask=True, method=Image.ANTIALIAS):
	"""
	resize 'image' to 'max_size' keeping the aspect ratio
	and place it in center of white 'max_size' image
	"""
	im_aspect = float(image.size[0]) / float(image.size[1])
	out_aspect = float(max_size[0]) / float(max_size[1])
	if im_aspect >= out_aspect:
		scaled = image.resize((max_size[0], int((float(max_size[0]) / im_aspect) + 0.5)), method)
	else:
		scaled = image.resize((int((float(max_size[1]) * im_aspect) + 0.5), max_size[1]), method)

	offset = (((max_size[0] - scaled.size[0]) / 2), ((max_size[1] - scaled.size[1]) / 2))
	back = Image.new("RGBA", max_size, Config.BAK_COLOR)
	if add_mask:
		back.paste(scaled, (int(offset[0]), int(offset[1])), scaled)
	else:
		back.paste(scaled, (int(offset[0]), int(offset[1])))
	return back

def generate_qr(input, size, border_size):
	qr = qrcode.QRCode(
		version=2,
		error_correction=qrcode.constants.ERROR_CORRECT_H,
		box_size=size,
		border=border_size)
	qr.add_data(input)
	qr.make(fit=True)
	qr = qr.make_image()
	return qr


def crypt(input, method='md5'):
	m = hashlib.new(method)
	m.update(bytes(input, 'utf'))
	return str(m.digest())


class DataFile:
	__contents = {}

	@staticmethod
	def get_content(filepath, type, reload_if_cached=False):
		if not reload_if_cached and filepath in DataFile.__contents:
			return DataFile.__contents[filepath]
		else:
			with open(filepath, 'r', encoding='utf-8') as json_file:
				if type == 'JSON':
					data = json.load(json_file)
					DataFile.__contents[filepath] = data
					return data
				else:
					raise Exception(NotImplemented)

	@staticmethod
	def clear_cached_content(filepath):
		if filepath in DataFile.__contents:
			del DataFile.__contents[filepath]
			return True
		else:
			return False

	@staticmethod
	def clear_cache():
		DataFile.__contents = {}
