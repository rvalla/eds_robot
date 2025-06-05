import datetime as dt

class Util():
  "The class to store useful functions and data"

  #Getting next monday date...
  def next_monday(self):
    #We insert a 15' offset to avoid all day events from the day before...
    today = dt.datetime.today().replace(hour=0, minute=15, second=0, microsecond=0)
    weekday = today.weekday()
    return today + dt.timedelta(days=7-weekday) 

  #Getting last monday date...
  def last_monday(self):
    #We insert a 15' offset to avoid all day events from the day before...
    today = dt.datetime.today().replace(hour=0, minute=15, second=0, microsecond=0)
    weekday = today.weekday()
    return today - dt.timedelta(days=weekday)

  #Getting today 0:00 date...
  def today(self):
    #We insert a 15' offset to avoid all day events from the day before...
    return dt.datetime.today().replace(hour=0, minute=15, second=0, microsecond=0)

  #Adding days to a date...
  def add_days(self, date, days):
    return date + dt.timedelta(days=days-1, hours=23, minutes=30)

  #Getting the date...
  def iso_today(self):
    return dt.date.today().isoformat()

  #Getting a datetime object from iso format...
  def isoformat_to_date(self, s):
    return dt.date.fromisoformat(s)
  
  #Getting a datetime object from iso format...
  def isoformat_to_datetime(self, s):
    return dt.datetime.fromisoformat(s[:-6])

  #About me...
  def __str__(self):
    return "I am the class where some useful functions are stored."
