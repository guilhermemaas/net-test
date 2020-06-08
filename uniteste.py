import requests
from bs4 import BeautifulSoap

page = requests.get('http://speed.unifique.com.br/')

soup = BeautifulSoap(page.text, 'html.parser')