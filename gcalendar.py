import json as js
import datetime as dt
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class GCalendar():
  "The class to work with Google Cloud Calendar API"

  #We need our credentials and the service...
  def __init__(self, credentials_path, credentials):
    self.today = dt.datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
    self.timezone = dt.timezone(dt.timedelta(hours=-3))
    self.service = service = build("calendar", "v3", credentials=credentials)
    self.calendars = {}
    self.update_calendar_list()

  #To create an event on a calendar...
  def create_event(self, calendar_id, summary, description, start, end, fullday):
    event = {}
    event["summary"] = summary
    event["description"] = description
    event["guestsCanInviteOthers"] = False
    event["guestsCanSeeOtherGuests"] = False
    if fullday:
      event["start"] = {"date": start.isoformat(), "timeZone": "America/Argentina/Buenos_Aires"}
      event["end"] = {"date": end.isoformat(), "timeZone": "America/Argentina/Buenos_Aires"}
    else:
      event["start"] = {"dateTime": start.astimezone(self.timezone).isoformat(), "timeZone": "America/Argentina/Buenos_Aires"}
      event["end"] = {"dateTime": end.astimezone(self.timezone).isoformat(), "timeZone": "America/Argentina/Buenos_Aires"}
    self.service.events().insert(calendarId=calendar_id, body=event).execute()
    print("I created " + summary + " event...", end="\n")

  #To create events from a csv file...
  def create_events(self, file_path):
    lines = open(file_path).readlines()[1:]
    for l in lines:
      event = l[:-1].split(";")
      calendar_id = self.calendars[event[0]]["id"]
      summary = event[1]
      description = event[2]
      fullday, start = self.create_date(event[3], event[4])
      fullday, end = self.create_date(event[5], event[6])
      self.create_event(calendar_id, summary, description, start, end, fullday)

  #To delete an event...
  def delete_event(self, calendar_id, event_id):
    self.service.events().delete(calendarId=calendar_id, eventId=event_id).execute()
    print("I deleted the event " + event_id + " in calendar " + calendar_id + "...", end="\n")

  #To create a datetime object from csv events list...
  def create_date(self, date, time):
    fullday = False
    date_object = None
    if not time == "-":
      d = date.split("/")
      t = time.split(":")
      date_object = dt.datetime(int(d[2]),int(d[1]),int(d[0]),int(t[0]),int(t[1]))
    else:
      d = date.split("/")
      date_object = dt.date(int(d[2]),int(d[1]),int(d[0]))
      fullday = True
    return fullday, date_object

  #To build a merged events list...
  def build_events_list(self, calendars_names, start_date, *, max_results=100):
    all_events = self.get_calendars_events(calendars_names, start_date, max_results=max_results)
    merged_list = []
    for c in range(len(all_events)):
      for e in all_events[c]:
        merged_list.append(self.clean_event_data(calendars_names[c], e))
    merged_list.sort(key=lambda merged_list:merged_list[3])
    return merged_list

  #To build a merged daily events list...
  def build_daily_events_list(self, calendars_names, start_date, end_date):
    all_events = self.get_calendars_events_in_period(calendars_names, start_date, end_date)
    merged_list = []
    for c in range(len(all_events)):
      for e in all_events[c]:
        merged_list.append(self.clean_event_data(calendars_names[c], e))
    merged_list.sort(key=lambda merged_list:merged_list[3])
    return merged_list

  #To extract desired data from events...
  def clean_event_data(self, calendar_name, event):
    data = [calendar_name]
    data.append(event["summary"])
    data.append(event["description"])
    data.append(self.get_event_date(event["start"]))
    data.append(self.get_event_date(event["end"]))
    data.append(self.get_interval(data[3]))
    data.append(data[3].weekday())
    data.append(event["htmlLink"])
    if "hangoutLink" in event:
      data.append(event["htmlLink"])
    else:
      data.append(None)
    return data
    
  #To create a datetime object from event date...
  def get_event_date(self, date_data):
    date = None
    if "dateTime" in date_data:
      date = dt.datetime.fromisoformat(date_data["dateTime"][:-6])
    else:
      date = dt.datetime.fromisoformat(date_data["date"])
    return date

  #To known how many days are left until event...
  def get_interval(self, date):
    return (date-self.today).days

  #To get events from a list of calendars...
  def get_calendars_events(self, calendars_names, start_date, *, max_results=100):
    all_events = []
    for n in calendars_names:
      all_events.append(self.get_calendar_events(self.calendars[n]["id"], start_date, max_results=max_results))
    return all_events

  #To get daily events from a list of calendars...
  def get_calendars_events_in_period(self, calendars_names, start_date, end_date):
    all_events = []
    for n in calendars_names:
      all_events.append(self.get_calendar_events_in_period(self.calendars[n]["id"], start_date, end_date))
    return all_events

  #To get events on a calendar from date...
  def get_calendar_events(self, calendar_id, start_date, *, max_results=100):
    sd = start_date.isoformat() + "Z"
    events = self.service.events().list(calendarId=calendar_id, timeMin=sd,
                                  singleEvents=True, orderBy="startTime",
                                  maxResults=max_results).execute()
    print("I get events in calendar " + calendar_id, end="\n")
    return events.get("items")

  #To get events on a calendar from date...
  def get_calendar_events_in_period(self, calendar_id, start_date, end_date):
    sd = start_date.isoformat() + "Z"
    ed = end_date.isoformat() + "Z"
    events = self.service.events().list(calendarId=calendar_id, timeMin=sd,
                                  timeMax=ed,singleEvents=True,
                                  orderBy="startTime").execute()
    print("I get events in calendar " + calendar_id, end="\n")
    return events.get("items")

  #To get a calendars list for a user...
  def get_calendar_list(self):
    calendar_list = self.service.calendarList().list().execute()
    return calendar_list["items"]

  #To print the calendar list...
  def print_calendar_list(self):
    print("I will print my calendars list...", end="\n")
    for k in self.calendars:
      print("----", end="\n")
      print(self.calendars[k]["summary"], end="\n")
      if "description" in self.calendars[k]:
        print(self.calendars[k]["description"], end="\n")
      print(self.calendars[k]["id"], end="\n")
      print(self.calendars[k]["timeZone"], end="\n")
      print("----", end="\n\n")

  #To update and save our calendar list...
  def update_calendar_list(self):
    print("I will try to update my calendars list...", end="\n")
    calendar_list = self.get_calendar_list()
    self.calendars.clear()
    for item in calendar_list:
      self.calendars[item["summary"]] = {}
      self.calendars[item["summary"]]["summary"] = item["summary"]
      self.calendars[item["summary"]]["id"] = item["id"]
      self.calendars[item["summary"]]["url"] = "https://calendar.google.com/calendar/u/0?cid=" + item["id"]
      self.calendars[item["summary"]]["timeZone"] = item["timeZone"]
      if "description" in item.keys():
        self.calendars[item["summary"]]["description"] = item["description"]

  #About me...
  def __str__(self):
    return "I am the class to work with Google Cloud Calendar API."
