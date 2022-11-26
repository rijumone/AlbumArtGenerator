import os
import time
from pprint import pprint
import flickrapi
import random

api_key = os.getenv('FLICKR_API')
api_secret = os.getenv('FLICKR_SECRET')

IMG_CATEGORIES = [
    'dogs',
    'cats',
    'animals',
    'anime',
    'weapons',
    'flowers',
    'beach',
    'sunset',
    'nsfw',
    'farm',
    'addiction',
    'sports',
    'love',
    'airplanes',
    'actor',
    'cars',
]

def main():

    flickr = flickrapi.FlickrAPI(api_key, api_secret, format='parsed-json')
    
    photosets = flickr.photosets.getList()
    pprint(photosets)


def update_flickr_image(imgobj={'title':'A','url':'https','width':'500','height':'500'}):
    
    flickr = flickrapi.FlickrAPI(api_key, api_secret, format='parsed-json')
    
    random.seed()
    rand_page = random.randrange(1,99,1)
    
    extras = 'url_sq,url_t,url_s,url_q,url_m,url_n,url_z,url_c,url_l,url_o'
    
    raw = flickr.photos.search(
        text=random.choice(IMG_CATEGORIES), 
        page=rand_page, 
        per_page=1, 
        extras=extras,
    )
    photos = raw['photos']
    
   # pp.pprint(photos)
    print("Page: ",rand_page)
     
    for image in photos['photo']:
        title = image['title']
        try:
            url = image['url_o']
            width = image['width_o']
            height = image['height_o']
        except:
            try:
                url = image['url_l']
                width = image['width_l']
                height = image['height_l']
            except:
                try:
                    url = image['url_c']
                    width = image['width_c']
                    height = image['height_c']
                except:
                    pass

    imgobj['title'] = title
    imgobj['url'] = url
    imgobj['width'] = width
    imgobj['height'] = height
    
    return url 
    

def main1():
    for _ in range(100):
        imgurl = update_flickr_image()
        print( imgurl)
        time.sleep(2)

if __name__ == '__main__':
    main1()
