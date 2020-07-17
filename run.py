from Parse import AdParser, AdListParser
from ORM import Operations

def save_ad_data(ad_orm, url):
  parser = AdParser(url)
  ad = parser.ORMObject()
  Operations.UpdateAd(ad_orm, ad)

def RUN_GetAd():
  unread_ads = Operations.GetAllUnreadAds()
  for unread_ad in unread_ads:
    save_ad_data(unread_ad, unread_ad.URL)

def RUN_GetAdList():
  sites = Operations.GetAllSites()
  keywords = Operations.GetAllKeywords()

  ads = AdListParser(sites, keywords)

  for ad in ads.ads:
    Operations.SaveAd(ad)



if __name__ == "__main__":
  #RUN_GetAdList()
  RUN_GetAd()

