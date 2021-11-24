from os import path
from PIL import ImageFont

TEST = False

EDITION='2021'
EDITIONS_FOLDER = 'editions'

DB_PATH_T = 'hackeps-'+EDITION+'/dev/users'
DB_PATH = 'hackeps-'+EDITION+'/prod/users'


OUT_FOLDER = '_out_'
OUT_PATH = path.join('.', OUT_FOLDER)

RES_FOLDER = 'resources'
RES_PATH = path.join('.', RES_FOLDER)

DATA_FILE = 'data.json'
DATA_PATH = path.join(RES_PATH, EDITIONS_FOLDER, EDITION, DATA_FILE)

DB_CERT = '2019_firebase_cert.json'
DB_CERT_PATH = path.join(RES_PATH, DB_CERT)

BAK_FILE = 'plantilla.png'
BAK_PATH = path.join(RES_PATH, EDITIONS_FOLDER, EDITION, BAK_FILE)

FONT_FILE = 'Montserrat-Regular.ttf'
# FONT_FILE = 'arial.ttf'
FONT_PATH = path.join(RES_PATH, FONT_FILE)
FONT_SIZE = 80
FONT_COLOR = (0,0,0)
FONT = ImageFont.truetype(FONT_PATH, FONT_SIZE)
# FONT = ImageFont.truetype("Symbola.ttf", 60, encoding='unic')
