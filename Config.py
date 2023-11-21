from os import path
from PIL import ImageFont

TEST = False

EDITION='2023'
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

BAK_FILE_CONTESTANT = 'plantilles\\participant.png'
BAK_PATH_CONTESTANT = path.join(RES_PATH, EDITIONS_FOLDER, EDITION, BAK_FILE_CONTESTANT)
BAK_FILE_STAFF = 'plantilles\\organitzador.png'
BAK_PATH_STAFF = path.join(RES_PATH, EDITIONS_FOLDER, EDITION, BAK_FILE_STAFF)
BAK_FILE_EMPRESA = 'plantilles\\patrocinador.png'
BAK_PATH_EMPRESA = path.join(RES_PATH, EDITIONS_FOLDER, EDITION, BAK_FILE_EMPRESA)

FONT_FOLDER = 'fonts'
FONT_FILE = 'SpaceMono-Regular.ttf'
BOLD_FONT_FILE = 'SpaceMono-Bold.ttf'
FONT_PATH = path.join(RES_PATH, FONT_FOLDER, FONT_FILE)
BOLD_FONT_PATH = path.join(RES_PATH, FONT_FOLDER, BOLD_FONT_FILE)
TYPE_FONT_SIZE =50
NAME_FONT_SIZE = 90
FONT_COLOR = (0,0,0)
WHITE_FONT_COLOR = (255,255,255)
DARK_FONT_COLOR = (35,35,35)
TYPE_FONT = ImageFont.truetype(FONT_PATH, TYPE_FONT_SIZE)
NAME_FONT = ImageFont.truetype(FONT_PATH, NAME_FONT_SIZE)
BOLD_TYPE_FONT = ImageFont.truetype(BOLD_FONT_PATH, TYPE_FONT_SIZE)
BOLD_NAME_FONT = ImageFont.truetype(BOLD_FONT_PATH, NAME_FONT_SIZE)
# FONT = ImageFont.truetype("Symbola.ttf", 60, encoding='unic')

MAIN_COLOR = (31, 33, 36)
BAK_COLOR = (247, 247, 242)