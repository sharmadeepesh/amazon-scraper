import requests
import json
from bs4 import BeautifulSoup

search_categories = ['earphones','smartphones','coolers','monitors','books','television', 'keyboards','mouse','bagpacks','sunglasses']
search_url = "https://www.amazon.com/s?k={}"
api_url = "http://api.scraperapi.com?api_key=YOUR_API_KEY_HERE"
links = []
name=[]
prices = []
images = []
details = []
stock_status = []
stars = []
categories = []
products = {}
dumplist = {}

def get_price(soup):
    try:
        price = soup.find('span',{'class':'a-color-price'}).text
        prices.append(price)
    except AttributeError:
        prices.append("Not Found")

def get_category(soup):
    category = ''
    try:
        category_soup = soup.find_all('a',{'class':'a-link-normal a-color-tertiary'})
        category_list = [elem.text.strip() for elem in category_soup]
        for elem in category_list:
            category += elem + ' > '
        categories.append(category)
    except AttributeError:
        categories.append("Not Found")

def get_details(soup):
    detailsdict = {}
    try:
        detail_soup = soup.find('table',{'class':'prodDetTable'})
        rows = detail_soup.find_all('tr')
        for i in range(len(rows)-3):
            detailsdict[rows[i].find('th').text.strip()] = rows[i].find('td').text.strip()
        details.append(detailsdict)
    except AttributeError:
        details.append("Not Found")

def get_stars(soup):
    try:
        star = soup.find('span',{'id':'acrPopover'})['title']
        stars.append(star[0:3])
    except TypeError:
        stars.append("Not Found")

def get_stock_status(soup):
    try:
        stock_soup = soup.find('div',{'id':'availability'})
        stock_status.append(stock_soup.find('span').text.strip())
    except AttributeError:
        stock_status.append("Not Found")

def get_image(soup):
    try:
        image = soup.find('img',{'id':'landingImage'})['src']
        images.append(image)
    except TypeError:
        images.append("Not Found")

def get_soup(url):
    content = requests.get(api_url+url).text
    soup = BeautifulSoup(content,'html.parser')
    get_price(soup)
    get_image(soup)
    get_details(soup)
    get_stock_status(soup)
    get_category(soup)
    get_stars(soup)

def get_name(soup):
    for product in soup:
        name.append((product.text).strip())

def get_links(category):
    url = api_url+search_url
    search = requests.get(url.format(category)).text
    soup = BeautifulSoup(search,'html.parser')
    headings = soup.find_all('h2',{'class':'a-size-mini'})
    for product in headings:
        link = "https://www.amazon.com" + product.find('a')['href']
        links.append(link)
    get_name(headings)

def get_json():
    for i in range(len(name)):
        products[i]={
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

if __name__ == "__main__":
    for category in categories:
        get_links('earphones')
    for link in links:
        get_soup(link)
    get_json()


#For Error Catching Purposes
'''for i in range(len(links)):
        print('Turn of',i)
        get_soup(links[i])
        print(i,"done")'''

    
