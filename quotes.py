import requests
from models import Document_Author, Document_Quote, Document_Tags, Quote, Author, Document_Link
import json
from time import sleep

from bs4 import BeautifulSoup
from input import URL

Quotes_list = []  ## to accumulate records for quotes
url = URL
while True:
  print("workig with: " + url)
  response = requests.get(url)  ## obtain html page
  quotes = Document_Quote(response, ["span", "text"])
  quotes2write = quotes.find_all()

  author = Document_Author(response, ["small", "author"])
  authors2write = author.find_all()

  tags = Document_Tags(response, ["div", "tags"], ["meta", "content"])
  tags2write = tags.find_all()
  # print(authors2write)
  # print(quotes2write)
  # print(tags2write)
  # break
  """
  for each item found on the page
  create a record Quote and append its dictionary Quote.data into Quotes_list
  """
  for num in range(len(quotes2write)):
    author = authors2write[num]
    quote = quotes2write[num]
    tag = tags2write[num]
    #print(tag)
    record = Quote(tag, author, quote)
    Quotes_list.append(record.data)
    ########print(Quotes_list)
  """
  define the link to the next page if exist
  if does not exist then leave the loop and write the file
  """

  link = Document_Link(response, ["li", "next"], ["a", "href"])
  # soup = BeautifulSoup(response.text, "lxml")
  # link = soup.find("li", class_="next")
  relative_url = link.find_all()
  if relative_url:
    url = URL + relative_url
    print("waiting 2 seconds to continue...")
    sleep(2)
  else:
    break
##print(Quotes_list)
## write Quotes_list into json file
with open("quotes.json", "w") as f:
  json.dump(Quotes_list, f)
