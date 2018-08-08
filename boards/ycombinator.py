#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup as parse
import json,re


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
  # companies = [re.findall(company,str(titles))]
  # print(titles)
  # print(companies)

  details = zip(titles,times,urls)
  return details


# pretty print job results in JSON
def postData():
  for ti,t,u in details:
    posting = {'Title':ti,
    # 'Company':c,
    'Url': u,
    # 'Location':l,
    'Time':t
    }
    data = json.dumps(posting,indent=4)
    print(data)
    print("\n")

details = getPostings()
postData()