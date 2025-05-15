import re
import json
import datetime as dt
import authorize as auth
from htmlformat import HtmlFormat
from gmail import GMail
from gcalendar import GCalendar

#Before we start we select our configuration paths...
config_path = "data/config.json"
config = json.load(open(config_path)) #We load the configuration file...
t_mails_path = "data/csv/" + config["file_prefix"] + "maillist.csv"
FIRST_MAIL = 0 #The starting point in maillist.csv file...

#We update our token...
auth.update_token("data/", [config["mail_scope"], config["calendar_scope"]])

#We need an instance Html(), GMail() and GCalendar():
html = HtmlFormat("data/", config["file_prefix"])
mail = GMail(config["token"], [config["mail_scope"], config["calendar_scope"]])
calendar = GCalendar(config["token"], [config["mail_scope"], config["calendar_scope"]])

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
  send_first_contact_mail(m[0], calendar.calendars, m[1], m[2], m[3], m[4])

print("That's all!", end="\n")
