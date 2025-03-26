import base64
from email.message import EmailMessage
from email.mime.text import MIMEText
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class Mail():
  "The class to work with Google Cloud Gmail API"

  #We need our credentials and the service...
  def __init__(self, credentials_path, scopes):
    self.credentials = Credentials.from_authorized_user_file(credentials_path, scopes)
    self.service = service = build("gmail", "v1", credentials=self.credentials)

  #We need to create a MIME mail...
  def create_mail(self, my_address, to, subject, message_text):
    message = MIMEText(message_text)
    message["to"] = to
    message["from"] = my_address
    message["subject"] = subject
    raw_message = base64.urlsafe_b64encode(message.as_string().encode("utf-8"))
    return {"raw": raw_message.decode("utf-8")}

  #We need to create a MIME html mails...
  def create_html_mail(self, my_address, to, subject, message_text):
    message = MIMEText(message_text, "html")
    message["to"] = to
    message["from"] = my_address
    message["subject"] = subject
    raw_message = base64.urlsafe_b64encode(message.as_string().encode("utf-8"))
    return {"raw": raw_message.decode("utf-8")}

  #We can send the message...
  def send_mail(self, my_address, to, message):
    try:
      message = self.service.users().messages().send(userId=my_address, body=message).execute()
      print("Mail sent to " + to + ".", end="\n")
      #return message
    except Exception as e:
      print("Error while trying to send an email.", end="\n")
      #return None

  #About me...
  def __str__(self):
    return "I am the class to work with Google Cloud GMail API."
