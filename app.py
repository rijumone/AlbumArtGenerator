from os import getenv
import json
import requests
from loguru import logger
from bs4 import BeautifulSoup
from flask import Flask, render_template

UNSPLASH_ACCESS_KEY = getenv('UNSPLASH_ACCESS_KEY')

app = Flask(__name__)

_ctr = 0
@app.route("/")
def hello_world():
    return render_template(
        'index.html',
        img_url=get_image_url(),
        artist_name=get_artist_name(),
        album_title=get_album_title(),
    )
    # return f'<img src="{get_image_url()}">'


def main():
    print(f'{get_album_title()} - {get_artist_name()}')


def get_image_url():
    global _ctr
    _ctr += 1
    print(f'_ctr: {_ctr}')
    url = f'https://api.unsplash.com/photos/random?client_id={UNSPLASH_ACCESS_KEY}&orientation=squarish'
    headers = {
        'Accept-Version': 'v1'
    }

    # return 'https://images.unsplash.com/photo-1630585308572-f53438fc684f?ixid=MnwyNjMyODl8MHwxfHJhbmRvbXx8fHx8fHx8fDE2MzI3MzA1NTY&ixlib=rb-1.2.1&fit=crop&w=500&h=500'
    return 'https://images.unsplash.com/photo-1634140651084-79c562526e21?ixid=MnwyNjMyODl8MHwxfHJhbmRvbXx8fHx8fHx8fDE2MzU4NzY4MDQ&ixlib=rb-1.2.1&fit=crop&w=500&h=500'

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
    return ' '.join(response.json()['content'].split(' ')[-6:]).title()


if __name__ == '__main__':
    main()
