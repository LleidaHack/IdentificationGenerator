from PIL import Image
import Config
from fpdf import FPDF
import glob
import os
image_directory = r'./_out_/'
extensions = ('*.jpg','*.png','*.gif')

# --- Configurable layout / scaling parameters ---
# Convert pixels to millimeters. Increase this to make images larger.
# Typical values: 0.0271 (small), 0.0847 (larger). Default here is 0.0847 for bigger images.
PIXEL_TO_MM = 0.0847
# Page layout: number of images per row/column
IMAGES_PER_ROW = 3
IMAGES_PER_COL = 3
# Page margins (mm) and gap between images (mm)
MARGIN_MM = 7
GAP_MM = 0.5
# Target badge size (mm) — set to your measured lanyard size
TARGET_WIDTH_MM = 90
TARGET_HEIGHT_MM = 65
# If True, compute IMAGES_PER_ROW / IMAGES_PER_COL automatically based on the target and page size
AUTO_LAYOUT = True
# How much of the target area the image should fill (0.0-1.0)
CELL_FILL = 0.95
# Allow upscaling images if they're smaller than the target
UPSCALE = True
# Global multiplier for fine adjustments
GLOBAL_SCALE = 1.0
# -------------------------------------------------

pdf = FPDF()
imagelist = []
for ext in extensions:
    imagelist.extend(glob.glob(os.path.join(image_directory, ext)))

pdf_size = {'P': {'w': 210, 'h': 297}, 'L': {'w': 297, 'h': 210}}

for index, imageFile in enumerate(imagelist):
    cover = Image.open(imageFile)
    px_w, px_h = cover.size

    # convert pixels to mm
    width_mm = float(px_w * PIXEL_TO_MM)
    height_mm = float(px_h * PIXEL_TO_MM)

    # determine orientation by image aspect
    orientation = 'P' if width_mm < height_mm else 'L'

    page_w = pdf_size[orientation]['w']
    page_h = pdf_size[orientation]['h']

    # If AUTO_LAYOUT and target specified, compute how many target cells fit on the page
    if AUTO_LAYOUT and TARGET_WIDTH_MM and TARGET_HEIGHT_MM:
        IMAGES_PER_ROW = max(1, int((page_w - 2 * MARGIN_MM + GAP_MM) // (TARGET_WIDTH_MM + GAP_MM)))
        IMAGES_PER_COL = max(1, int((page_h - 2 * MARGIN_MM + GAP_MM) // (TARGET_HEIGHT_MM + GAP_MM)))

    # compute available cell size for each image
    cell_w = (page_w - 2 * MARGIN_MM - (IMAGES_PER_ROW - 1) * GAP_MM) / IMAGES_PER_ROW
    cell_h = (page_h - 2 * MARGIN_MM - (IMAGES_PER_COL - 1) * GAP_MM) / IMAGES_PER_COL

    # If a target size is set, try to fit the image inside the target area first
    if TARGET_WIDTH_MM and TARGET_HEIGHT_MM:
        target_w = TARGET_WIDTH_MM * GLOBAL_SCALE * CELL_FILL
        target_h = TARGET_HEIGHT_MM * GLOBAL_SCALE * CELL_FILL
        base_scale = min(target_w / width_mm, target_h / height_mm)
    else:
        base_scale = min(cell_w / width_mm, cell_h / height_mm)

    if not UPSCALE:
        base_scale = min(1.0, base_scale)

    render_w = width_mm * base_scale
    render_h = height_mm * base_scale

    # add new page when needed
    images_per_page = IMAGES_PER_ROW * IMAGES_PER_COL
    if index % images_per_page == 0:
        pdf.add_page(orientation=orientation)

    col = index % IMAGES_PER_ROW
    row = (index // IMAGES_PER_ROW) % IMAGES_PER_COL

    x = MARGIN_MM + (render_w + GAP_MM) * col
    y = MARGIN_MM + (render_h + GAP_MM) * row

    pdf.image(imageFile, x, y, render_w, render_h)

pdf.output(os.path.join(image_directory, "file.pdf"), "F")