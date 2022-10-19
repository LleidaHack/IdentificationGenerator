from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader

from PIL import Image

import os

path = '_out_'
filename = 'test.pdf'
title = 'Test'

MAXY = 139
MAXX = -5
MARGIN = 10

def createPDF(path_to_images, document_name, document_title):

    def rowGen(list_of_images): #Creates a list of 4 image rows

        for i in range(0, len(list_of_images), 2):
            yield list_of_images[i:i + 2]


    def renderRow(path_to_images, row, y_pos): #Renders each row to the page

        x_pos = 27.5 #starting x position
        thumb_size = 450, 400 #Thumbnail image size

        for i in row:

            img = Image.open(os.path.join(path_to_images, i)) #Opens image as a PIL object
            img.thumbnail(thumb_size) #Creates thumbnail 

            img = ImageReader(img) #Passes PIL object to the Reportlab ImageReader

            #Lays out the image and filename
            pdf.drawImage(img, x_pos * mm , y_pos * mm, width = 317, height = 227, preserveAspectRatio=True, anchor='c')

            x_pos += 150 #Increments the x position ready for the next image


    images = [i for i in os.listdir(path_to_images) if i.endswith('.png')] #Creates list of images filtering out non .jpgs
    row_layout = list(rowGen(images)) #Creates the layout of image rows
    
    pdf = canvas.Canvas(document_name, pagesize=landscape(A4), pageCompression=1) #Creates the PDF object
    pdf.setTitle(document_title)
    
    rows_rendered = 0

    y_pos = 113.5  #Sets starting y pos
    pdf.setFont('Helvetica', 10)

    for row in row_layout: #Loops through each row in the row_layout list and renders the row. For each 5 rows, makes a new page

        if rows_rendered == 2:
        
            pdf.showPage()
            pdf.setFont('Helvetica', 10)
            y_pos = -100
            rows_rendered = 0
            break

        else:
            
            renderRow(path_to_images, row, y_pos)
            y_pos -= 100
            rows_rendered += 1
    pdf.save()
createPDF(path, filename, title)