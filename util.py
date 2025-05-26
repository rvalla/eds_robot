import datetime as dt

class Util():
  "The class to store useful functions and data"

  #Getting next monday date...
  def next_monday(self):
    today = dt.datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
    weekday = today.weekday()
    return today + dt.timedelta(days=7-weekday) 

  #Getting last monday date...
  def last_monday(self):
    today = dt.datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
    weekday = today.weekday()
    return today - dt.timedelta(days=weekday)

  #Getting a datetime object from iso format...
  def isoformat_to_date(self, s):
    return dt.date.fromisoformat(s)
  
  #Getting a datetime object from iso format...
  def isoformat_to_datetime(self, s):
    return dt.datetime.fromisoformat(s[:-5])

  #About me...
  def __str__(self):
    return "I am the class where some useful functions are stored."
