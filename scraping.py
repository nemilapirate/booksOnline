# récupération des données pour un livre
import requests
from bs4 import BeautifulSoup
from csv import writer

product_page_url = "https://books.toscrape.com/catalogue/a-murder-in-time_877/index.html"
page = requests.get(product_page_url)

soup = BeautifulSoup(page.content,"html.parser")

informations = soup.find('article', class_="product_page").text

