import json
import authorize as auth
from htmlformat import HtmlFormat
from util import Util
from gmail import GMail

#Before we start we select our configuration paths...
config_path = "data/config.json"
config = json.load(open(config_path)) #We load the configuration file...
t_mails_path = "data/csv/" + config["file_prefix"] + "maillist.csv"
SUCCESS = 0 #To check if we have data to send...
SENT = 0
ERRORS = 0
FAILURES = []
subject = None
mail_body = None

print("------ Ad Hoc mails -------", end="\n")
print("Let's send a custom mail to our maillist...", end="\n")
print("Please give me an email subject:", end="\n")
subject = input()
print("Now give me the path to the file where the email body is:", end="\n")
mail_body = input()

#We update our token...
credentials = auth.update_token("data/", [config["mail_scope"], config["calendar_scope"], config["spreadsheets_scope"]])

#We need an instance Util(), Html(), GMail() and GSpreadsheets():
ut = Util()
html = HtmlFormat("data/", config["file_prefix"])
mail = GMail(config["token"], credentials)

#Let's define a function to send emails...
def send_mail(to, body):
  html_message = mail.create_html_mail(config["mail"], to, "Robot Del Sol: " + subject, body)
  mail.send_mail(config["mail"], to, html_message)

#Building message's body...
message_body = html.adhoc_body("data/html/" + mail_body)

#We can iterete our configuration file now...
t_mails = []
file = open(t_mails_path).readlines()[1:]
for l in file:
  aux = l.split(";")
  if aux[5] == "1": #We add only some addresses...
    t_mails.append(aux[0])

print("The mailing list was created!", end="\n")
print("I am ready to start sending mails...", end="\n")

for m in t_mails:
  try:
    send_mail(m, message_body)
    SENT += 1
  except Exception as e:
    print("I couldn't send anything to " + m + "...", end="\n")
    print(e, end="\n")
    ERRORS += 1
    FAILURES.append(m[0])

#We save our data in stats.csv now...
file = open("data/stats/stats.csv", "a")
line = ut.iso_today() + ";"
line += str(config["testing"]) + ";"
line += "adhoc;"
line += str(SENT) + ";"
line += str(ERRORS) + ";"
line += str(FAILURES) + "\n"
file.write(line)
file.close()

print("That's all!", end="\n")
print("-----------", end="\n")
