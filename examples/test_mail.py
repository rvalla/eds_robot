import sys
sys.path.append("..")

import json
import datetime as dt
import authorize as auth
from gmail import GMail
from htmlformat import HtmlFormat

print("I am ready to test my mailing capabilities...", end="\n")
config = json.load(open("../data/config.json")) #We load the configuration file...
credentials = auth.update_token(config["ex_auth"], #First we get our credentials...
                [config["mail_scope"], config["calendar_scope"], config["spreadsheets_scope"]])

#We need an instance of Mail():
mail = GMail(config["ex_token"], credentials)
html = HtmlFormat(config["ex_html"], config["file_prefix"])

#We create some random events...
next_week_events = []
next_week_events.append(["Test", "Evento misterioso", "Un evento loquísimo y misterioso que da que hablar.",
                        dt.datetime(2025,5,10,11,35), dt.datetime(2025,5,10,12,35),
                        (dt.datetime(2025,5,10,11,35)-dt.datetime.today()).days,
                        dt.datetime(2025,5,10,11,35).weekday(), "https://calendar.google.com/saraza", None])
next_week_events.append(["Test", "Evento misterioso", "Un evento loquísimo y misterioso que da que hablar.",
                        dt.datetime(2025,5,11,11,35), dt.datetime(2025,5,11,12,35),
                        (dt.datetime(2025,5,12,11,35)-dt.datetime.today()).days,
                        dt.datetime(2025,5,11,11,35).weekday(), "https://calendar.google.com/saraza", "https://meet.google.com/saraza"])
next_week_events.append(["Test", "Evento misterioso", "Un evento loquísimo y misterioso que da que hablar.",
                        dt.datetime(2025,5,15), dt.datetime(2025,5,16),
                        (dt.datetime(2025,5,15)-dt.datetime.today()).days,
                        dt.datetime(2025,5,15,11,35).weekday(), "https://calendar.google.com/saraza", None])

later_events = []
later_events.append(["Test", "Evento misterioso", "Un evento loquísimo y misterioso que da que hablar.",
                        dt.datetime(2025,5,21), dt.datetime(2025,5,22),
                        (dt.datetime(2025,5,21)-dt.datetime.today()).days,
                        dt.datetime(2025,5,21).weekday(), "https://calendar.google.com/saraza", None])
later_events.append(["Test", "Evento misterioso", "Un evento loquísimo y misterioso que da que hablar.",
                        dt.datetime(2025,5,23,10,20), dt.datetime(2025,5,23,10,40),
                        (dt.datetime(2025,5,24)-dt.datetime.today()).days,
                        dt.datetime(2025,5,24).weekday(), "https://calendar.google.com/saraza", None])

#We need a body for a html message:
message_body = html.remainders_mail_body(next_week_events, later_events)

#We save our body to check it:
file = open("html/test_mail.html", "w")
file.write(message_body)
file.close()

#We ask the user the destination email address:
print("I will create a random calendars remainder. Please tell me an e-mail address:", end="\n")
to = input()

#We create the html message...
html_message = mail.create_html_mail(config["mail"], to, "Test", message_body)

#We are ready to send our emails...
mail.send_mail(config["mail"], to, html_message)
print("That's all!", end="\n")
