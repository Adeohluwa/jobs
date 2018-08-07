#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup

url = "https://news.ycombinator.com/jobs"

page = requests.get(url)
print(page.content)