from Parse import AdParser, AdListParser
from ORM import Operations
from Email import Email
import sys
import random
import os

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

def RUN_SendEmails(user, test=False):
  ads = Operations.GetAllUnNotifiedAds()[1:10]

  if test:
    ads = [random.choice(ads)]
    ads[0].Email = user['email']

  email = Email(user, ads)
  email.run()

if __name__ == "__main__":
  args = sys.argv
  argscount = len(args)
  cmd = args[1] if argscount > 1 else 'GetAdList'
  test = args[2] == 'True' if argscount > 2 else True

  if cmd == 'GetAdList':
    RUN_GetAdList(test)

  elif cmd == 'GetAdData':
    RUN_GetAdData(test)

  elif cmd == 'SendEmails':
    user = {}
    user['email'] = args[3] if argscount > 4 else os.environ.get('EMAIL')
    user['password'] = args[4] if argscount > 4 else os.environ.get('PASSWORD')

    RUN_SendEmails(user, test)
