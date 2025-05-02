import json as js
import datetime as dt
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class GCalendar():
  "The class to work with Google Cloud Calendar API"

  #We need our credentials and the service...
  def __init__(self, credentials_path, scopes):
    self.timezone = dt.timezone(dt.timedelta(hours=-3))
    self.credentials = Credentials.from_authorized_user_file(credentials_path, scopes)
    self.service = service = build("calendar", "v3", credentials=self.credentials)
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

  #To list events on a calendar from date...
  def get_calendar_events(self, calendar_id, start_date, *, max_results=200):
    sd = start_date.isoformat() + "Z"
    events = self.service.events().list(calendarId=calendar_id, timeMin=sd,
                                  singleEvents=True, orderBy="startTime",
                                  maxResults=max_results).execute()
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
      self.calendars[item["summary"]]["timeZone"] = item["timeZone"]
      if "description" in item.keys():
        self.calendars[item["summary"]]["description"] = item["description"]
  
  #About me...
  def __str__(self):
    return "I am the class to work with Google Cloud Calendar API."
