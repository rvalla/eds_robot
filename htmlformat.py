import re

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
    message_body = self.get_mail_header()
    message_body += self.remainders_hello()
    message_body += self.title_row("La próxima semana:")
    if len(next_week_events) > 0:
      message_body += self.events_rows(next_week_events, True)
    else:
      message_body += self.hr_row()
      message_body += self.no_events_row()
    message_body += self.hr_row()
    message_body += self.empty_row()
    if len(later_events) > 0:
      message_body += self.title_row("Más adelante:")
      message_body += self.events_rows(later_events, False)
      message_body += self.hr_row()
      message_body += self.empty_row()
    message_body += self.remainders_disclaimer()
    message_body += self.get_mail_footer()
    return message_body

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

  def no_events_row(self):
    row = "<tr>\n<td colspan=4>\n"
    row += "<p>Parece que no hay ningún evento durante la próxima semana en tus calendarios."
    row += "<br>Supongo que tendrás que trabajar igual.</p>"
    row += "</td>\n</tr>\n"
    return row
  
  def date_cell(self, date, interval, week_day, in_next_week):
    cell = "<td style=\"min-width:100px;\"><p class=\"date\">"
    if not in_next_week:
      cell += "En " + str(interval) + " días<br>"
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

  def empty_row(self):
    return "<tr><td colspan=4></td></tr>"

  def remainders_hello(self):
    return "<tr>\n<td colspan=4>\n<p>¡Hola!<br>Preparé para vos este correo personalizado " + \
        "consultando los calendarios compartidos que más te interesan.<br>¡Espero que " + \
        "tengas lindo fin de semana!</p>\n</td>\n</tr>\n"

  def remainders_disclaimer(self):
    return "<tr>\n<td colspan=4>\n<p>Yo, <b>Robot Del Sol</b>, generé este correo automáticamente " + \
        "al consultar los calendarios compartidos. La información suministrada puede contener errores, " + \
        "incluso puede ser modificada por humanos en los próximos días. Si necesitás que incluya " +\
        "eventos de otros calendarios o necesitás permiso para modificar alguno, podés " + \
        "<a href=\"mailto:robot@eds.edu.ar\">escribirme</a>.</p>\n</td>\n</tr>\n"

  def body_from_template(self, file_path, targets, data):
    message_body = self.get_mail_header()
    body = open(file_path, "r").read()
    for i in range(len(targets)):
      body = re.sub(targets[i], data[i], body)
    message_body += body 
    message_body += self.get_mail_footer()
    return message_body

  def remainders_first_contact_mail_body(self, calendars_data, calendars_suscriptions, calendars_permissions, later_count, later_tags):
    message_body = self.get_mail_header()
    message_body += self.remainders_first_contact_hello()
    message_body += self.title_row("Tu configuración:")
    message_body += self.format_calendars_suscriptions(calendars_data, calendars_suscriptions)
    if not calendars_permissions[0] == "-":
      message_body += self.format_calendars_permissions(calendars_data, calendars_permissions)
    message_body += self.format_later_events_configuration(later_count, later_tags)
    message_body += self.title_row("¿Necesitás modificar tu configuración?")
    message_body += self.configuration_change_message()
    message_body += self.hr_row()
    message_body += self.empty_row()
    message_body += self.remainders_first_contact_disclaimer()
    message_body += self.get_mail_footer()
    return message_body

  def format_calendars_suscriptions(self, calendars_data, calendars_suscriptions):
    m = "<tr>\n<td colspan=4>\n<p>Cuando prepare tus correos semanales voy a incluir eventos " + \
        "de los siguientes calendarios compartidos:\n"
    m += self.calendars_list(calendars_data, calendars_suscriptions)
    m += "</p>\n</td>\n</tr>\n"
    return m

  def format_calendars_permissions(self, calendars_data, calendars_permissions):
    m = "<tr>\n<td colspan=4>\n<p>Por el momento, tenés permiso para crear o modificar " + \
        "eventos en los siguientes calendarios compartidos:\n"
    m += self.calendars_list(calendars_data, calendars_permissions)
    m += "</p>\n</td>\n</tr>\n"
    return m

  def format_later_events_configuration(self, later_count, later_tags):
    m = "<tr>\n<td colspan=4>\n<p>Los correos semanales personalizados tienen dos secciones. " + \
        "En la sección <i>próxima semana</i> vas a ver todos los eventos que existan durante esa " + \
        "semana. En la sección <i>más adelante</i> voy a incluir hasta " \
        + self.html_tagging("b", str(later_count)) + " eventos destacados que en su descripción contengan "
    m += self.later_tags_string(later_tags) + ".</p>"
    m += "<p>No hace falta que hagas nada para recibir mis correos, pero si querés ver los calendarios " + \
          "compartidos en " + self.html_link("https://calendar.google.com", "Calendar") + " hace falta que " + \
          "te suscribas. Podés hacerlo haciendo click en los links de la lista de acá arriba (se va a abrir " + \
          "Calendar y va aparecer una ventana con el botón " + \
          self.html_tagging("i", "agregar") + ".</p>\n</td>\n</tr>\n"
    return m

  def configuration_change_message(self):
    m = "<tr>\n<td colspan=4>\n<p>Los correos semanales personalizados que te voy a enviar pueden configurarse. " + \
          "Podés <a href=\"mailto:robot@eds.edu.ar\">escribirme</a> solicitando los cambios que necesites. " + \
          "Los parámetros de configuración disponibles son:"
    parameters = ["Tu selección de calendarios compartidos", "El número máximo de eventos en la sección <i>más adelante</i>",
                  "Las etiquetas que transforman un evento en <i>evento destacado</i>"]
    m += self.text_list(parameters)
    m += "Todos los detalles están en el documento "
    m += self.html_link("https://docs.google.com/document/d/1NXDwTJyq6s8l0wBX-MmhDpOHlZPGwLLEc2Vidp4xy8w", "2025_robot_calendarioscompartidos")
    m += ".</p><p>Espero que mis correos hagan la vida de los humanos de la escuela un poco más fácil.</p>"
    return m
  
  def later_tags_string(self, later_tags):
    m = ""
    if len(later_tags) > 1:
      m += "las etiquetas "
      for t in range(len(later_tags)):
        m += self.html_tagging("b", self.html_tagging("i", later_tags[t]))
        if t < len(later_tags) - 2:
          m += ", "
        elif t == len(later_tags) - 2:
          m += " y "
    else:
      m += "la etiqueta " + self.html_tagging("b", self.html_tagging("i", later_tags[0]))
    return m

  def enumeration_string(self, word_list):
    m = ""
    if len(word_list) > 1:
      for t in range(len(word_list)):
        m += self.html_tagging("b", word_list[t])
        if t < len(word_list) - 2:
          m += ", "
        elif t == len(word_list) - 2:
          m += " y "
    else:
      m = self.html_tagging("b", word_list[0])
    return m

  def calendars_list(self, calendars_data, calendars):
    titles = []
    hrefs = []
    for c in calendars:
      titles.append(c)
      hrefs.append(calendars_data[c]["url"])
    return self.link_list(hrefs, titles)

  def remainders_first_contact_hello(self):
    return "<tr>\n<td colspan=4>\n<p>¡Hola! Soy <b>Robot Del Sol</b>,<br>A partir de hoy, " + \
        "una vez a la semana, voy a enviarte un correo personalizado incluyendo los eventos " + \
        "de los calendarios compartidos que más te interesan. Te acerco todo lo que necesitás " + \
        "saber.</p>\n</td>\n</tr>\n"

  def remainders_first_contact_disclaimer(self):
    return "<tr>\n<td colspan=4>\n<p>Yo, <b>Robot Del Sol</b>, generé este correo automáticamente  " + \
        "para comunicarme con vos por primera vez. Si ya habías recibido alguno de mis correos " + \
        "te pido disculpas. Recordá que podés <a href=\"mailto:robot@eds.edu.ar\">escribirme</a> para " + \
        "sacarte cualquier duda que tengas.</p>\n</td>\n</tr>\n"

  def get_mail_header(self):
    header = "<html lang=\"es\">\n<head>\n"
    header += self.mail_head
    header += "<style>\n"
    header += self.mail_style
    header += "</style>\n</head>\n<body>\n<table>\n"
    header += self.mail_header
    return header

  def get_mail_footer(self):
    m = self.mail_footer
    m += "</table>\n</body>\n</html>"
    return m

  def html_link(self, href, text):
    return "<a href=\"" + href + "\">" + text + "</a>"

  def html_tagging(self, tag, text):
    return "<" + tag + ">" + text + "</" + tag + ">"

  def text_list(self, texts):
    m = "<ul>\n"
    for t in texts:
      m += "<li>" + t + "</li>\n"
    m += "</ul>\n"
    return m

  def link_list(self, hrefs, titles):
    m = "<ul>\n"
    for f, t in zip(hrefs, titles):
      m += "<li>" + self.html_link(f, t) + "</li>\n"
    m += "</ul>\n"
    return m
  
  #About me...
  def __str__(self):
    return "I am the class to format html text."
