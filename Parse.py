from selenium import webdriver
import selenium as se
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import urllib3
import time
from urllib.parse import urlparse, parse_qs

from ORM import Operations

states = {"Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR", "Colorado": "CO", "Connecticut": "CT", "Delaware": "DE", "Georgia": "GA", "Hawaii": "HI", "Idaho": "ID", "Illinois": "IL", "Indiana": "IN", "Iowa": "IA", "Kansas": "KS", "Kentucky": "KY", "Louisiana": "LA", "Maine": "ME", "Maryland": "MD", "Massachusetts": "MA", "Michigan": "MI", "Minnesota": "MN", "Mississippi": "MS", "Missouri": "MO", "Montana": "MT", "Nebraska": "NE", "Nevada": "NV", "New Hampshire": "NH", "New Jersey": "NJ", "New Mexico": "NM", "North Carolina": "NC", "North Dakota": "ND", "Ohio": "OH", "Oklahoma": "OK", "Oregon": "OR", "Pennsylvania": "PA", "Rhode Island": "RI", "South Carolina": "SC", "South Dakota": "SD", "Tennessee": "TN", "Utah": "UT", "Vermont": "VT", "Virginia": "VA", "Washington": "WA", "West Virginia": "WV", "Wisconsin": "WI", "Wyoming": "WY"}

def getAllSites():
  url = "https://geo.craigslist.org/iso/us/{}"
  for k,v in states.items():
    driver = openPage(url.format(v))
    soup = driverToBS4(driver)

    sites = soup.find_all("div", class_="geo-site-list-container")
    if len(sites) > 0:
      links = sites[0].find_all("a")
      for p in links:
        print(p['href'])

    else: 
      print(k,v)

    driver.quit()

def openPage(url):
  try:
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options, executable_path='/usr/bin/geckodriver')
    driver.get(url)

    return driver

  except Exception as e:
    return None


def driverToBS4(driver):
  source = driver.page_source
  soup = BeautifulSoup(source, "lxml")

  return soup


class AdParser:
  driver = None
  longitude = None
  latitude = None
  email = None
  header = None
  URL = None

  def __init__(self, url):
    self.URL = url
    self.readAd()

  def ORMObject(self):
    result = {}
    result["longitude"] = self.longitude
    result["latitude"] = self.latitude
    result["email"] = self.email
    result["header"] = self.header
    result["URL"] = self.URL

    return result

  def readAd(self):

    self.driver = openPage(self.URL)

    if self.driver is None:
      return

    self.setGeolocation()
    self.setHeader()
    self.setEmail()

    self.driver.quit()


  def setHeader(self):

    try:
      soup = driverToBS4(self.driver)
      headers = soup.find_all("h2", class_="postingtitle")
      self.header = [x.text.replace('\n', '') for x in headers][0]

    except Exception as e:
      pass

  def setEmail(self):

    try:
      rebtn = self.driver.find_element_by_css_selector('.reply-button.js-only')
      rebtn.click()

      counter = 0

      while counter < 10:
        soup = driverToBS4(self.driver)
        emailItems = soup.find_all("a", class_="mailapp")

        if len(emailItems) > 0:
          self.email = emailItems[0].text
          break

        time.sleep(.5)
        counter += 1

    except Exception as e:
      pass

  def setGeolocation(self):

    try:

      soup = driverToBS4(self.driver)

      maps = soup.find_all("div", class_="viewposting leaflet-container leaflet-touch leaflet-fade-anim leaflet-grab leaflet-touch-drag leaflet-touch-zoom")

      if len(maps) > 0:
        pin = maps[0]

      self.longitude = pin["data-longitude"]
      self.latitude = pin["data-latitude"]

    except Exception as e:
      pass

class AdListParser:
  searchPre = "{}/search/hhh?query=\"{}\""
  ads = []

  def __init__(self, sites, keywords):
    for site in sites[0:10]:
      for keyword in keywords:
        url = self.searchPre.format(site.Value, keyword.Value)
        ad_list = self.fetchAdLinks(url)

        if len(ad_list) > 0:
          for ad in ad_list:

            try:
              data = {}
              data['id'] = int(ad.rsplit('/', 1)[-1].split('.')[0])
              data["URL"] = ad
              data["keyword"] = keyword.Id
              data["site"] = site.Id

              self.ads.append(data)

            except Exception as e:
              pass

  def fetchAdLinks(self, url):
    http = urllib3.PoolManager()
    r = http.request("GET", url)
    soup = BeautifulSoup(r.data, features="lxml")
    linkTags = soup.find_all("a", class_="result-title hdrlnk")
    links = [x['href'] for x in linkTags]

    return links


if __name__ == "__main__":
  sites = Operations.GetAllSites()
  keywords = Operations.GetAllKeywords()
  print([x.Value for x in sites])

  # a = AdListParser(sites, keywords)
  # for x in a.ads:
  #   print(x)
