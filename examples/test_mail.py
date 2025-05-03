import sys
sys.path.append("..")

import json
import datetime as dt
import authorize as auth
from gmail import GMail
from htmlformat import HtmlFormat

config = json.load(open("../data/config.json")) #We load the configuration file...
#auth.update_token(config["ex_auth"], [config["mail_scope"], config["calendar_scope"]]) #First we create or update our token...

#We need an instance of Mail():
#mail = GMail(config["ex_token"], [config["mail_scope"], config["calendar_scope"]])
html = HtmlFormat(config["ex_html"], config["file_prefix"])

#We ask the user the destination email address:
to = input()

#We create some random events...
next_week_events = []
next_week_events.append(["Test", "Evento misterioso", "Un evento loquísimo y misterioso que da que hablar.",
                        dt.datetime(2025,5,10,11,35), dt.datetime(2025,5,10,12,35),
                        (dt.datetime(2025,5,10,11,35)-dt.datetime.today()).days, None])
next_week_events.append(["Test", "Evento misterioso", "Un evento loquísimo y misterioso que da que hablar.",
                        dt.datetime(2025,5,11,11,35), dt.datetime(2025,5,11,12,35),
                        (dt.datetime(2025,5,12,11,35)-dt.datetime.today()).days, "https://meet.google.com/saraza"])
next_week_events.append(["Test", "Evento misterioso", "Un evento loquísimo y misterioso que da que hablar.",
                        dt.datetime(2025,5,15), dt.datetime(2025,5,16),
                        (dt.datetime(2025,5,15)-dt.datetime.today()).days, None])

later_events = []
later_events.append(["Test", "Evento misterioso", "Un evento loquísimo y misterioso que da que hablar.",
                        dt.datetime(2025,5,21), dt.datetime(2025,5,22),
                        (dt.datetime(2025,5,21)-dt.datetime.today()).days, None])
later_events.append(["Test", "Evento misterioso", "Un evento loquísimo y misterioso que da que hablar.",
                        dt.datetime(2025,5,23,10,20), dt.datetime(2025,5,23,10,40),
                        (dt.datetime(2025,5,24)-dt.datetime.today()).days, None])

#We need a body for a html message:
message_body = html.remainders_mail_body(next_week_events, later_events)
file = open("testing.html", "w")
file.write(message_body)
file.close()

#We create the html message...
#html_message = mail.create_html_mail(config["mail"], to, "Test", message_body)

#We create a body for a text message:
message_body = "Hi, how are you?\nThis an example message sent with eds_robot.\nGood luck!"
message_body += "\n\nIMPORTANT: This message was sent by a robot."

#We create the text message...
#message = mail.create_mail(config["mail"], to, "Test", message_body)

#We are ready to send our emails...
#mail.send_mail(config["mail"], to, html_message)
#mail.send_mail(config["mail"], to, message)
