
"""
The main file to run asynchrounous requests
"""


import time
# complete_start = time.time()  

import asyncio
import aiohttp
import os

from bs4 import BeautifulSoup

  
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

  
def converr(imgs,path, round_to = 20):
  """
  html -> pdf
  path - > str of path to files

  """
  start = time.time()  



  end = time.time()
  total_time = end - start
  print("It took {} seconds to write {} images".format(round(total_time, round_to),len(imgs)))

    
    

def main_func(urls, path, round_to = 20,debug__ = False):
  """
  urls -> list of urls
  path -> path to pdfs
  """
  start = time.time()  

  pg_d = asyncio.run(get_urls(urls, round_to,debug_ = debug__)) # pages to find the imgs
  print("\n------------------------\n")


  for sno,imgs in enumerate(all_imgs, start = 1):
    

    print(f"getting ch {sno}")
    img_d = asyncio.run(get_urls(imgs, round_to,debug_ = debug__)) # dict of images, contains binary


    print(f"making ch {sno}")
    converr(img_d["content"],f"{path}/ch_{sno}", save_info[0], save_info[1],round_to)
    print("------------------\n")


  end = time.time()
  total_time = end - start
  print("It took {} seconds to make {} chapters.".format(round(total_time, round_to),len(urls)))

  
  