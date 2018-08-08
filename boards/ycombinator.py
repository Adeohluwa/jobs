#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup as parse
import json,re
from geotext import GeoText

# get job details
def getPostings():
  url = 'https://news.ycombinator.com/jobs'
  response = requests.get(url)
  page = parse(response.content,'lxml')    
  headlines = page.select('a.storylink')
  timestamps = page.select('span.age')
  company = re.compile(r'^[A-Z].+ \(YC .\d+\)|^[A-Z]\w+ [a-z]')

  titles = [title.text for title in headlines]
  times = [time.text for time in timestamps]
  urls = [title['href'] for title in headlines]
  locations = [GeoText(title).cities for title in titles]
  # companies = [re.findall(company,str(titles))]
  # print(titles)

  details = zip(titles,times,urls,locations)
  return details

# pretty print job results in JSON
def postData():
  for ti,t,u,l in details:
    posting = {'Company Name': ti,
    'Job Title':'N/A',
    'Url': u,
    'Location':l[0] if l else 'N/A',
    'Time':t
    }
    data = json.dumps(posting,indent=4)
    print(data)
    print("\n")

details = getPostings()
postData()