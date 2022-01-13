#!/usr/bin/python

import requests
from bs4 import BeautifulSoup

URL = "https://www.defense.gov/News/Contracts/Contract/Article/2858648/"

page = requests.get(URL)

# Get the div with the class="body"
soup = BeautifulSoup(page.content, "html.parser")

body = soup.find("div", class_="body")
awards = body.find_all("p", string=lambda text: "awarded" in text)
companies = []

for award in awards:
    text = award.text
    companies.append(text.split(',', 1)[0])

print(companies)
