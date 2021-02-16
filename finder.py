# Get all search results:
# document.querySelectorAll('.g .tF2Cxc');

import os
from selenium import webdriver
from paths import *
from json_utils import *
import urllib.request

links_json = {}
scraper = None
driver = None

if not os.path.isdir(GECKO_PATH):
  os.makedirs(GECKO_PATH)
  url = 'https://download1582.mediafire.com/e72loo1dznvg/lhkrdzx2etmpwvv/geckodriver.exe'
  urllib.request.urlretrieve(url, GECKO_PATH + '\\geckodriver.exe')

if not os.path.isdir(JSON_DIR):
  os.makedirs(JSON_DIR)
  if not os.path.isfile(JSON_PATH):
    open(JSON_PATH, 'w+')
    write_json({'links':[]})

class Link:
  def __init__(self, url, text):
    self.full_url: str = url
    self.text = text
    self.website = self.full_url.split('/')[2] # Calculate the website

  def check_same(self, other):
    return self.website == other.website

  def print(self):
    print(self.website)

class Scraper:
  def __init__(self, driver = None):
    self.webdriver: webdriver.Firefox = driver

  def set_driver(self, driver):
    self.webdriver = driver

  def search(self, term, gender, age):
    url = f'https://www.amazon.co.uk/s?k={f"{term}+costume+for+{gender}+{age}"}'
    self.webdriver.get(url)
    links = []
    for elem in self.webdriver.find_elements_by_css_selector('.s-result-item h2 a.a-link-normal.a-text-normal'):
      href = elem.get_attribute('href')
      text = elem.get_attribute('textContent').strip()
      links.append(Link(href, text))
    links = links[:10]

    links_json['links'].append({
      'search_term': term,
      'links': [{'url':l.full_url,'title':l.text} for l in links]
    })
    driver.close()
    write_json(links_json)
    print('Saved to a JSON File!')
    see_links = input('Do you want to see the links now (Y/n)? ') or 'y'
    if see_links == 'y':
      print('Getting links...')
      path = JSON_DIR + '\\costume_links.txt'
      with open(path, 'w') as f:
        string = ''
        for link in links_json['links'][-1]['links']:
          string += f'{link["title"]}:\n\n{link["url"]}\n\n\n'
        f.write(string)
      os.system(f'notepad {path}')
    raise KeyboardInterrupt

try:
  links_json = read_json()
  scraper = Scraper()
  term = input('What costume do you want? (anything) ') or 'batman'
  age = input('Age for costume? (kid/adult) ') or 'kid'
  gender = input('Boy or girl? (boy/girl) ') or 'boy'
  driver = webdriver.Firefox(executable_path=FULL_GECKO_PATH)
  scraper.set_driver(driver)
  scraper.search(term, gender, age)
except KeyboardInterrupt:
  print('Exiting')
