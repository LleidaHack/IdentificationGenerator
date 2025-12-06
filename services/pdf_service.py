from PIL import Image
from fpdf import FPDF
import os
import tempfile
import shutil

class PDFService:
    def __init__(self):
        # Config params from batch_pdfer.py
        self.PIXEL_TO_MM = 0.0847
        self.IMAGES_PER_ROW = 3
        self.IMAGES_PER_COL = 3
        self.MARGIN_MM = 0
        self.GAP_MM = 1
        self.TARGET_WIDTH_MM = 95
        self.TARGET_HEIGHT_MM = 70
        self.AUTO_LAYOUT = False
        self.CELL_FILL = 0.95
        self.UPSCALE = True
        self.GLOBAL_SCALE = 1.0

    def create_pdf(self, images: list[Image.Image]) -> str:
        """
        Creates a PDF from a list of PIL Images.
        Returns the path to the generated PDF file.
        """
        # Create a temp dir to store images
        temp_dir = tempfile.mkdtemp()
        image_paths = []
        
        try:
            # Save all images to temp dir
            for idx, img in enumerate(images):
                img_path = os.path.join(temp_dir, f"img_{idx}.png")
                img.save(img_path)
                image_paths.append(img_path)

            pdf = FPDF()
            
            pdf_size = {'P': {'w': 210, 'h': 297}, 'L': {'w': 297, 'h': 210}}

            for index, imageFile in enumerate(image_paths):
                # Retrieve dimensions from stored file to match original logic
                # although we have the PIL objects, fpdf needs reading sizing sometimes or we calculate it.
                # using the PIL object we have in 'images' list would be faster for size, 
                # but let's stick to the file loop logic for consistency with original script if needed.
                # Actually, we can use the PIL image from the list for sizing.
                
                curr_img = images[index]
                px_w, px_h = curr_img.size

                # convert pixels to mm
                width_mm = float(px_w * self.PIXEL_TO_MM)
                height_mm = float(px_h * self.PIXEL_TO_MM)

                # determine orientation by image aspect
                orientation = 'P' if width_mm < height_mm else 'L'

                page_w = pdf_size[orientation]['w']
                page_h = pdf_size[orientation]['h']

                # compute available cell size
                cell_w = (page_w - 2 * self.MARGIN_MM - (self.IMAGES_PER_ROW - 1) * self.GAP_MM) / self.IMAGES_PER_ROW
                cell_h = (page_h - 2 * self.MARGIN_MM - (self.IMAGES_PER_COL - 1) * self.GAP_MM) / self.IMAGES_PER_COL

                if self.TARGET_WIDTH_MM and self.TARGET_HEIGHT_MM:
                    target_w = self.TARGET_WIDTH_MM * self.GLOBAL_SCALE * self.CELL_FILL
                    target_h = self.TARGET_HEIGHT_MM * self.GLOBAL_SCALE * self.CELL_FILL
                    base_scale = min(target_w / width_mm, target_h / height_mm)
                else:
                    base_scale = min(cell_w / width_mm, cell_h / height_mm)

                if not self.UPSCALE:
                    base_scale = min(1.0, base_scale)

                render_w = width_mm * base_scale
                render_h = height_mm * base_scale

                # add new page when needed
                images_per_page = self.IMAGES_PER_ROW * self.IMAGES_PER_COL
                if index % images_per_page == 0:
                    pdf.add_page(orientation=orientation)

                col = index % self.IMAGES_PER_ROW
                row = (index // self.IMAGES_PER_ROW) % self.IMAGES_PER_COL

                x = self.MARGIN_MM + (render_w + self.GAP_MM) * col
                y = self.MARGIN_MM + (render_h + self.GAP_MM) * row

                pdf.image(imageFile, x, y, render_w, render_h)

            output_pdf_path = os.path.join(temp_dir, "output.pdf")
            pdf.output(output_pdf_path, "F")
            
            # We need to return the file path, but the temp dir will be tricky if we want to delete it effectively.
            # Ideally, we return the bytes.
            
            with open(output_pdf_path, "rb") as f:
                pdf_bytes = f.read()
                
        finally:
            shutil.rmtree(temp_dir)
            
        return pdf_bytes
