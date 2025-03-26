import os.path
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

def update_token():
  #List of apis to authorize...
  config = json.load(open("data/config.json"))
  SCOPES = [config["mail_scope"], config["calendar_scope"]]

  print("I will try to authorize the following Google Cloud APIs:", end="\n")
  for s in SCOPES:
    print("- " + s, end="\n")

  credentials = None
  if os.path.exists("data/token.json"):
    credentials = Credentials.from_authorized_user_file("data/token.json", SCOPES)
    print("I will try to authorize the following Google Cloud APIs:", end="\n")

  if not credentials or not credentials.valid:
    if credentials and credentials.expired and credentials.refresh_token:
      print("I will refresh credentials now...", end="\n")
      credentials.refresh(Request())
    else:
      print("I will need your help!", end="\n\n")
      flow = InstalledAppFlow.from_client_secrets_file("data/secret.json", SCOPES)
      credentials = flow.run_local_server(port=0)
    with open("data/token.json", "w") as token:
      token.write(credentials.to_json())
  else:
    print("Your credentials are still valid.", end="\n")

  print("That's all!", end="\n")
