from Parse import AdParser, AdListParser
from ORM import Operations
import sys
import random

def RUN_GetAdData(test=False):

  unread_ads = Operations.GetAllUnreadAds()

  if test:
    unread_ads = [random.choice(unread_ads)]

  for unread_ad in unread_ads:
    parsed_ad = AdParser(unread_ad.URL)
    ad = parsed_ad.ORMObject()
    Operations.UpdateAd(unread_ad, ad)


def RUN_GetAdList(test=False):
  sites = Operations.GetAllSites()
  keywords = Operations.GetAllKeywords()

  if test:
    sites = [random.choice(sites)]
    keywords = [random.choice(keywords)]

  ads = AdListParser(sites, keywords)

  for ad in ads.ads:
    Operations.SaveAd(ad)


if __name__ == "__main__":
  cmd = sys.argv[1] if len(sys.argv) > 1 else 'GetAdList'
  test = sys.argv[2] == 'True' if len(sys.argv) > 2 else True

  if cmd == 'GetAdList':
    RUN_GetAdList(test)

  elif cmd == 'GetAdData':
    RUN_GetAdData(test)
