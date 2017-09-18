import pandas as pd
import requests
from bs4 import BeautifulSoup as bs4
import time
import random

url_base = 'http://sfbay.craigslist.org/search/eby/roo'
pages = [url_base, url_base + '?s=120', url_base + '?s=240', url_base + '?s=360', url_base + '?s=480', url_base + '?s=600', url_base + '?s=720',
         url_base + '?s=840', url_base + '?s=960', url_base + '?s=1080', url_base + '?s=1200', url_base + '?s=1320', url_base + '?s=1460',
         url_base + '?s=1580', url_base + '?s=1700', url_base + '?s=1820', url_base + '?s=1940', url_base + '?s=2060', url_base + '?s=2180',
         url_base + '?s=2300']
title_list = []
price_list = []
neighborhood_list = []
movein_list = []
attributes_list = []
description_list = []
latitude_list = []
longitude_list = []
for page in pages:
    rsp = requests.get(page)
    html = bs4(rsp.text, 'html.parser')
    rooms = html.find_all('li', attrs={'class': 'result-row'})
    for room in rooms:
        print "room"
        time.sleep(random.randint(2, 5))
        link = 'http://sfbay.craigslist.org/eby/roo' + room.find('a')['href'][8:]
        rsp2 = requests.get(link)
        html2 = bs4(rsp2.text, 'html.parser')
        try:
            title = html2.find('title').text
            title_list.append(title.encode('utf-8'))
        except:
            title = None
            title_list.append(title)
        try:
            price = html2.find_all('span', attrs={'class': 'price'})[0].text
            price_list.append(price.encode('utf-8'))
        except:
            price = None
            price_list.append(price)
        try:
            neighborhood = html2.find('small').text
            neighborhood_list.append(neighborhood.encode('utf-8'))
        except:
            neighborhood = None
            neighborhood_list.append(neighborhood)
        try:
            movein = html2.find_all('p', attrs={'class': 'attrgroup'})[0].find('span')['data-date']
            movein_list.append(movein.encode('utf-8'))
        except:
            movein = None
            movein_list.append(movein)
        try:
            attributes = html2.find_all('p', attrs={'class': 'attrgroup'})[1].find_all('span') # need to parse still
            attributes_list.append(attributes)
        except:
            attributes = None
            attributes_list.append(attributes)
        try:
            description = html2.find_all('section', attrs={'id': 'postingbody'})[0].text
            description_list.append(description.encode('utf-8'))
        except:
            description = None
            description_list.append(description)
        try:
            latitude = html2.find_all('div', attrs={'class': 'mapbox'})[0].find('div')['data-latitude']
            latitude_list.append(latitude.encode('utf-8'))
        except:
            latitude = None
            latitude_list.append(latitude)
        try:
            longitude = html2.find_all('div', attrs={'class': 'mapbox'})[0].find('div')['data-longitude']
            longitude_list.append(longitude.encode('utf-8'))
        except:
            longitude  = None
            longitude_list.append(longitude)

df = pd.DataFrame.from_items([('title', title_list), ('price', price_list), ('neighborhood', neighborhood_list), ('movein', movein_list),
                              ('attributes', attributes_list), ('description', description_list), ('latitude', latitude_list),
                              ('longitude', longitude_list)])
df.to_csv('craigslist.csv', index=False)
