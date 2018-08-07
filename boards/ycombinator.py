#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup as parse

url = "https://news.ycombinator.com/jobs"

response = requests.get(url)

page = parse(response.content,'lxml')    
headlines = page.select('a.storylink')

for each in headlines:
  print(each.text)