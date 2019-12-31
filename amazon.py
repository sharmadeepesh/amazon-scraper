import requests
import json
from bs4 import BeautifulSoup

search_categories = ['earphones','smartphones','coolers','monitors','books','television', 'keyboards','mouse','bagpacks','sunglasses']
search_url = "https://www.amazon.com/s?k={}"
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
    except AttributeError:
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
    content = requests.get(url).text
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
    search = requests.get(search_url.format(category),headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
    }).text
    soup = BeautifulSoup(search,'html.parser')
    print(soup)
    headings = soup.find_all('span',{'class':'a-size-mini'})
    for product in headings:
        link = "https://www.amazon.com" + product.find('a')['href']
        links.append(link)
        print(link)
    get_name(headings)

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

if __name__ == "__main__":
    for category in categories:
        get_links(category)
    for link in links:
        get_soup(link)
    get_json()

#For Error Catching Purposes
'''for i in range(len(links)):
        print('Turn of',i)
        get_soup(links[i])
        print(i,"done")'''

    