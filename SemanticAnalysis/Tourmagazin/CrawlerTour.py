# Tour magazine crawler

from bs4 import BeautifulSoup
import requests
import numpy as np

url = "https://www.tour-magazin.de/"

req = requests.get(url)
soup = BeautifulSoup(req.text,"lxml")
tabs = [x.find('a') for x in soup.find('nav',class_='main vertical').find('ul').find_all('li',recursive=False)]
