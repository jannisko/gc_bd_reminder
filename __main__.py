from os import environ, path
from dotenv import load_dotenv
from pathlib import Path

from datetime import datetime, timedelta
import pickle
import logging
import re

from pprint import pprint

logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

env_path = Path('.') / 'auth.env'
load_dotenv(dotenv_path=env_path)

# the api wrapper has to be imported after setting the environment variables
from google_reminder_api_wrapper import ReminderApi

# string at the start of each reminders clientAssignedId
# this is used to identify reminders created by this app
APP_NAME = 'gcbdreminder'

def main():
    # initialize the official google calendar API
    # We only need read access to the calendar api because we create the reminders through windmark's reminder-api-wrapper
    SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

    # Calendar ID for birthdays created by Google Contacts
    CALENDAR_ID = 'addressbook#contacts@group.v.calendar.google.com'

    

    creds = create_creds(SCOPES)

    events = get_all_events(creds, CALENDAR_ID)

    logging.info('Received ' + str(len(events)) + ' events')


    ## TODO: GET DIFF

    api = ReminderApi()
    reminders = api.list()

    added_events = get_added(events, reminders)
    logging.info(f'Found {len(added_events)} new events')
    #deleted = get_deleted(events, reminders)
    
    for event in events:
        pass
        #create_reminder(event)

    if not events:
        logging.info('No upcoming birthday events found.')
    else:
        # for event in events:
        #     start = event['start'].get('dateTime', event['start'].get('date'))
        #     print(start, event['summary'])
        pass

def create_creds(SCOPES):
    """creates credentials for using reading from the google calendar API

    taken from https://developers.google.com/calendar/quickstart/python
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return creds

def get_all_events(creds, CALENDAR_ID):
    """get all future birthday events (max. 250)
    """
    service = build('calendar', 'v3', credentials=creds)
    now = datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    logging.debug('Getting all upcoming birthday events')
    events_result = service.events().list(calendarId=CALENDAR_ID, timeMin=now,
                                        singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])
    return events

def delete_all_reminders():
    api = ReminderApi()
    reminders = api.list()
    for task in reminders['task']:
        if(task['taskId']['clientAssignedId'].startswith(APP_NAME)):
            logging.info(f'Deleting: {task["title"]}')
            api.delete(task['taskId']['serverAssignedId'])

def create_valid_id(event):

    # From https://developers.google.com/calendar/v3/reference/events
    # characters allowed in the ID are those used in base32hex encoding, i.e. lowercase letters a-v and digits 0-9, see section 3.1.2 in RFC2938
    # the length of the ID must be between 5 and 1024 characters

    regex = re.compile("((?![a-v0-9]).)*")

    return regex.sub('', \
        APP_NAME + \
        event['summary'].lower() + \
        str(datetime.strptime(event['start']['date'], '%Y-%m-%d')))
    
def create_reminder(event):
    api = ReminderApi()
    start_date = datetime.strptime(event['start']['date'], '%Y-%m-%d')
    start_date += timedelta(hours=8)
    logging.info(f'Creating Event: {event["summary"]}, Date:  + {str(start_date)}')
    logging.debug(f'ID: {create_valid_id(event)}')
    api.create(event['summary'], due_date=start_date, taskId={'clientAssignedId': create_valid_id(event)})

def get_added(events, reminders):
    reminder_set = set()
    added_events = list()
    for reminder in reminders['task']:
        reminder_set.add(reminder['title'])
    for event in events:
        if(event['summary'] not in reminder_set):
            added_events.append(event)
    return added_events

def get_deleted():
    pass


if __name__ == "__main__":
    
    #delete_all_reminders()
    main()