from os import path
from PIL import ImageFont

TEST = False

EDITION='2022'
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

FONT_FILE = 'DIN-Regular.ttf'
BOLD_FONT_FILE = 'DIN-Bold.ttf'
FONT_FOLDER = 'fonts'
FONT_PATH = path.join(RES_PATH, FONT_FOLDER, FONT_FILE)
TYPE_FONT_SIZE = 18
NAME_FONT_SIZE = 12
FONT_COLOR = (0,0,0)
WHITE_FONT_COLOR = (255,255,255)
TYPE_FONT = ImageFont.truetype(FONT_PATH, TYPE_FONT_SIZE)
NAME_FONT = ImageFont.truetype(FONT_PATH, NAME_FONT_SIZE)

MAIN_COLOR = (31, 33, 36)
BAK_COLOR = (247, 247, 242)