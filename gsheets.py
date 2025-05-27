from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class GSpreadsheets():
  "The class to work with Google Cloud spreadsheets API"

  #We need our credentials and the service...
  def __init__(self, credentials_path, credentials):
    self.service = service = build("sheets", "v4", credentials=credentials)

  #To get a range in the spreadsheet...
  def get_range(self, spreadsheet_id, the_range):
    data = (self.service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=the_range).execute())
    return data.get("values", [])

  #To get many ranges in the spreadsheet...
  def get_ranges(self, spreadsheet_id, the_ranges):
    data = (self.service.spreadsheets().values().batchGet(spreadsheetId=spreadsheet_id, ranges=the_ranges).execute())
    return data.get("valueRanges", [])

  #To write data to a range...
  def write_range(self, spreadsheet_id, the_range, the_data):
    body = {"values": [the_data]}
    result = (self.service.spreadsheets().values().update(spreadsheetId=spreadsheet_id, range=the_range,
              valueInputOption="RAW", body=body).execute())
    print("The spreadsheet was updated!", end="\n")

  #To write data on many ranges...
  def write_ranges(self, spreadsheet_id, the_ranges, the_datas):
    data = []
    for i in range(len(the_ranges)):
      data.append({"range": the_ranges[i], "values": [the_datas[i]]})
    body = {"valueInputOption": "RAW", "data": data}
    result = (self.service.spreadsheets().values().batchUpdate(spreadsheetId=spreadsheet_id, body=body).execute())

  #About me...
  def __str__(self):
    return "I am the class to work with Google Cloud spreadsheets API."
