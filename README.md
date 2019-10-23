# Google Calendar Birthday Reminder Script

This Python script creates reminders for every birthday event in your Google Calendar.

[![Build Status](https://travis-ci.org/jannisko/gc_bd_reminder.svg?branch=master)](https://travis-ci.org/jannisko/gc_bd_reminder)

## Motivation

It has always bugged me that contacts.google.com lets you set birthdates for people and automatically creates events on calendar.google.com, but there is no way to get reminded of these events.

This script is a workaround to for this problem. So I would only recommend using it if you absolutely need this feature.

This project is only possible because of [windmark's](https://github.com/windmark) unofficial [google-reminder-api-wrapper](https://github.com/windmark/google-reminder-api-wrapper)

## Prerequisites

### Modules

This script was written in Python 3.7, it requires the following modules:

* google-api-python-client
* google-auth-httplib2
* google-auth-oauthlib
* python-dotenv
* python-dateutil

### Other requirements

#### Calendar credentials

Download the Google Calendar api credentials for your account by following **step 1** on the following [site](https://developers.google.com/calendar/quickstart/python#step_1_turn_on_the) and move credentials.json into the projects root folder.

#### Reminder credentials

Follow the following steps on how to manually get the credentials required to access the reminder api.  
You will need the SID, HSID, SSID, APISID, SAPISID, authorization and key.

> **from windmark's [google-reminder-api-wrapper](https://github.com/windmark/google-reminder-api-wrapper#finding-credentials)**
>
> #### Finding Credentials
>
>Credentials can be found by doing the following
>
>1. Go to Google Calendar, https://calendar.google.com and make sure the "Reminder" calendar is marked.
>
>2. Open the "Network" tab of the Chrome Developer Tool and search for `reminders / list`
>
>3. In the "Header" sub-tab, find the required headers in the "Request Header"

Lastly, add these headers to the auth.env file in the projects root folder.

(Tip: if Chrome doesn't show you the full headers you might want to try it in a different browser.)

## Deployment

### Optional Arguments

* --delete  
   Removes all reminders created by this script.
* --days n  
   Specify how many days in advance the reminder should be set  
   default: 0
* --time hh[:mm[:ss]]  
   Specify at what time of day the reminders should be set  
   default: 07:00:00

```bash
# in the project's root directory
pip install -r requirements.txt
python . [arguments]
```

### Docker

```Bash
docker build --tag gc_bd_reminder .
docker run gc_bd_reminder [arguments]
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
