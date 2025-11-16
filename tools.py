from base64 import b64decode
import hashlib
from io import BytesIO
import json
import os

import qrcode
from PIL import ImageDraw, Image
import requests
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


def draw_text(image, text, pos, font, fill, centrate=True, mayus=False):
	if mayus:
		text = text.upper()
	draw = ImageDraw.Draw(image)
	w = draw.textlength(text, font=font)
	# Center horizontally around pos[0] when centrate=True
	if centrate:
		x = pos[0] - (w / 2)
		ImageDraw.Draw(image).text((x, pos[1]), text, font=font, fill=fill)
	else:
		ImageDraw.Draw(image).text(pos, text, font=font, fill=fill)

def centrate_text_relative(image, text, font, relative_pos, relative_size, fill, mayus=False):
	#centrate relative on x and split in 2 lines if text width is bigger than relative_size
	if mayus:
		text = text.upper()
	draw = ImageDraw.Draw(image)
	w = draw.textlength(text, font=font)
	# center the text horizontally around relative_pos[0]
	x = relative_pos[0] - (w / 2)
	y = relative_pos[1]
	# if w > relative_size[0]:
	# 	#split in 2 lines
	# 	words = text.split(' ')
	# 	line1 = ''
	# 	line2 = ''
	# 	for word in words:
	# 		if draw.textsize(line1 + ' ' + word, font=font)[0] < relative_size[0]:
	# 			line1 += ' ' + word
	# 		else:
	# 			line2 += ' ' + word
	# 	x1 = relative_pos[0] + (relative_size[0] - draw.textsize(line1, font=font)[0]) / 2
	# 	x2 = relative_pos[0] + (relative_size[0] - draw.textsize(line2, font=font)[0]) / 2
	# 	draw.text((x1, y), line1, font=font)
	# 	draw.text((x2, y + h), line2, font=font)
	# else:
	ImageDraw.Draw(image).text((x, y), text, font=font, fill=fill)

def has_transparency(img):
    if img.info.get("transparency", None) is not None:
        return True
    if img.mode == "P":
        transparent = img.info.get("transparency", -1)
        for _, index in img.getcolors():
            if index == transparent:
                return True
    elif img.mode == "RGBA":
        extrema = img.getextrema()
        if extrema[3][0] < 255:
            return True

    return False

def scale(image, max_size, mask_col=Config.BAK_COLOR,method=Image.LANCZOS):
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
	back = Image.new("RGBA", max_size, mask_col)
	if has_transparency(image):
		try:
			back.paste(scaled, (int(offset[0]), int(offset[1])), scaled)
		except:
			scaled = scaled.convert("RGBA")
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


def translate_image(image) -> Image:
	# handle bytes directly
	if isinstance(image, (bytes, bytearray)):
		return Image.open(BytesIO(image))

	s = str(image)
	# remote URL
	if s[:4].lower() == "http":
		resp = requests.get(s, timeout=10)
		try:
			resp.raise_for_status()
		except Exception as e:
			raise RuntimeError(f"Failed to download image from URL {s}: {e}")

		ct = resp.headers.get('Content-Type', '').lower()
		content = resp.content

		# handle SVG responses specifically (PIL doesn't support SVG)
		if 'svg' in ct or (content.lstrip().startswith(b'<') and b'<svg' in content[:200].lower()):
			try:
				import cairosvg
				png_bytes = cairosvg.svg2png(bytestring=content)
				return Image.open(BytesIO(png_bytes))
			except Exception as e:
				# if the problem is missing native cairo library, provide a fallback placeholder image
				msg = str(e)
				if isinstance(e, OSError) or 'no library called' in msg.lower() or 'cannot load library' in msg.lower():
					# create a simple placeholder image (RGBA) so downstream code can continue
					placeholder = Image.new('RGBA', (200, 200), (220, 220, 220, 255))
					return placeholder
				# otherwise raise a descriptive error
				raise RuntimeError(f"Failed to convert SVG to PNG for {s}: {e}")

		# try to open the response content as an image
		try:
			return Image.open(BytesIO(content))
		except Exception:
			# provide useful debug info when PIL can't identify the bytes
			raise RuntimeError(f"Downloaded content from {s} is not a valid raster image (Content-Type: {ct})")

	# data URI (base64 or plain)
	if s.startswith('data:'):
		# split header and payload
		try:
			header, payload = s.split(',', 1)
		except Exception:
			raise RuntimeError('Invalid data URI format')

		is_base64 = ';base64' in header.lower()
		is_svg = 'svg' in header.lower()

		# get raw bytes (if not base64, treat payload as utf-8 text)
		try:
			data_bytes = b64decode(payload) if is_base64 else payload.encode('utf-8')
		except Exception as e:
			raise RuntimeError(f'Invalid base64 data in data URI: {e}')

		# if SVG, convert to PNG (cairosvg) or fallback
		if is_svg or (data_bytes.lstrip().startswith(b'<') and b'<svg' in data_bytes[:200].lower()):
			try:
				import cairosvg
				png_bytes = cairosvg.svg2png(bytestring=data_bytes)
				return Image.open(BytesIO(png_bytes))
			except Exception as e:
				msg = str(e)
				if isinstance(e, OSError) or 'no library called' in msg.lower() or 'cannot load library' in msg.lower():
					placeholder = Image.new('RGBA', (200, 200), (220, 220, 220, 255))
					return placeholder
				raise RuntimeError(f'Failed to convert SVG data URI to PNG: {e}')

		# otherwise try to open as raster image
		try:
			return Image.open(BytesIO(data_bytes))
		except Exception as e:
			raise RuntimeError(f'Invalid data URI image content: {e}')

	# local file path
	if os.path.exists(s):
		try:
			return Image.open(s)
		except Exception as e:
			raise RuntimeError(f"Found file {s} but PIL cannot open it as image: {e}")

	# try relative to current working directory
	possible = os.path.join(os.getcwd(), s)
	if os.path.exists(possible):
		try:
			return Image.open(possible)
		except Exception as e:
			raise RuntimeError(f"Found file {possible} but PIL cannot open it as image: {e}")

	raise FileNotFoundError(f"Image reference not recognized as URL, data URI, or existing file: {s}")