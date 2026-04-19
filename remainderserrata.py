import re
import json
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

print("------ REMAINDERS ERRATA-------", end="\n")
print("Let's create and send remainders errata emails...", end="\n")

#We update our token...
credentials = auth.update_token("data/", [config["mail_scope"], config["calendar_scope"], config["spreadsheets_scope"]])

#We need an instance Util(), Html(), GMail() and GCalendar():
ut = Util()
html = HtmlFormat("data/", config["file_prefix"])
mail = GMail(config["token"], credentials)
calendar = GCalendar(credentials, -3)

#Let's interact a little bit with the user...
print("I asume you already corrected the wrong event. Tell me its actual date.")
date_string = input()
errata_date = ut.get_date(date_string)
next_day = ut.add_days(errata_date, 1)

print("Now I need you to tell me the calendar's name.")
calendar_name = input()

#Ready to collect events...
print("I am ready to collect all events in your date...", end="\n")
errata_events = calendar.build_errata_events_list(calendar_name, errata_date, next_day)

#Selecting the wrong events...
print("I have all events in " + calendar_name + " at " + errata_date.strftime("%Y-%m-%d") + ".")

for e in errata_events:
  print("- "+ e[1])

print("\nPlease tell me the names of errata events to send (separated with ',').")
selected_events = input().split(",")
events_to_send = []

for e in errata_events:
  if e[1] in selected_events:
    events_to_send.append(e)

#Let's send an email...
def send_errata_mail(to, events, selected_calendars, later_count, later_tags):
  message_body = html.errata_mail_body(events_to_send)
  html_message = mail.create_html_mail(config["mail"], to, "Robot Del Sol: Fe de erratas", message_body)
  mail.send_mail(config["mail"], to, html_message)

#We can iterate our configuration file now...
t_mails = []
file = open(t_mails_path).readlines()[1:]
for l in file:
  data = l.split(";")
  t_mails.append((data[0], data[1].split(","), int(data[3]), data[4].split(",")))

print("The mailing list was created!", end="\n")
print("I am ready to start sending the errata mails...", end="\n")

for m in t_mails:
  try:
    if calendar_name in m[1]:
      send_errata_mail(m[0], selected_events, m[1], m[2], m[3])
      SENT += 1
  except Exception as e:
    print("I couldn't send anything to " + m[0] + "...", end="\n")
    print(e, end="\n")
    ERRORS += 1
    FAILURES.append(m[0])

#We save our data in stats.csv now...
file = open("data/stats/stats.csv", "a")
line = ut.iso_today() + ";"
line += str(config["testing"]) + ";"
line += "erratas;"
line += str(SENT) + ";"
line += str(ERRORS) + ";"
line += str(FAILURES) + "\n"
file.write(line)
file.close()

print("That's all!", end="\n")
print("-----------", end="\n")
