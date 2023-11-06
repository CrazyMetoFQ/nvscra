import time

doc_start = time.time()

import fitz
from io import BytesIO
from PIL import Image
import toml
import asyncio
import aiohttp
import os

opts = toml.load("opts.toml")

if os.path.isdir(opts["outfiledir"]):
   pass
else:
   os.mkdir(opts["outfiledir"])

async def get_urls(urls, round_to = 20, debug_ = False):
  """
  urls -> list of links

  returns response, ok, content of urls.
  requests are sent asynchrously.
  """
  
  if debug_:print(urls)
  else:pass

  start = time.time()  
  async with aiohttp.ClientSession() as session:
    	   
    tasks = []
    for url in urls:
      tasks.append(asyncio.create_task(session.get(url, ssl=False)))

    responses = await asyncio.gather(*tasks)
      
    urls_result = {"res":responses,
                      "ok":[r.ok for r in responses],
                      "content":[await r.content.read() for r in responses]}

    end = time.time()
    total_time = end - start
    print("It took {} seconds to make {} calls".format(round(total_time, round_to),len(urls)))
    
    return urls_result



def html2pdf(HTML, outpdfloc, sno=1):
    """
    Converts html to pdf
    """

    start = time.time()  
    
    MEDIABOX = fitz.paper_rect("letter")  # output page format: Letter
    WHERE = MEDIABOX + (36, 36, -36, -36)  # leave borders of 0.5 inches

    story = fitz.Story(html=HTML)  # create story from HTML
    writer = fitz.DocumentWriter(outpdfloc)  # create the writer

    more = 1  # will indicate end of input once it is set to 0

    while more:  # loop outputting the story
        device = writer.begin_page(MEDIABOX)  # make new page
        more, _ = story.place(WHERE)  # layout into allowed rectangle
        story.draw(device)  # write on page
        writer.end_page()  # finish page

    writer.close()  # close output file

    end = time.time()
    total_time = end - start
    print(f"It took {round(total_time, opts['round_to'])} seconds to convert html to pdf | {sno}")

def blakcr(docnm, sno=1):

    start = time.time()  

    doc = fitz.open(docnm) # open a document

    hex_color = '#FF0000'
    rgb_color = tuple(int(hex_color[i:i+2], 16) for i in (1, 3, 5))

    for page_index in range(len(doc)): # iterate over pdf pages
        page = doc[page_index] # get the page

        img = Image.new('RGB', (int(page.rect.width), int(page.rect.height)), color = "#CCCFDA")
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        image_bytes = buffer.getvalue()

        page.insert_image(page.bound(),stream=image_bytes, overlay=False)

    doc.save(docnm[:-4]+"_b.pdf") # save the document with a new filename

    
    end = time.time()
    total_time = end - start
    print(f"It took {round(total_time, opts['round_to'])} seconds to convert make a pdf black | {sno}")


def main():
    
    print(f"Getting {opts['end'] - opts['start']} URLS")
    urls = [opts["base_link"].format(i) for i in range(opts["start"],opts["end"])]
    chps_htmls = asyncio.run(get_urls(urls, opts["round_to"],opts["debug"]))["content"]
    print("\n------------------------\n")
    
    for sno, chp_html in enumerate(chps_htmls, start=opts["start"]):
        file_name = opts["outfileformat"].format(sno)
        current_iteration = sno - opts["start"] +1

        print(f"Making {file_name} | {current_iteration} / {opts['end'] - opts['start']}")

        html2pdf(str(chp_html), file_name, current_iteration) # making file
        blakcr(file_name, current_iteration)  # making it black (adds _b to filename)
        print(os.listdir())
        print(os.listdir(opts["outfiledir"]))

        # os.remove(file_name) # remving non black one

# main()
print(os.listdir(opts["outfiledir"]))
