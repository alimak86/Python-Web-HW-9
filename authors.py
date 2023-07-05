import requests
from models import Document_Author, Document_Quote, Document_Tags, Quote, Author, Document_Link, Author_Link
import json
from time import sleep

from bs4 import BeautifulSoup
from input import URL

Authors_list = []  ## to accumulate records for authors
Authors_link_list = {}  ## accumulate links for author description page
url = URL
"""
accumulate all the links for the author description
"""
while True:
  print("workig with: " + url)
  response = requests.get(url)  ## obtain html page
  authors = Author_Link(response, ["div", "quote"], ["a", "href"])
  links2write = authors.find_all()
  for link in links2write:
    Authors_link_list[link] = URL + link

  link = Document_Link(response, ["li", "next"], ["a", "href"])
  relative_url = link.find_all()
  if relative_url:
    url = URL + relative_url
    print("waiting 2 seconds to continue...")
    sleep(2)
  else:
    break

AUTHOR_TITLE = "author-title"
AUTHOR_BORN_LOCATION = "author-born-location"
AUTHOR_BORN_DATE = "author-born-date"
AUTHOR_DESCRIPTION = "author-description"

for element in Authors_link_list:
  #print(Authors_link_list[element])
  url = Authors_link_list[element]
  print("workig with: " + url)
  response = requests.get(url)  ## obtain html page
  author = Document_Author(response, ["h3", "author-title"])
  fullname = author.find_all()[0].lstrip().rstrip()
  born_loc = Document_Author(response, ["span", AUTHOR_BORN_LOCATION])
  born_location = born_loc.find_all()[0]
  born_date1 = Document_Author(response, ["span", AUTHOR_BORN_DATE])
  born_date = born_date1.find_all()[0]
  description1 = Document_Author(response, ["div", AUTHOR_DESCRIPTION])
  description = description1.find_all()[0].lstrip().rstrip()
  record = Author(fullname, born_date, born_location, description)
  Authors_list.append(record.data)
############  break

#############print(Authors_list)
with open("authors.json", "w") as f:
  json.dump(Authors_list, f)