from bs4 import BeautifulSoup
from collections import UserDict, UserList
from abc import ABC, abstractmethod
"""
works with the lists obtained from the soup.find_all()
"""
"""
this class is to handle work of BeautifulSoup
"""
FS_META_TAG = ","  ## words separator in document meta attribute


class Document_Base:

  def __init__(self, response, tag_attr_list):
    self.response = response
    self.tag = tag_attr_list[0]
    self.attr = tag_attr_list[1]
    self.execute = BeautifulSoup(self.response.text, "lxml")

  @abstractmethod
  def find_all():
    pass


class Author_Link(Document_Base):

  def __init__(self, response, tag_attr_list, list):
    Document_Base.__init__(self, response, tag_attr_list)
    self.meta = list[0]
    self.href = list[1]

  def find_all(self):
    items = self.execute.find_all(name=self.tag, class_=self.attr)
    output = []
    for element in items:
      output.append(element.find(self.meta)[self.href])
    return output


class Document_Link(Document_Base):

  def __init__(self, response, tag_attr_list, list):
    Document_Base.__init__(self, response, tag_attr_list)
    self.meta = list[0]
    self.href = list[1]

  def find_all(self):
    element = self.execute.find(name=self.tag, class_=self.attr)
    if element == None:
      return None
    return element.find(self.meta)[self.href]


class Document_Quote(Document_Base):

  def find_all(self):
    items = self.execute.find_all(name=self.tag, class_=self.attr)
    output = []
    for element in items:
      output.append(element.text)
    return output


class Document_Author(Document_Base):

  def find_all(self):
    items = self.execute.find_all(name=self.tag, class_=self.attr)
    output = []
    for element in items:
      output.append(element.text)
    return output


class Document_Tags(Document_Base):

  def __init__(self, response, tag_attr_list, internal_list):
    Document_Base.__init__(self, response, tag_attr_list)
    self.meta = internal_list[0]
    self.content = internal_list[1]

  def find_all(self):
    elements = self.execute.find_all(name=self.tag, class_=self.attr)
    output = []
    for element in elements:
      output.append(element.find(self.meta)[self.content].split(FS_META_TAG))
    return output


TAGS_FIELD = "tags"
AUTHOR_FIELD = "author"
QUOTE_FIELD = "quote"
FULLNAME_FIELD = "fullname"
BORN_DATE_FIELD = "born_date"
BORN_LOCATION_FIELD = "born_location"
DESCRIPTION_FIELD = "description"
"""
interface for the dictionaries
use as a Base class for the Quote and Author class
"""


class DictBase(UserDict):

  def print(self):
    for element in self.data:
      print(element + ":" + str(self.data[element]))


class Quote(DictBase):

  def __init__(self, tags, authorname, quote):
    self.data = {}
    self.data[TAGS_FIELD] = tags
    self.data[AUTHOR_FIELD] = authorname
    self.data[QUOTE_FIELD] = quote


class Author(DictBase):

  def __init__(self, fullname, born_date, born_location, description):
    self.data = {}
    self.data[FULLNAME_FIELD] = fullname
    self.data[BORN_DATE_FIELD] = born_date
    self.data[BORN_LOCATION_FIELD] = born_location
    self.data[DESCRIPTION_FIELD] = description
