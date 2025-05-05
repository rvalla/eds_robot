![logo](https://gitlab.com/escueladelsol/eds_robot/-/raw/themoststable/assets/img/icon_64.png)

# eds_robot

In Buenos Aires, At [Escuela Del Sol](https://escueladelsol.com.ar), we are working in some little
tools to make our lives easier. The people at the school use
[Google Workspace](https://workspace.google.com/) to send emails, produce colaborative documents
and more. We are currently working on:

### Calendar to email

Using **GMail()**, **GCalendar()** and **HtmlFormat()** the code in *remainders.py* can send
personalized emails with events in the coming weeks. To configure the remainders you need two
*.csv* files store at */data/csv*.  

```
calendar_name;n
robot@eds.edu.ar;1
Test;2
...
```
```
mail;calendars;n
robot@eds.edu.ar;calendar 1,calendar 2;1
another@us.er;calendar 1,calendar 5;2
another@us.er;calendar 1,calendar 3;3
...
```

### Events in calendar

The **GCalendar()** class can get, create or delete events. You can check
*examples/test_calendar.py*. Some other functions are related to *calendar to email*
remainders.  

## To run any code

You will need a *Google Cloud* project, a *Google account* and your *credentials* to use these tools.
Then you are ready to edit *data/config.json* file.

```
{
  "name":"eds_robot",
  "testing": true,
  "file_prefix": "test_",
  "mail": "your@email.address",
  "credentials": "data/secret.json",
  "token": "data/token.json",
  "calendar_scope": "https://www.googleapis.com/auth/calendar",
  "chat_scope": "https://www.googleapis.com/auth/chat.messages",
  "classroom_scope": "https://www.googleapis.com/auth/classroom.courses",
  "docs_scope": "https://www.googleapis.com/auth/documents",
  "drive_scope": "https://www.googleapis.com/auth/drive",
  "forms_scope": "https://www.googleapis.com/auth/forms.body",
  "mail_scope": "https://www.googleapis.com/auth/gmail.compose",  
  "spreadsheets_scope": "https://www.googleapis.com/auth/spreadsheets",
  "ex_auth": "../data/",
  "ex_credentials": "../data/secret.json",
  "ex_html": "../data/",
  "ex_token": "../data/token.json"
}
```

Feel free to contact us by [mail](mailto:rvalla@eds.edu.ar).
