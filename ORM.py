import os
import json

from datetime import datetime

from sqlalchemy import ForeignKey, desc, create_engine, func, Column, BigInteger, Integer, Float, String, Boolean, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

if os.environ.get('DATABASE') is not None:
  connectionString = os.environ.get('DATABASE')

engine = create_engine(connectionString, echo=False)

Base = declarative_base()

class Sites(Base):
  __tablename__ = 'sites'

  Id = Column('id', Integer, primary_key=True)
  Value = Column('value', Text)

class Keywords(Base):
  __tablename__ = 'keywords'
  Id = Column('id', Integer, primary_key=True)
  Value = Column('value', Text)

class Ad(Base):
  __tablename__ = 'ads'

  Id = Column('id', BigInteger, primary_key=True)
  Keyword_Id = Column('keyword', Integer, ForeignKey('keywords.id'), primary_key=True)
  Site_Id = Column('site', Integer, ForeignKey('sites.id'), primary_key=True)
  URL = Column('url', Text)
  Fetched = Column('fetched', Boolean)
  Email = Column('email', Text)
  Time = Column('time', DateTime)
  Longitude = Column('longitude', Float)
  Latitude = Column('latitude', Float)
  Notified = Column('notified', Boolean)
  Header = Column('header', Text)



  def __init__(self, data):
    self.Id = data["id"]
    self.URL = data["URL"]
    self.Keyword_Id = data["keyword"]
    self.Site_Id = data["site"]
    self.Fetched = True

  def Update(self, data):
    self.Email = data["email"]
    self.Time = datetime.now()
    self.Longitude = data["longitude"]
    self.Latitude = data["latitude"]
    self.Header = data["header"]
    self.Notified = False

  def Readable(self):
    result = {}
    result["Id"] = self.Id
    result["Data"] = json.loads(self.Data)
    result["Time"] = self.Time

    return result


class Operations:

  def GetAllKeywords():
    return session.query(Keywords).all()

  def GetAllSites():
    return session.query(Sites).all()

  def GetAllUnreadAds():
    return session.query(Ad
      ).filter(Ad.Time == None).all()

  def GetAllUnNotifiedAds():
    return session.query(Ad).filter(Ad.Notified == False, Ad.Email != None).all()

  def SaveAd(data):
    ad = Ad(data)

    exists = session.query(Ad.Id
      ).filter_by(Id=ad.Id, Site_Id=ad.Site_Id
      ).scalar() != None

    if not exists:
      session.add(ad)
      session.commit()

  def UpdateAd(ad_orm, data):
    ad_orm.Update(data)

    session.commit()

  def MarkEmailSent(ad_orm):
    ad_orm.Notified = True
    session.commit()


Base.metadata.create_all(engine)

Session = sessionmaker()
Session.configure(bind=engine)
session = Session()


if __name__ == "__main__":
  print(os.environ.get('DATABASE'))
  print(Operations.GetAllUnreadAds())
