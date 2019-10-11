import argparse

from datetime import time

import logging

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
    print(args  )

    app = gc_bd_reminder(args.days_in_advance, args.time_of_day)

    if(args.delete_all):
        app.delete_all_reminders()
    else:
        app.update_reminders()


    

if __name__ == "__main__":
    main()