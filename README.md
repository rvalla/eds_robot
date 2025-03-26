![logo](https://gitlab.com/escueladelsol/eds_robot/-/raw/themoststable/assets/img/icon_64.png)

# eds_robot

In Buenos Aires, At [Escuela Del Sol](https://escueladelsol.com.ar), we are working in some little
tools to make our lives easier. The people at the school use
[Google Workspace](https://workspace.google.com/) to send emails, produce colaborative documents
and more. We are currently working on:

### Calendar to email

The idea is simply to automaticaly send personalized emails with a summary of future events
in calendar. You can see *test_mail.py* to give it a try. Actually is a work in progress...  

## To run any code

You will need a *Google Cloud* project, a *Google account* and your *credentials* to use these tools.
Then you are ready to edit *data/config.json* file.

```
{
  "name":"be_creative",
  "testing": true,
  "mail": "your@email.address",
  "credentials": "data/secret.json",
  "token": "data/token.json",
  "mail_scope": "https://www.googleapis.com/auth/gmail.compose",
  "calendar_scope": "https://www.googleapis.com/auth/calendar.events",
  "drive_scope": "https://accounts.google.com/o/oauth2/auth"
}
```

Feel free to contact us by [mail](mailto:rvalla@eds.edu.ar).
