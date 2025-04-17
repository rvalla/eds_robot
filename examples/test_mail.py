import sys
sys.path.append("..")

import json
import authorize as auth
from gmail import GMail

config = json.load(open("../data/config.json")) #We load the configuration file...
auth.update_token("../data/", [config["mail_scope"], config["calendar_scope"]]) #First we create or update our token...

#We need an instance of Mail():
mail = GMail(config["ex_token"], [config["mail_scope"], config["calendar_scope"]])

#We ask the user the destination email address:
to = input()

#We need a body for a html message:
message_body = "<html>"
message_body += open("../data/html/test.css").read() #We load the css header...
message_body += "<body>"
message_body += open("../data/html/test_header.html").read() #We write the header...
message_body += "<tr><td colspan=3><h1>This is a test</h1></td></tr>"
message_body += "<tr><td colspan=3><h2>A first email in html</h2></td></tr>"
message_body += "<tr><td colspan=3><h3>We are using a table</h3></td></tr>"
message_body += """<tr><td>X</td><td>O</td><td>X</td></tr>
                <tr><td>X</td><td>X</td><td>0</td></tr>
                <tr><td>O</td><td>X</td><td>O</td></tr>"""
message_body += "<tr><td colspan=3 style='color:#cccccc;'>This message was sent by a robot.</td></tr>"
message_body += open("../data/html/test_footer.html").read() #We write our footer...
message_body += "</body></html>"

#We create the html message...
html_message = mail.create_html_mail(config["mail"], to, "Test", message_body)

#We create a body for a text message:
message_body = "Hi, how are you?\nThis an example message sent with eds_robot.\nGood luck!"
message_body += "\n\nIMPORTANT: This message was sent by a robot."

#We create the text message...
message = mail.create_mail(config["mail"], to, "Test", message_body)

#We are ready to send our emails...
mail.send_mail(config["mail"], to, html_message)
mail.send_mail(config["mail"], to, message)
