from os import getenv
from dotenv import load_dotenv
load_dotenv()

UNSPLASH_ACCESS_KEY = getenv('UNSPLASH_ACCESS_KEY')
FLICKR_KEY = getenv('FLICKR_KEY')
FLICKR_SECRET = getenv('FLICKR_SECRET')

ALBUM_FONTS = [
    'Comforter Brush',
    'Praise',
    'Dancing Script',
    'Estonia',
]

ARTIST_FONTS = [
    'Bebas Neue',
    'Road Rage',
    'Comfortaa',
    'Lobster',
    'Patua One',
]