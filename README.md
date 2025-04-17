![logo](https://gitlab.com/escueladelsol/eds_robot/-/raw/themoststable/assets/img/icon_64.png)

# eds_robot

In Buenos Aires, At [Escuela Del Sol](https://escueladelsol.com.ar), we are working in some little
tools to make our lives easier. The people at the school use
[Google Workspace](https://workspace.google.com/) to send emails, produce colaborative documents
and more. We are currently working on:

### Calendar to email

The idea is simply to automaticaly send personalized emails with a summary of future events
in calendar. Actually is a work in progress...  

### Events to calendar

Simply the functions needed to create bulk events in calendar from a *.csv* file. You can see
*examples/test_calendar.py*.  

## To run any code

You will need a *Google Cloud* project, a *Google account* and your *credentials* to use these tools.
Then you are ready to edit *data/config.json* file.

```
{
  "name":"eds_robot",
  "testing": true,
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
  "ex_token": "../data/token.json"
}
```

Feel free to contact us by [mail](mailto:rvalla@eds.edu.ar).
