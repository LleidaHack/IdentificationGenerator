from PIL import Image
import Config
from fpdf import FPDF
import glob
import os

image_directory = r'./_out_/'
extensions = ('*.jpg','*.png','*.gif')
pdf = FPDF()
imagelist=[]
for ext in extensions:
    imagelist.extend(glob.glob(os.path.join(image_directory,ext)))

for index, imageFile in enumerate(imagelist):
    cover = Image.open(imageFile)
    width, height = cover.size
    print(width, height)

    # convert pixel in mm with 1px=0.0847 mm
    width, height = float(width * 0.0847), float(height * 0.0847)

    # given we are working with A4 format size 
    pdf_size = {'P': {'w': 210, 'h': 297}, 'L': {'w': 297, 'h': 210}}

    # get page orientation from image size 
    orientation = 'P' if width < height else 'L'

    #  make sure image size is not greater than the pdf format size
    width = width if width < pdf_size[orientation]['w'] else pdf_size[orientation]['w']
    height = height if height < pdf_size[orientation]['h'] else pdf_size[orientation]['h']

    if index % 9 == 0:
        pdf.add_page(orientation=orientation)

    pdf.image(imageFile, 90.2 * (index%3), 61.1*((index//3)%3), width, height)


pdf.output(image_directory + "file.pdf", "F")