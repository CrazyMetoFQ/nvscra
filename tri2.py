from bs4 import BeautifulSoup
import time
import fitz
from io import BytesIO
from PIL import Image
import toml
import asyncio
import aiohttp
import os
from unidecode import unidecode


# Open the text file
with open('test copy.html', 'rb') as f:
    htmltext = f.read() #.replace("&#8220;", '"').replace("&#8230", "…").replace("&#8217", "'").replace("&#8221", '"')

soup = BeautifulSoup(htmltext, 'lxml')
txt = soup.get_text()
txt = unidecode(txt).strip()
txt = txt[txt.find("Chapter 1"):]
txt = txt[txt.find("Chapter 2334 - End"):]
txt = txt[txt.find("Next")+4:].strip()
txt = txt[:txt.find("Chapter 2334 - End")].strip()


with open("tri.txt", "w") as f:
    f.write(txt)

text = txt 
# Create a new PDF document
doc = fitz.open()

# Add a new page to the document
page = doc.new_page()

# Add the text to the page
page.insert_text(text,text)

# Save the document as a PDF file
doc.save('output.pdf')

# Close the document
doc.close()
