import re
import json
import authorize as auth
from util import Util
from htmlformat import HtmlFormat
from gmail import GMail
from gcalendar import GCalendar

#Before we start we select our configuration paths...
config_path = "data/config.json"
config = json.load(open(config_path)) #We load the configuration file...
t_mails_path = "data/csv/" + config["file_prefix"] + "maillist.csv"
FIRST_MAIL = None #The starting point in maillist.csv file...
SENT = 0
ERRORS = 0
FAILURES = []
if config["testing"]:
  FIRST_MAIL = 0
else:
  FIRST_MAIL = config["last_first_contact"]

print("------ REMAINDERS: FIRST CONTACT -------", end="\n")
print("Let's create and send our first contact to new users of remainders...", end="\n")

#We update our token...
credentials = auth.update_token("data/", [config["mail_scope"], config["calendar_scope"], config["spreadsheets_scope"]])

#We need an instance Util(), Html(), GMail() and GCalendar():
ut = Util()
html = HtmlFormat("data/", config["file_prefix"])
mail = GMail(config["token"], credentials)
calendar = GCalendar(credentials, -3)

#Let's send an email...
def send_first_contact_mail(to, calendars_data, calendars_suscriptions, calendars_permissions, later_count, later_tags):
  message_body = html.remainders_first_contact_mail_body(calendars_data, calendars_suscriptions, calendars_permissions, later_count, later_tags)
  html_message = mail.create_html_mail(config["mail"], to, "Robot Del Sol: ¡Mucho gusto!", message_body)
  mail.send_mail(config["mail"], to, html_message)

#We can iterete our configuration file now...
t_mails = []
file = open(t_mails_path).readlines()[1:]
for l in range(FIRST_MAIL,len(file)):
  data = file[l].split(";")
  t_mails.append((data[0], data[1].split(","), data[2].split(","), int(data[3]), data[4].split(",")))

print("The mailing list was created!", end="\n")
print("I am ready to start sending mails...", end="\n")

for m in t_mails:
  try:
    send_first_contact_mail(m[0], calendar.calendars, m[1], m[2], m[3], m[4])
    SENT += 1
  except Exception as e:
    print("I couldn't send anything to " + m[0] + "...", end="\n")
    print(e, end="\n")
    ERRORS += 1
    FAILURES.append(m[0])

#We save our data in stats.csv now...
file = open("data/csv/stats.csv", "a")
line = ut.iso_today() + ";"
line += str(config["testing"]) + ";"
line += "first_contact;"
line += str(SENT) + ";"
line += str(ERRORS) + ";"
line += str(FAILURES) + "\n"
file.write(line)
file.close()

print("That's all!", end="\n")
print("-----------", end="\n")
