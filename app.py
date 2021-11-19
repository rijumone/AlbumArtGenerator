from os import path as os_path
from os import getenv, remove
import json
import urllib.parse
import urllib.request
import requests
from loguru import logger
from bs4 import BeautifulSoup
from flask import Flask, render_template
from config import *
import random
from uuid import uuid1
from time import time
from glob import glob
from PIL import Image
from PIL import ImageDraw
from flickr_util import update_flickr_image

app = Flask(__name__)

_ctr = 0
@app.route("/")
def hello_world():
    try:
        return render_template(
            'index.html',
            album_font=get_rand_font(ALBUM_FONTS),
            artist_font=get_rand_font(ARTIST_FONTS),
            img_url=get_image_url(),
            artist_name=get_artist_name(),
            album_title=get_album_title(),
        )
    except Exception as _e:
        return render_template('500.html')


def main():
    print(f'{get_album_title()} - {get_artist_name()}')


def get_image_url():
    # first, clean up ops
    rm_files_older_than()
    image_url = None
    while not image_url:
        image_url = update_flickr_image()
    return resize_image(image_url)
    # return 'https://images.unsplash.com/photo-1630585308572-f53438fc684f?ixid=MnwyNjMyODl8MHwxfHJhbmRvbXx8fHx8fHx8fDE2MzI3MzA1NTY&ixlib=rb-1.2.1&fit=crop&w=500&h=500'
    # return 'https://images.unsplash.com/photo-1634140651084-79c562526e21?ixid=MnwyNjMyODl8MHwxfHJhbmRvbXx8fHx8fHx8fDE2MzU4NzY4MDQ&ixlib=rb-1.2.1&fit=crop&w=500&h=500'
    return 'https://live.staticflickr.com/65535/51686436074_8be39a8dce_o.jpg'
    global _ctr
    _ctr += 1
    print(f'_ctr: {_ctr}')
    url = f'https://api.unsplash.com/photos/random?client_id={UNSPLASH_ACCESS_KEY}&orientation=squarish'
    headers = {
        'Accept-Version': 'v1'
    }

    

    response = requests.request('GET', url, headers=headers, data={})
    response_headers = response.headers
    # print(response_headers)
    for x_header in ['X-Ratelimit-Limit', 'X-Ratelimit-Remaining']:
        x_val = response_headers.get('X-Ratelimit-Limit', None)
        logger.debug(f'{x_header}: {x_val}')
        
    try:
        return f"{response.json()['urls']['raw']}&fit=crop&w=500&h=500"
    except json.decoder.JSONDecodeError:
        logger.critical(response.text)
        # return 'https://images.unsplash.com/photo-1630990616294-4376e614fdee?ixid=MnwyNjMyODl8MHwxfHJhbmRvbXx8fHx8fHx8fDE2MzI3MjE0NzY&ixlib=rb-1.2.1&fit=crop&w=500&h=500'
        return 'https://images.unsplash.com/photo-1630585308572-f53438fc684f?ixid=MnwyNjMyODl8MHwxfHJhbmRvbXx8fHx8fHx8fDE2MzI3MzA1NTY&ixlib=rb-1.2.1&fit=crop&w=500&h=500'


def get_artist_name():
    url = 'https://en.wikipedia.org/wiki/Special:Random'
    response = requests.request('GET', url)
    soup = BeautifulSoup(response.text, 'lxml')
    heading = soup.find(id='firstHeading').text
    return heading


def get_album_title():
    '''
    url = 'https://en.wikiquote.org/wiki/Special:Random'
    response = requests.request('GET', url)
    soup = BeautifulSoup(response.text, 'lxml')
    uls = soup.find(id='mw-content-text').find_all('ul')
    for ul in uls:
        lis = ul.find_all('li')
        for li in lis:
            return ' '.join(li.text.split(' ')[-6:]).strip()
    '''
    url = 'https://api.quotable.io/random'
    response = requests.request('GET', url)
    title = ' '.join(response.json()['content'].split(' ')[-6:]).title()
    if title[-1] == '.':
        title = title[:-1]
    return title

def resize_image(url, x=500, y=500, opacity=150):
    '''
    - download image to local fs
    - apply crop from center according to x and y
        - raise Exception if failed
    - apply black mask
    - save to static/img
    - return path
    '''
    _local_file = f'static/img/{str(uuid1())}.jpg'
    urllib.request.urlretrieve(url, _local_file)

    im = Image.open(_local_file)
    width, height = im.size
    
    orientation = 'square'
    excess = 0
    if width > height:
        orientation = 'landscape'
        excess = width - height
    elif height > width:
        orientation = 'portrait'
        excess = height - width

    # Setting the points for cropped image
    if orientation == 'landscape':
        left = excess / 2
        top = 0
        right = width - (excess / 2)
        bottom = height
    elif orientation == 'portrait':
        left = 0
        top = (excess / 2)
        right = width
        bottom = height - (excess / 2)
    else:
        left = 0
        top = 0
        right = width
        bottom = height

    im1 = im.crop((left, top, right, bottom))

    newsize = (x, y)
    im1 = im1.resize(newsize)

    draw = ImageDraw.Draw(im1, "RGBA")
    draw.rectangle(((0,0), (x,y)), fill=(0, 0, 0, opacity))

    # im1.show() # open in local viewer
    im1.save(_local_file)

    return _local_file


def rm_files_older_than(path='static/img/*', seconds=60):
    # path = path.join()
    for _f in glob(path):
        mtime = os_path.getmtime(_f)
        time_diff = int((time() - mtime) / (1))
        if time_diff >= seconds:
            remove(_f)


def get_rand_font(fonts):
    font = random.choice(fonts)
    return font, urllib.parse.quote_plus(font)


if __name__ == '__main__':
    # main()
    # resize_image(url='https://live.staticflickr.com/65535/51686436074_8be39a8dce_o.jpg')
    # resize_image(url='https://live.staticflickr.com/65535/51678703270_f358ff9595_o.jpg')
    rm_files_older_than()
"""
Hello, kindly provide me the API Key.

Details as requested below.

Rijumone / mailmeonriju@gmail.com
Random Album Art generator, for fun, non-commercial use (https://github.com/rijumone/AlbumArtGenerator)
https://github.com/rijumone/AlbumArtGenerator/blob/master/preview.png
Site/app not expected to eventually go over the free tier (150,000 queries/month).
Thank you!
"""