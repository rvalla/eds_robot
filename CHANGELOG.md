![logo](https://gitlab.com/escueladelsol/eds_robot/-/raw/themoststable/assets/img/icon_64.png)

# eds_robot: changelog

## 2025-05-26: v0.6.5 beta

Now **update_token()** in *authorize.py* returns *credentials* to pass them
to the different clases of **eds_robot**. New **body_from_template()**
function in **HtmlFormat()** allows you to send an email from a template
replacing custom tags using *python regex module*.  

## 2025-05-17: v0.6.0 beta

Now you can send *first contact* emails to new users running *remainders_first_contact.py*.
Some improvements in *remainders.py*. Ready to start saving some usage data in *data/csv/stats.csv*.  

## 2025-05-05: v0.5.0 beta

The *personalized remainders* are ready. **GCalendar()** was improved and now can delete
events too. **HtmlFormat()** take care of mail body formatting (css was tested on 
email clients as well as browsers). See */examples* folder to run your tests.  

## 2025-04-17: v0.1.0 alpha

For now **eds_robot** can send emails and create events in calendars. Running **authorize.py**
you update your credentials. Then you can use **Gmail()** and **GCalendar** classes. Some useful
functions are in **Util()**.  
You can run the *tests* at */examples* if you have valid credentials and a **Google Cloud Project**.   

Feel free to contact us by [mail](mailto:rvalla@eds.edu.ar).
