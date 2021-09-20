from bs4 import BeautifulSoup
import requests
from csv import writer

# tous les livres sur la page d'accueil
url = "https://books.toscrape.com/"
page = requests.get(url)

soup = BeautifulSoup(page.content,"html.parser")

# Récupération des données pour chaque livres
lists = soup.find_all('article', class_="product_pod")

with open('all_info.csv', 'w') as f:
    thewriter = writer(f)
    header = ['title', 'price', 'stock']
    thewriter.writerow(header)

    for list in lists:
        # img = list.find('img', class_= "thumbnail")
        # rating = list.find("p", class_= "star-rating").text.replace ('/n', '')
        title = list.find('h3').text.replace('/n', '')
        price = list.find('p', class_="price_color").text.replace('/n', '')
        stock = list.find('p', class_="instock").text

        informaton=[title, price, stock]
        thewriter.writerow(informaton)
