import re
import json
import authorize as auth
from util import Util
from gcalendar import GCalendar

#Before we start we select our configuration paths...
config_path = "data/config.json"
config = json.load(open(config_path)) #We load the configuration file...
t_calendars_path = "data/csv/" + config["file_prefix"] + "calendarlist.csv"
TAG_DATA = [] #calendar, total_events, events_with_tag, ratio
THE_TAG = None

print("------ CALENDAR TAG ANALYSIS -------", end="\n")
print("Let's check how many events exist with a tag...", end="\n")

#We update our token...
credentials = auth.update_token("data/", [config["mail_scope"], config["calendar_scope"], config["spreadsheets_scope"]])

#We need an instance Util(), Html(), GMail() and GCalendar():
ut = Util()
calendar = GCalendar(credentials, -3)

#We load the targeted calendars...
t_calendars = []
file = open(t_calendars_path).readlines()[1:]
for l in file:
  t_calendars.append(l.split(";")[0])
print("The current list of calendars is:", end=" ")
print(t_calendars, end="\n")
next_monday = ut.next_monday()

for c in t_calendars:
  TAG_DATA.append([c,0,0,0])
TAG_DATA.append(["All",0,0,0])

#Ready to collect all events...
print("I am ready to collect all events in targeted calendars...", end="\n")
all_events = calendar.build_events_list(t_calendars, next_monday, max_results=300)

#Ready to analyse the data...
print("\n------ WAITING FOR TAG -------", end="\n")
print("Please, tell me the tag I have to look for in event's description...", end="\n\n")
THE_TAG = input()
print("Ok. I will iterate all events and check how many of them include your tag...", end="\n\n")

#To get out calendar index...
def get_calendar_index(calendar):
  i = -1
  for r in range(len(TAG_DATA)):
    if calendar == TAG_DATA[r][0]:
      i = r
      break
  return i

#To decide is the event contains the tag...
def tag_found(event_description):
  return bool(re.search(THE_TAG, event_description))

#Let's iterate all events...
for e in all_events:
  i = get_calendar_index(e[0])
  TAG_DATA[i][1] += 1
  TAG_DATA[len(TAG_DATA)-1][1] += 1
  if tag_found(e[2]):
    TAG_DATA[i][2] += 1
    TAG_DATA[len(TAG_DATA)-1][2] += 1

#Let's save our results...
file = open("data/csv/calendars_tags.csv", "a")

def extend_string(calendar_name):
  for s in range(20-len(calendar_name)):
    calendar_name += " "
  return calendar_name

def write_line_in_file(calendar, tag, events_tag, total_events, ratio):
  file.write(ut.iso_today() + ";")
  file.write(calendar + ";")
  file.write(tag + ";")
  file.write(events_tag + ";")
  file.write(total_events + ";")
  file.write(ratio + "\n")

def print_data_row(calendar, events_tag, total_events, ratio):
  print(calendar, end="\t")
  print(events_tag, end="\t")
  print(total_events, end="\t")
  print(ratio, end="\n")

print("------ RESULTS -------", end="\n\n")
print("Calendar, Events with the tag, Total events, Ratio", end="\n")
for c in TAG_DATA:
  if c[1] > 0:
    c[3] = c[2]/c[1]
  else:
    c[3] = 0.0
  events_with_tag = str(c[2])
  total_events = str(c[1])
  ratio = "{0:.2f}".format(c[3])
  write_line_in_file(c[0], THE_TAG, events_with_tag, total_events, ratio)
  print_data_row(extend_string(c[0]), events_with_tag, total_events, ratio)

file.close()
print("\nThat's all!", end="\n")
print("-----------", end="\n")
