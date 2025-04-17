import os.path
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

def update_token(config_path, scopes):
  
  #List of apis to authorize...
  SCOPES = scopes

  print("I will try to authorize the following Google Cloud APIs:", end="\n")
  for s in SCOPES:
    print("- " + s, end="\n")

  credentials = None
  if os.path.exists(config_path + "token.json"):
    credentials = Credentials.from_authorized_user_file(config_path + "token.json", SCOPES)

  if not credentials or not credentials.valid:
    if credentials and credentials.expired and credentials.refresh_token:
      print("I will refresh credentials now...", end="\n")
      credentials.refresh(Request())
    else:
      print("I will need your help!", end="\n\n")
      flow = InstalledAppFlow.from_client_secrets_file(config_path + "secret.json", SCOPES)
      credentials = flow.run_local_server(port=0)
    with open(config_path + "token.json", "w") as token:
      token.write(credentials.to_json())
  else:
    print("Your credentials are still valid.", end="\n")

  print("That's all!", end="\n")
