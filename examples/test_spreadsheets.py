import sys
sys.path.append("..")

import json
import random as rd
import authorize as auth
from gsheets import GSpreadsheets

config = json.load(open("../data/config.json")) #We load the configuration file...
spreadsheet_data = json.load(open("../data/test_spreadsheets.json")) #We load spreadsheet data... 
credentials = auth.update_token(config["ex_auth"], #First we get our credentials...
                [config["mail_scope"], config["calendar_scope"], config["spreadsheets_scope"]])

#We need an instance of GSpreadsheets():
sheets = GSpreadsheets(config["ex_token"], credentials)

#We will play with our testing spreadsheet...
spreadsheet_id = spreadsheet_data["test_id"]
spreadsheet_sheets = spreadsheet_data["test_sheets"].split(",")

#We can choose a random sheet and range to read it and change it...
the_sheets = rd.sample(spreadsheet_sheets, 3)
row = rd.randint(1,53)

print("I am ready to test GSpreadsheets()...", end="\n")
print("What is in the sheet " + the_sheets[0] + " in the row " + str(row) + "?", end="\n" )

#Let's get some data from the spreadsheet...
the_range = the_sheets[0] + "!B" + str(row) + ":Z" + str(row) 
data = sheets.get_range(spreadsheet_id, the_range)[0]
print("I found interesting numbers there...", end="\n")
print("I will change them!", end="\n")

new_data = []
for d in data:
  if rd.random() < 0.25:
    new_data.append(int(d)-1)
  else:
    new_data.append(int(d)+1)

#We write the modified data into the spreadsheet...
sheets.write_range(spreadsheet_id, the_range, new_data)
print("I wrote the new numbers into the sheet!", end="\n\n")

#Let's do it again but with batchGet and batchUpdate...
print("Let's repeat this using batchGet and batchUpdate...", end="\n")
the_ranges = []
row = rd.randint(1,53)
the_ranges.append(the_sheets[1] + "!B" + str(row) + ":Z" + str(row))
print("What is in the sheet " + the_sheets[1] + " in the row " + str(row) + "?", end="\n" )
row = rd.randint(1,53)
the_ranges.append(the_sheets[2] + "!B" + str(row) + ":Z" + str(row))
print("And in the sheet " + the_sheets[2] + " in the row " + str(row) + "?", end="\n" )
data = sheets.get_ranges(spreadsheet_id, the_ranges)
print("I found interesting numbers there...", end="\n")
print("I will change them!", end="\n")
new_data = []
for i in range(2):
  new_data.append([])
  for d in data[i]["values"][0]:
    if rd.random() < 0.25:
      new_data[i].append(int(d)-1)
    else:
      new_data[i].append(int(d)+1)

#We write the modified data into the spreadsheet...
sheets.write_ranges(spreadsheet_id, the_ranges, new_data)
print("I wrote the new numbers into the sheet!", end="\n\n")

print("That's all!", end="\n")
