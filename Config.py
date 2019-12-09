from os import path
from PIL import ImageFont

TEST = False

DB_PATH_T = 'hackeps-2019/dev/users'
DB_PATH = 'hackeps-2019/prod/users'

EDITION='2019'
EDITIONS_FOLDER = 'editions'

OUT_FOLDER = '_out_'
OUT_PATH = path.join('.', OUT_FOLDER)

RES_FOLDER = 'resources'
RES_PATH = path.join('.', RES_FOLDER)

DATA_FILE = 'data.json'
DATA_PATH = path.join(RES_PATH, EDITIONS_FOLDER, EDITION, DATA_FILE)

DB_CERT = '2019_firebase_cert.json'
DB_CERT_PATH = path.join(RES_PATH, EDITIONS_FOLDER, EDITION, DB_CERT)

BAK_FILE = 'plantilla.png'
BAK_PATH = path.join(RES_PATH, EDITIONS_FOLDER, EDITION, BAK_FILE)

FONT_FILE = 'arial.ttf'
FONT_PATH = path.join(RES_PATH, FONT_FILE)
FONT_SIZE = 60
FONT = ImageFont.truetype(FONT_PATH, FONT_SIZE)
