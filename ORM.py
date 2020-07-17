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
    return session.query(Ad).filter(Ad.Notified == False).all()

  def SaveAd(data):
    ad = Ad(data)

    exists = session.query(Ad.Id
      ).filter_by(Id=ad.Id, Site_Id=ad.Site_Id
      ).scalar() != None

    if not exists:
      session.add(ad)
      session.commit()

  def UpdateAd(ad_orm, data):
    print(data)
    ad_orm.Update(data)

    session.commit()


Base.metadata.create_all(engine)

Session = sessionmaker()
Session.configure(bind=engine)
session = Session()


if __name__ == "__main__":
  print(os.environ.get('DATABASE'))
  print(Operations.GetAllUnreadAds())


'''

class Errors(Base):
  __tablename__ = 'errors'

  Id = Column(Integer, primary_key=True)
  Text = Column(Text)
  Time = Column(DateTime)
  URL = Column(Integer)

  def __init__(self, data):
    self.Text = data["Text"]
    self.Time = data["Time"]
    self.URL = data["URL"]

class Car(Base):
  __tablename__ = 'cars'

  Id = Column(Integer, primary_key=True)
  Maker = Column(String)
  Model = Column(String)
  Type = Column(String)
  Price = Column(Integer)
  Description = Column(String)
  Year = Column(Integer)
  Driven = Column(Integer)
  Fuel = Column(String)
  Transmission = Column(String)
  Drive = Column(String)
  ExchangeUp = Column(Boolean)
  ExchangeDown = Column(Boolean)
  Seats = Column(Integer)
  Doors = Column(Integer)
  Valves = Column(Integer)
  Inspected = Column(Boolean)
  Color = Column(String)
  Created = Column(DateTime)
  Sold = Column(DateTime, nullable=True)
  User = Column(String)

  def TryGetInteger(self, value):
    result = 0

    if value.isnumeric():
      result = int(value)

    return result

  def __init__(self, data):
      self.Id = int(data["Id"])
      self.Maker = data["Framleiðandi"]
      self.Model = data["Undirtegund"]
      self.Type = data["Tegund"]
      self.Price = data["Price"]
      self.Description = data["Description"]
      self.Year = self.TryGetInteger(data["Ár"])
      self.Driven = self.TryGetInteger(data["Akstur"].replace(".", ""))
      self.Fuel = data["Eldsneyti"]
      self.Transmission = data["Skipting"]
      self.Drive = data["Hjóladrifin"]
      self.ExchangeUp = data["Skipti"].find("Fyrir dýrari") > 0
      self.ExchangeDown = data["Skipti"].find("Fyrir ódýrari") > 0
      self.Seats = self.TryGetInteger(data["Fjöldi sæta"])
      self.Doors = self.TryGetInteger(data["Fjöldi dyra"])
      self.Valves = self.TryGetInteger(data["Fjöldi strokka"])
      self.Inspected = data["Skoðaður"] == "Já"
      self.Color = data["Litur"]
      self.Created = data["Created"]
      self.User = data["User"]

  def Readable(self):
    obj = {}
    obj["Id"] = self.Id
    obj["Maker"] = self.Maker
    obj["Model"] = self.Model
    obj["Type"] = self.Type
    obj["Price"] = self.Price
    obj["Description"] = self.Description
    obj["Year"] = self.Year
    obj["Driven"] = self.Driven
    obj["Fuel"] = self.Fuel
    obj["Transmission"] = self.Transmission
    obj["Drive"] = self.Drive
    obj["ExchangeUp"] = self.ExchangeUp
    obj["ExchangeDown"] = self.ExchangeDown
    obj["Seats"] = self.Seats
    obj["Doors"] = self.Doors
    obj["Valves"] = self.Valves
    obj["Inspected"] = self.Inspected
    obj["Color"] = self.Color
    obj["Created"] = self.Created
    obj["Sold"] = self.Sold
    obj["User"] = self.User

    return obj


class Operations:

  def LogError(error_data):
    session.add(Errors(error_data))
    session.commit()

  def MarkCarSold(car_id):
    car = session.query(Car).filter_by(Id=car_id).first()
    car.Sold = datetime.now()
    session.commit()

  def SaveCars(cars):
    all_ids = session.query(Car.Id).all()
    session.bulk_save_objects([x for x in cars if x not in all_ids])
    session.commit()

  def SaveCar(car):
    exists = session.query(Car.Id).filter_by(Id=car.Id).scalar() != None

    if not exists:
      session.add(car)
      session.commit()

  def GetUnsoldIDs():
    data = session.query(Car.Id).filter_by(Sold=None).all()
    return [x[0] for x in data]

  def GetAllSold():
    data = session.query(Car).filter(Car.Sold.isnot(None)).all()
    result = []

    for item in data:
      obj = {}
      obj["Id"] = item.Id
      obj["Maker"] = item.Maker
      obj["Model"] = item.Model
      obj["Type"] = item.Type
      obj["Year"] = item.Year
      obj["Driven"] = item.Driven
      obj["Fuel"] = item.Fuel
      obj["Transmission"] = item.Transmission
      obj["Drive"] = item.Drive
      obj["ExchangeUp"] = item.ExchangeUp
      obj["ExchangeDown"] = item.ExchangeDown
      obj["Seats"] = item.Seats
      obj["Doors"] = item.Doors
      obj["Valves"] = item.Valves
      obj["Inspected"] = item.Inspected
      obj["Color"] = item.Color
      obj["Created"] = item.Created
      obj["Sold"] = item.Sold
      obj["User"] = item.User

      result.append(obj)


    return result

  def GetAllIds():
    return [x[0] for x in session.query(Car.Id).all()]


  def GetMakerModelYearByParameters(maker, model, year):
    data = session.query(func.max(Car.Id)
      ).filter_by(Maker=maker, Model=model, Year=year
      ).filter(Car.Price > 2000
      ).group_by(
        Car.Maker,
        Car.Model,
        Car.Year,
        Car.Fuel,
        Car.Transmission,
        Car.Color,
        Car.User
      ).all()

    ids = [x[0] for x in data]

    return [x.Readable() for x in session.query(Car).filter(Car.Id.in_(ids)).all()]

  def GetMakerModelYearCount():
    data = session.query(func.max(Car.Id)
      ).filter(Car.Price > 2000
      ).group_by(
        Car.Maker,
        Car.Model,
        Car.Year,
        Car.Fuel,
        Car.Transmission,
        Car.Color,
        Car.User
      ).all()

    ids = [x[0] for x in data]

    data = session.query(Car.Maker, Car.Model, Car.Year, func.count()
      ).filter(Car.Id.in_(ids)
      ).group_by(Car.Maker, Car.Model, Car.Year
      ).all()

    return [dict(zip(["Maker", "Model", "Year", "Count"], d)) for d in data]

  def GetMakers():
    makers = session.query(Car.Maker, func.count()).group_by(Car.Maker).all()
    makers_dict = {maker[0]: maker[1] for maker in makers}
    return makers_dict

  def GetModels():
    return session.query(Car.Model, func.count()).group_by(Car.Model).all()

  def LogUpdate(data):
    update = Updates(data)
    session.add(update)
    session.commit()

  def GetLogs():
    updates = session.query(Updates).order_by(desc(Updates.Time)).limit(10).all()
    return [x.Readable() for x in updates]

Base.metadata.create_all(engine)



from sqlalchemy.orm import sessionmaker
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()
'''
