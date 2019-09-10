#!/usr/local/bin/python3
# A test file using BeautifulSoup

import requests
from bs4 import BeautifulSoup

r = requests.get("http://herenow.com/results/#/races/20558/results")

data = r.text

soup = BeautifulSoup(data, "html.parser")

for link in soup("link"):
    print(link["href"])
