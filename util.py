import datetime as dt

class Util():
  "The class to store useful functions and data"

  #Getting next monday date...
  def next_monday(self):
    today = dt.date.today()
    weekday = today.weekday()
    return today + dt.timedelta(days=7-weekday)    

  #Getting a date object from iso format...
  def isoformat_to_date(self, s):
    return dt.datetime.fromisoformat(s)
  
  #Getting a datetime object from iso format...
  def isoformat_to_datetime(self, s):
    return dt.datetime.fromisoformat(s[:-5])

  #About me...
  def __str__(self):
    return "I am the class where some useful functions are stored."
