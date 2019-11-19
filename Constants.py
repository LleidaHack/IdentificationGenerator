import os
from PIL import ImageFont

TEST = True
if TEST:
	# dev or prod
	ENVIROMENT = 'dev'
else:
	ENVIROMENT = 'prod'

DB_PATH = 'hackeps-2019/' + ENVIROMENT + '/users'

OUT_FOLDER = '_out_'
RES_FOLDER = 'resources'
DATA_FILE = 'data.json'
DB_CERT = '2019_firebase_cert.json'
BAK_PATH = 'plantilla.png'
FONT = ImageFont.truetype(os.path.join(RES_FOLDER, 'arial.ttf'), 60)
