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
t_mails_path = "data/csv/" + config["file_prefix"] + "maillist_daily.csv"
SENT = 0
ERRORS = 0
FAILURES = []

print("------ DAILY REMAINDERS -------", end="\n")
print("Let's create and send our daily remainders...", end="\n")

#We update our token...
credentials = auth.update_token("data/", [config["mail_scope"], config["calendar_scope"], config["spreadsheets_scope"]])

#We need an instance Util(), Html(), GMail() and GCalendar():
ut = Util()
html = HtmlFormat("data/", config["file_prefix"])
mail = GMail(config["token"], credentials)
calendar = GCalendar(config["token"], credentials)

#We load the targeted calendars...
t_calendars = []
file = open(t_calendars_path).readlines()[1:]
for l in file:
  t_calendars.append(l.split(";")[0])
print("The current list of calendars is:", end=" ")
print(t_calendars, end="\n")
today = ut.today()
tomorrow = today + dt.timedelta(days=1)

#Ready to collect all events...
print("I am ready to collect all events in the next weeks...", end="\n")
all_events = calendar.build_daily_events_list(t_calendars, today, tomorrow)

#Filtering all events to get a personalize user list...
def filter_events(events, selected_calendars):
  daily_events = []
  n = 0
  s = 0
  while n < len(all_events):
    if events[n][0] in selected_calendars:
      daily_events.append(events[n])
    n += 1
  return daily_events

#Let's send an email...
def send_daily_remainders_mail(to, events, selected_calendars):
  daily_events = filter_events(events, selected_calendars)
  message_body = html.daily_remainders_mail_body(daily_events)
  html_message = mail.create_html_mail(config["mail"], to, "Robot Del Sol: Tu agenda de hoy", message_body)
  mail.send_mail(config["mail"], to, html_message)

#We can iterete our configuration file now...
t_mails = []
file = open(t_mails_path).readlines()[1:]
for l in file:
  data = l.split(";")
  t_mails.append((data[0], data[1].split(",")))

print("The mailing list was created!", end="\n")
print("I am ready to start sending mails...", end="\n")

for m in t_mails:
  try:
    send_daily_remainders_mail(m[0], all_events, m[1])
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
line += "dailyremainders;"
line += str(SENT) + ";"
line += str(ERRORS) + ";"
line += str(FAILURES) + "\n"
file.write(line)
file.close()

print("That's all!", end="\n")
