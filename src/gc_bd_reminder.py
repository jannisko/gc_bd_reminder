from os import environ, path
from pathlib import Path
import re
from datetime import datetime, timedelta, time
import logging

import pickle

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from google_reminder_api_wrapper.reminder_api import ReminderApi

class gc_bd_reminder:
    
    def __init__(self, days_in_advance, time_of_day):

        # string at the start of each reminders clientAssignedId
        # this is used to identify reminders created by this app
        self.APP_NAME = 'gcbdreminder'
        # initialize the official google calendar API
        # We only need read access to the calendar api because we create the reminders through windmark's reminder-api-wrapper
        self.SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

        # Calendar ID for birthdays created by Google Contacts
        self.CALENDAR_ID = 'addressbook#contacts@group.v.calendar.google.com'

        self.days_in_advance = days_in_advance
        self.time_of_day = time_of_day

        self.creds = self.create_creds()

        self.api = ReminderApi()

    def update_reminders(self):

        events = self.get_all_events()

        logging.debug(f'Received {str(len(events))} events')

        reminders = self.api.list()

        logging.debug(f'Received {str(len(reminders["task"]))} reminders')

        added_events = get_added(events, reminders)
        logging.info(f'Found {len(added_events)} new events')

        delete_reminders = get_deleted(events, reminders)
        logging.info(f'Found {len(delete_reminders)} reminders to be deleted')
        
        
        for event in added_events:
            create_reminder(event)

        for reminder in delete_reminders:
            delete_reminder(reminder)

        
    def create_creds(self):
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
                    'credentials.json', self.SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        return creds

    def get_all_events(self):
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

    def delete_all_reminders(self):
        reminders = self.api.list()
        for task in reminders['task']:
            if(task['taskId']['clientAssignedId'].startswith(APP_NAME)):
                logging.info(f'Deleting: {task["title"]}')
                self.api.delete(task['taskId']['serverAssignedId'])

    def create_valid_id(self, event):

        # From https://developers.google.com/calendar/v3/reference/events
        # characters allowed in the ID are those used in base32hex encoding, i.e. lowercase letters a-v and digits 0-9, see section 3.1.2 in RFC2938
        # the length of the ID must be between 5 and 1024 characters

        regex = re.compile("((?![a-v0-9]).)*")

        return regex.sub('', \
            self.APP_NAME + \
            event['summary'].lower() + \
            str(datetime.strptime(event['start']['date'], '%Y-%m-%d')))
        
    def create_reminder(self, event):
        start_date = datetime.strptime(event['start']['date'], '%Y-%m-%d')
        start_date += timedelta(hours=self.time_of_day.hour, minutes=self.time_of_day.minute)
        start_date -= timedelta(days=self.days_in_advance)
        logging.info(f'Creating Event: {event["summary"]}, Date: {str(start_date)}')
        logging.debug(f'ID: {create_valid_id(event)}')
        self.api.create(event['summary'], due_date=start_date, taskId={'clientAssignedId': create_valid_id(event)})

    def delete_reminder(self, reminder):
        logging.info(f'Deleting Reminder: {reminder["title"]}')
        self.api.delete(reminder['taskId']['serverAssignedId'])

    @staticmethod
    def get_added(events, reminders):
        reminder_set = set()
        added_events = list()
        for reminder in reminders['task']:
            reminder_set.add(reminder['title'])
        for event in events:
            if(event['summary'] not in reminder_set):
                added_events.append(event)
        return added_events

    @staticmethod
    def get_deleted(events, reminders):
        event_set = set()
        reminders_to_be_deleted = list()
        for event in events:
            event_set.add(event['summary'])
        for reminder in reminders['task']:
            if reminder['title'] not in event_set and \
                APP_NAME in reminder['taskId']['clientAssignedId']:
                reminders_to_be_deleted.append(reminder)
        return reminders_to_be_deleted
