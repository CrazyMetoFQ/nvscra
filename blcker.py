import fitz
from PIL import Image
import io

import fitz

# docnm = r'c:\Users\alima\Downloads\phy pra for XI (1).pdf'
docnm = input("Ebter Doc Name:- ")
docnm = fr'c:\Users\alima\Downloads\{docnm}'
doc = fitz.open(docnm) # open a document

hex_color = '#FF0000'
rgb_color = tuple(int(hex_color[i:i+2], 16) for i in (1, 3, 5))

for page_index in range(len(doc)): # iterate over pdf pages
    page = doc[page_index] # get the page

    img = Image.new('RGB', (int(page.rect.width), int(page.rect.height)), color = "#CCCFDA")
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    image_bytes = buffer.getvalue()

    page.insert_image(page.bound(),stream=image_bytes, overlay=False)

doc.save(docnm[:-4]+"BLACKED.pdf") # save the document with a new filename
