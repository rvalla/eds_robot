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
      event["start"] = {"date": str(start.year) + "-" + str(start.month) + "-" + str(start.day), "timeZone": "America/Argentina/Buenos_Aires"}
      event["end"] = {"date": str(end.year) + "-" + str(end.month) + "-" + str(end.day), "timeZone": "America/Argentina/Buenos_Aires"}
    else:
      event["start"] = {"dateTime": start.astimezone(self.timezone).isoformat(), "timeZone": "America/Argentina/Buenos_Aires"}
      event["end"] = {"dateTime": end.astimezone(self.timezone).isoformat(), "timeZone": "America/Argentina/Buenos_Aires"}
    print(event)
    self.service.events().insert(calendarId=calendar_id, body=event).execute()

  #To create events from a csv file...
  def create_events(self, file_path, separator):
    lines = open(filepath).read_lines()[1:]
    

  #To list events on a calendar from date...
  def get_calendar_events(self, calendar_id, start_date):
    sd = start_date.isoformat() + "Z"
    events = self.service.events().list(calendarId=calendar_id, timeMin=sd,
                                  singleEvents=True, maxResults=200).execute()
    return events.get("items")    

  #To get a calendars list for a user...
  def get_calendar_list(self):
    token = None
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
