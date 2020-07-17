import smtplib
from email.mime.text import MIMEText as text
from ORM import Operations

class Email:
  user = None
  ads = None
  email1 = '\nHi\nIs this still on the market?\nIs there any deferred maintenance and expected costs?\nFull address & zip for me to run some comps\nIs there some flexibility on the purchase price for an all cash fast sale?\n\nThanks\nNathan\n\n{}'
  email2 = '\nHi\nIs this still on the market?\nAre there any deferred maintenance and expected costs?\nWhat is the gross rent?\nWho pays utilities?\nFull address & zip for me to run some comps\nIs there some flexibility on the purchase price for an all cash fast sale?\n\nThanks\nNathan\n\n{}'

  def __init__(self, user, ads):
    self.user = user
    self.ads = ads

  def run(self):
    for ad in self.ads:
      self.sendmail(ad)

  def sendmail(self, ad):
    from_address= self.user['email']

    smtp_server = 'smtp.gmail.com'
    smtp_port= 587
    smtp_user= self.user['email']
    smtp_password= self.user['password']

    if (ad.Keyword_Id <= 5):
      msg = text(self.email1.format(ad.URL))

    else:
      msg = text(self.email2.format(ad.URL))

    msg['Subject'] = ad.Header
    msg['From'] = self.user['email']
    msg['To'] = 'isebarn182@gmail.com' #ad.Email

    server = smtplib.SMTP(smtp_server, smtp_port)
    server.ehlo()
    server.starttls()
    server.login(smtp_user, smtp_password)
    server.sendmail(self.user['email'], 'isebarn182@gmail.com', msg.as_string())
    server.quit()

if __name__ == "__main__":
  user = {}
  user['email'] = 'isebarn182@gmail.com'
  user['password'] = 'tommy182'

  ads = Operations.GetAllUnNotifiedAds()[1:10]
  email = Email(user, ads)
  email.run()


# https://stackoverflow.com/questions/16512592/login-credentials-not-working-with-gmail-smtp
