import re
import json
import datetime as dt
import authorize as auth
from htmlformat import HtmlFormat
from util import Util
from gmail import GMail
from gcalendar import GCalendar

#Before we start we select our configuration paths...
config_path = "data/config.json"
config = json.load(open(config_path)) #We load the configuration file...
t_calendars_path = "data/csv/" + config["file_prefix"] + "calendarlist.csv"
t_mails_path = "data/csv/" + config["file_prefix"] + "maillist.csv"
SENT = 0
ERRORS = 0
FAILURES = []

print("------ WEEKLY REMAINDERS -------", end="\n")
print("Let's create and send our daily remainders...", end="\n")

#We update our token...
credentials = auth.update_token("data/", [config["mail_scope"], config["calendar_scope"], config["spreadsheets_scope"]])

#We need an instance Util(), Html(), GMail() and GCalendar():
ut = Util()
html = HtmlFormat("data/", config["file_prefix"])
mail = GMail(config["token"], credentials)
calendar = GCalendar(credentials, -3)

#We load the targeted calendars...
t_calendars = []
file = open(t_calendars_path).readlines()[1:]
for l in file:
  t_calendars.append(l.split(";")[0])
print("The current list of calendars is:", end=" ")
print(t_calendars, end="\n")
next_monday = ut.next_monday()
next_sunday = next_monday + dt.timedelta(days=6)

#Ready to collect all events...
print("I am ready to collect all events in the next weeks...", end="\n")
all_events = calendar.build_events_list(t_calendars, next_monday)

#To decide is the event contains any later tags...
def is_later_event(tags, event):
  is_important = False
  for t in tags:
    if bool(re.search(t, event)):
      is_important = True
      break
  return is_important

#Filtering all events to get a personalize user list...
def filter_events(events, selected_calendars, later_count, later_tags):
  next_week_events = []
  later_events = []
  n = 0
  s = 0
  while events[n][3] < next_sunday and n < len(all_events):
    if events[n][0] in selected_calendars:
      next_week_events.append(events[n])
    n += 1
  while s < later_count and n < len(events):
    if is_later_event(later_tags, events[n][2]) and events[n][0] in selected_calendars:
      later_events.append(events[n])
      s += 1
    n += 1
  return next_week_events, later_events

#Let's send an email...
def send_remainders_mail(to, events, selected_calendars, later_count, later_tags):
  next_week_events, later_events = filter_events(events, selected_calendars, later_count, later_tags)
  message_body = html.remainders_mail_body(next_week_events, later_events)
  html_message = mail.create_html_mail(config["mail"], to, "Robot Del Sol: Próxima semana", message_body)
  mail.send_mail(config["mail"], to, html_message)

#We can iterete our configuration file now...
t_mails = []
file = open(t_mails_path).readlines()[1:]
for l in file:
  data = l.split(";")
  t_mails.append((data[0], data[1].split(","), int(data[3]), data[4].split(",")))

print("The mailing list was created!", end="\n")
print("I am ready to start sending mails...", end="\n")

for m in t_mails:
  try:
    send_remainders_mail(m[0], all_events, m[1], m[2], m[3])
    SENT += 1
  except Exception as e:
    print("I couldn't send anything to " + m[0] + "...", end="\n")
    print(e, end="\n")
    ERRORS += 1
    FAILURES.append(m[0])

#We save our data in stats.csv now...
file = open("data/csv/stats.csv", "a")
line = dt.date.today().isoformat() + ";"
line += str(config["testing"]) + ";"
line += "remainders;"
line += str(SENT) + ";"
line += str(ERRORS) + ";"
line += str(FAILURES) + "\n"
file.write(line)
file.close()

print("That's all!", end="\n")
