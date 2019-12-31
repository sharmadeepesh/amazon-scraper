import json

name = ['name 1','name 2']
links = ['www.link.com','www.link2.com']
images = ['image1','image2']
details = ['details1','details2']
prices = ['1000','2000']
stock_status = ['In stock','Out of stock']
stars = ['3.4','5']
categories = ['toys','pets']
products = {}
dumplist = {}

def get_json():
    for i in range(len(name)):
        products[name[i]]={
            'price': prices[i],
            'image': images[i],
            'details': details[i],
            'stock status': stock_status[i],
            'category': categories[i],
            'stars': stars[i],
            'link': links[i]
        }
    dumplist['Scrape Output'] = products
    with open('output.json','w') as outputfile:
        json.dump(dumplist,outputfile) 

get_json()