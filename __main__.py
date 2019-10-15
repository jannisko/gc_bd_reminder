import argparse

from datetime import time

import logging
import os
from dotenv import load_dotenv

# if reminder api credentials haven't been set before starting the script,
# try to get them from .env file
if(os.environ.get('SID') == None):
    file_path = os.path.dirname(os.path.abspath(__file__))
    env_path = os.path.join(file_path, '../auth.env')
    load_dotenv(dotenv_path=env_path)

# the api wrapper has to be imported after setting the environment variables
# because the env variables get read at import time

from src.gc_bd_reminder import gc_bd_reminder


logging.basicConfig(level=logging.INFO, format=' %(asctime)s - %(levelname)s - %(message)s')


def main():

    parser = argparse.ArgumentParser(description='Create reminders for birthday events in Google Calendar')
    parser.add_argument('--delete', dest='delete_all', action='store_true',
                        help='Delete all reminders created by this script')
    parser.add_argument('--days', dest='days_in_advance', type=int,
                        action='store', default=0,
                        help='Specify how many days before the birthday the reminder should be set (default=0)')
    parser.add_argument('--time', dest='time_of_day', type=time.fromisoformat,
                        action='store', default='07:00:00',
                        help='Specify at what time of day the reminder should be set (format=hh[:mm[:ss]], default=07:00:00)')

    args = parser.parse_args()
    
    logging.info(args)

    app = gc_bd_reminder(args.days_in_advance, args.time_of_day)

    if(args.delete_all):
        app.delete_all_reminders()
    else:
        app.update_reminders()


    

if __name__ == "__main__":
    main()