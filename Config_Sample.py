from os import path
from PIL import ImageFont

TEST = True

DB_PATH_T = 'firebase/development/database/path'
DB_PATH = 'firebase/production/database/path'

# the folder where the generated output will be saved, if it dosen't exist will be created and if exists will be emptyed
OUT_FOLDER = '_out_'
OUT_PATH = path.join('.', OUT_FOLDER)

# the folder where all resources will be saved
RES_FOLDER = 'resources'
RES_PATH = path.join('.', RES_FOLDER)

# the file containing all input data
DATA_FILE = 'data.json'
DATA_PATH = path.join(RES_PATH, DATA_FILE)

# the path to the firebase certificate file
DB_CERT = '2019_firebase_cert.json'
DB_CERT_PATH = path.join(RES_PATH, DB_CERT)

# path to the background to be used
BAK_FILE = 'plantilla.png'
BAK_PATH = path.join(RES_PATH, BAK_FILE)

# path to file to be used as font
FONT_FILE = 'arial.ttf'
FONT_PATH = path.join(RES_PATH, FONT_FILE)

# font size
FONT_SIZE = 60

# font to be used
FONT = ImageFont.truetype(FONT_FILE, FONT_SIZE)
