import os, dotenv

# if reminder api credentials haven't been set before starting the script,
# try to get them from .env file
if(os.environ.get('SID') == None):
    file_path = os.path.dirname(os.path.abspath(__file__))
    env_path = os.path.join(file_path, '../auth.env')
    dotenv.load_dotenv(dotenv_path=env_path)

from google_reminder_api_wrapper.reminder_api import ReminderApi

def test_list():
    api = ReminderApi()
    reminders = api.list()
    assert type(reminders) == dict

def test_create_get_delete():
    client_assigned_id = 'test_reminder_id'
    api = ReminderApi()
    api.create('test_reminder', taskId={'clientAssignedId': client_assigned_id})
    reminder = api.get('', taskId={'clientAssignedId': client_assigned_id})
    assert reminder['task'][0]['taskId']['clientAssignedId'] == client_assigned_id
    api.delete('', taskId={'clientAssignedId': client_assigned_id})