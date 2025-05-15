import json

#Before we start we select our configuration paths...
config_path = "data/config.json"
config = json.load(open(config_path)) #We load the configuration file...
t_mails_path = "data/csv/" + config["file_prefix"] + "maillist.csv"

#Loading the file...
mailist_is_healthy = True
maillist = open(t_mails_path).readlines()[1:]
errors = []

#Variables to check...
DOMAIN = "eds.edu.ar"
CALENDARS = ["Agenda (BOT)","No hay clases (BOT)","1ro (BOT)","2do (BOT)","3ro (BOT)","4to (BOT)",
          "5to (BOT)","6to (BOT)","7mo (BOT)","Coordinación (BOT)","Secretaría (BOT)","-"]
TAGS = ["#importante"]

def check_domain(address):
  if address.split("@")[1] == DOMAIN:
    return True
  else:
    return False

def check_list(in_file, true_list):
  is_healthy = True
  for i in in_file:
    if not i in true_list:
      is_healthy = False
      break
  return is_healthy

def check_number(string_n):
  is_number = True
  try:
    int(string_n)
  except:
    is_number = False
  return is_number

print("I will check the mailing list now...", end="\n")
for l in range(len(maillist)):
  data = maillist[l].split(";")
  if not check_domain(data[0]):
    errors.append((l, "mail"))
  if not check_list(data[1].split(","), CALENDARS):
    errors.append((l, "suscriptions"))
  if not check_list(data[2].split(","), CALENDARS):
    errors.append((l, "permissions"))
  if not check_number(data[3]):
    errors.append((l, "later_events"))
  if not check_list(data[4].split(","), TAGS):
    errors.append((l, "later_tags"))

if len(errors) == 0:
  print("I didn't find any errors...", end="\n")
else:
  print("I found " + str(len(errors)) + " errors...", end="\n")
  for e in errors:
    print(e)

print("That's all!", end="\n")
