#!/usr/bin/python

import requests
from bs4 import BeautifulSoup
from datetime import datetime

def get_soup(url):
  page = requests.get(url)
  soup = BeautifulSoup(page.content, "html.parser")
  return soup

def format_date(date):
  try:
    datetime_object = datetime.strptime(date, '%b. %d, %Y').date()
  except Exception as e:
    print(e)
  
  return datetime_object.strftime('%Y-%m-%d')

def scrape_contract_links(url, page_num):
  soup = get_soup(url + str(page_num))
  content = soup.find_all("listing-titles-only")
  links = []
  
  for item in content:
    date = format_date(item.attrs['publish-date-ap'])
    link = item.attrs['article-url']
    
    links.append({
      "date":date,
      "link":link
    })
  
  return links

def scrape_single_date(url):
  soup = get_soup(url)
  content = soup.find("div", class_="content")
  return content

def pull_awards(content):
  awardtexts = ""
  awards = []

  try:
    awardtexts = content.find_all("p")
  except Exception as e:
    print(e)

  for award in awardtexts:
    text = award.text
    if 'awarded' in text:
      company = text.split(',', 1)[0]
      awards.append(company)
  
  return awards

URL_LIST = "https://www.defense.gov/News/Contracts/?Page="
PAGES = 1

awards = []
page_num = 1

while page_num <= PAGES:
  links = scrape_contract_links(URL_LIST, page_num)
  
  for link in links:
    date_content = scrape_single_date(link['link'])
    awarded_companies = pull_awards(date_content)
    awards.append({
      "date": link['date'],
      "companies": awarded_companies
    })
  
  page_num += 1
  
print(awards)
