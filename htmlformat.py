class HtmlFormat():
  "The class to format text into html"

  def __init__(self, path_prefix, file_prefix):
    self.date_format = "%d/%m/%Y"
    self.short_date_format = "%d/%m"
    self.time_format = "%H:%Mhs"
    self.week_days = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    self.mail_head = open(path_prefix + "html/" + file_prefix + "head.html", "r").read()
    self.mail_style = open(path_prefix + "html/" + file_prefix + "style.css", "r").read()
    self.mail_header = open(path_prefix + "html/" + file_prefix + "header.html", "r").read()
    self.mail_footer = open(path_prefix + "html/" + file_prefix + "footer.html", "r").read()

  def remainders_mail_body(self, next_week_events, later_events):
    message_body = "<html lang=\"es\">\n<head>\n"
    message_body += self.mail_head
    message_body += "<style>\n"
    message_body += self.mail_style
    message_body += "</style>\n</head>\n<body>\n<table>\n"
    message_body += self.mail_header
    message_body += self.title_row("La próxima semana:")
    message_body += self.events_rows(next_week_events, True)
    message_body += self.hr_row()
    message_body += self.empty_row()
    message_body += self.title_row("Más adelante:")
    message_body += self.events_rows(later_events, False)
    message_body += self.empty_row()
    message_body += self.mail_footer
    message_body += "</table>\n</body>\n</html>"
    return message_body

  def empty_row(self):
    return "<tr><td colspan=4></td></tr>"

  def events_rows(self, events, in_next_week):
    rows = ""
    for e in events:
      rows += self.hr_row()
      rows += self.event_row(e, in_next_week)
    return rows
      
  def event_row(self, event, in_next_week):
    row = "<tr>\n"
    row += self.date_cell(event[3], event[5], event[6], in_next_week)
    row += self.summary_cell(event[0], event[1], event[2], event[7], event[8])
    row += "</tr>\n"
    return row
  
  def date_cell(self, date, interval, week_day, in_next_week):
    cell = "<td><p class=\"date\">"
    if not in_next_week:
      cell += "en " + str(interval) + " días<br>"
      cell += date.strftime(self.date_format) + "<br>"
    else:
      cell += self.week_days[week_day] + " "
      cell += date.strftime(self.short_date_format) + "<br>"
    if not date.hour == 0:
      cell += date.strftime(self.time_format)
    cell += "</p></td>\n"
    return cell

  def summary_cell(self, calendar, summary, description, event_url, meet_call):
    cell = "<td colspan=3>"
    cell += self.html_tagging("h2", summary)
    cell += description
    if not meet_call == None:
      cell += "<br>" + self.html_link(meet_call, "Videollamada de Google Meet")
    cell += "<br>" + self.html_link(event_url, "Ver evento en " + calendar)
    cell += "</td>\n"
    return cell

  def title_row(self, text):
    return "<tr><td colspan=4><h1>" + text + "</h1></td></tr>\n"

  def hr_row(self):
    return "<tr><td colspan=4><hr></td></tr>\n"

  def html_link(self, href, text):
    return "<a href='" + href + "'>" + text + "</a>"

  def html_tagging(self, tag, text):
    return "<" + tag + ">" + text + "</" + tag + ">" 
  
  #About me...
  def __str__(self):
    return "I am the class to format html text."
