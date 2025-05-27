import sys
sys.path.append("..")

import json
import random as rd
import datetime as dt
import authorize as auth
from gcalendar import GCalendar

config = json.load(open("../data/config.json")) #We load the configuration file...
credentials = auth.update_token(config["ex_auth"], #First we get our credentials...
                [config["mail_scope"], config["calendar_scope"], config["spreadsheets_scope"]])

#We need an instance of GCalendar():
calendar = GCalendar(config["ex_token"], credentials)

#We need some random events...
#We are going to create and delete a set of events...
events_count = 5
events_count_in_file = 20
calendars = ["robot@eds.edu.ar", "Test (BOT)"]
today_t = dt.datetime.today()
today_d = dt.date.today()
cleaning = False #Deciding if we delete our random events at the end of this test...

#We create a file to test bulk event creation:
events_file = open("../data/csv/test_calendarevents.csv", "w")
events_file.write("calendar_name;event_summary;event_description;start_date;start_time;end_date;end_time\n")
for e in range(events_count_in_file):
  events_file.write(rd.choice(calendars) + ";")
  events_file.write("Test " + str(e+1) + ";")
  events_file.write("This is a bulk test using test_calendar.py in /examples" + rd.choice([" #importante","",""]) +  ".;")
  if rd.random() < 0.4:
    start_date = today_d + dt.timedelta(days=rd.randint(0,30))
    end_date = start_date + dt.timedelta(days=1)
    events_file.write(str(start_date.day) + "/" + str(start_date.month) + "/" + str(start_date.year) + ";-;")
    events_file.write(str(end_date.day) + "/" + str(end_date.month) + "/" + str(end_date.year) + ";-\n")
  else:
    start_date = today_t + dt.timedelta(days=rd.randint(0,30), hours=rd.randint(0,23))
    end_date = start_date + dt.timedelta(hours=rd.randint(0,4), minutes=rd.randint(30,60))
    events_file.write(str(start_date.day) + "/" + str(start_date.month) + "/" + str(start_date.year) + ";")
    events_file.write(str(start_date.hour) + ":" + str(start_date.minute) + ";")
    events_file.write(str(end_date.day) + "/" + str(end_date.month) + "/" + str(end_date.year) + ";")
    events_file.write(str(end_date.hour) + ":" + str(end_date.minute) + "\n")
events_file.close()

#We are ready to create some events:
for e in range(events_count):
  if rd.random() < 0.4:
    start_date = today_d + dt.timedelta(days=rd.randint(0,14))
    end_date = start_date + dt.timedelta(days=1)
    calendar.create_event(calendar.calendars[rd.choice(calendars)]["id"], "Test " + str(e+1), "Testing EDS Robot event creation function.", start_date, end_date, True)
  else:
    start_date = today_t + dt.timedelta(days=rd.randint(0,14), hours=rd.randint(0,23))
    end_date = start_date + dt.timedelta(hours=rd.randint(0,4), minutes=rd.randint(30,60))
    calendar.create_event(calendar.calendars[rd.choice(calendars)]["id"], "Test " + str(e+1), "Testing EDS Robot event creation function.", start_date, end_date, False)

#We now create all events in our recently created file:
calendar.create_events("../data/csv/test_calendarevents.csv")

#We now can retrieve our events...
all_events = []
for c in calendars:
  all_events.append(calendar.get_calendar_events(calendar.calendars[c]["id"], today_t))

#We check events in our calendar...
for c in range(len(calendars)):
  for e in all_events[c]:
    print(calendars[c] + " - " + e["summary"] + " - " + str(e["start"]), end="\n")

#We clean our calendars to end this test...
if cleaning:
  for c in range(len(calendars)):
    for e in all_events[c]:
      calendar.delete_event(calendar.calendars[calendars[c]]["id"], e["id"])
