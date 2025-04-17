import sys
sys.path.append("..")

import json
import datetime as dt
import authorize as auth
from gcalendar import GCalendar

config = json.load(open("../data/config.json")) #We load the configuration file...
auth.update_token("../data/", [config["mail_scope"], config["calendar_scope"]]) #First we create or update our token...

#We need an instance of Mail():
calendar = GCalendar(config["ex_token"], [config["mail_scope"], config["calendar_scope"]])

#We are ready to create some events:
calendar.create_event("primary", "Test", "Testing EDS Robot", dt.datetime(2025,4,5,12,30), dt.datetime(2025,4,5,13,30), False)
calendar.create_event("primary", "Test", "Testing EDS Robot", dt.date(2025,4,7), dt.date(2025,4,8), True)
calendar.create_events("../data/css/test_calendarevents.csv")
