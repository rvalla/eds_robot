import sys
sys.path.append("..")

import json
import authorize as auth
from gmail import GMail
from htmlformat import HtmlFormat

print("I am ready to test my mailing capabilities...", end="\n")
config = json.load(open("../data/config.json")) #We load the configuration file...
auth.update_token(config["ex_auth"], [config["mail_scope"], config["calendar_scope"], config["spreadsheets_scope"]]) #First we create or update our token...

#We need an instance of Mail():
mail = GMail(config["ex_token"], [config["mail_scope"]])
html = HtmlFormat(config["ex_html"], config["file_prefix"])

#We define replacement values for D1, D2, D3 and D4 tags on test_template.html...
targets = ["<<D1>>","<<D2>>","<<D3>>","<<D4>>"]
data = ["Manzana", "Naranja", "Brócoli", "Uva"]

#We need to build a body from our template:
message_body = html.body_from_template("../data/html/test_template.html", targets, data)

#We save our body to check it:
file = open("html/test_mail_template.html", "w")
file.write(message_body)
file.close()

#We ask the user the destination email address:
print("I will send you a mail built from our template. Please tell me an e-mail address:", end="\n")
to = input()

#We create the html message...
html_message = mail.create_html_mail(config["mail"], to, "Template test", message_body)

#We are ready to send our emails...
mail.send_mail(config["mail"], to, html_message)
print("That's all!", end="\n")
