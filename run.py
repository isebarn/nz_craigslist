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

  counter = 0
  for unread_ad in unread_ads:
    counter += 1
    print('{}/{}'.format(counter, len(unread_ads)))
    parsed_ad = AdParser(unread_ad.URL)
    ad = parsed_ad.ORMObject()
    Operations.UpdateAd(unread_ad, ad)


def RUN_GetAdList(test=False):
  sites = Operations.GetAllSites()
  keywords = Operations.GetAllKeywords()
  exclusions = Operations.GetAllExclusions()

  if test:
    sites = [random.choice(sites)]
    keywords = [random.choice(keywords)]

  ads = AdListParser(sites, keywords, exclusions)

  for ad in ads.ads:
    Operations.SaveAd(ad)

def RUN_SendEmails(user, test=False):
  ads = Operations.GetAllUnNotifiedAds()
  for x in ads:
    ad_title = x.URL.split('/d/')[-1].split('/')[0]

    if ad_title in new_ads:
      x.Notified = True
      Operations.MarkEmailSent(x)

    else:
      new_ads.append(ad_title)

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
