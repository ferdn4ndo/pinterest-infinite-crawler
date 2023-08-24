import os
import requests
import asyncio
from bs4 import BeautifulSoup
from time import sleep

async def download_image(src, alt_text, dir, save_description=True):
    ErrorLevel = 0
    failed = False
    filename = src.split('/')[-1]
    if dir[-1] != "/":
        dir += "/"
    savedir = dir + filename
    src = src.replace("/236x/", "/originals/").replace("/474x/", "/originals/").replace("/736x/", "/originals/")
    while True:
        try:
            request = requests.get(src)
            # If status code is not 200, skip this image
            # Maybe this cause 403 Error, but I don't know how to handle it
            # assert request.status_code == 200
            if request.status_code != 200:
                print(f"Download {src} fail!")
                return True

            with open(savedir, 'wb') as file:
                file.write(request.content)

            print(f"Downloaded image {src}!")

            if save_description:
                text_filename = os.path.join(dir, filename.replace(".jpg", ".txt"))
                with open(text_filename, 'w') as file:
                    file.write(alt_text)
                    print(f"Saved image description {text_filename}!")

            break
        except Exception as e:
            print(f"{src} : Download fail! Error: {e}")
            ErrorLevel += 1
            sleep(1)
            if (ErrorLevel >= 10):
                failed = True
                print(src + ": Download fail, Skip image")
                break
    return failed


async def download_image_host(plist, alt_list, dir, save_description=True):
    fail_image = 0
    fts = [asyncio.ensure_future(download_image(plist[i], alt_list[i], dir, save_description)) for i in range(0, len(plist))]
    fail_image = await asyncio.gather(*fts)
    return fail_image
