import os, dotenv

# if reminder api credentials haven't been set before starting the script,
# try to get them from .env file
if(os.environ.get('SID') == None):
    file_path = os.path.dirname(os.path.abspath(__file__))
    env_path = os.path.join(file_path, '../auth.env')
    dotenv.load_dotenv(dotenv_path=env_path)

from src import gc_bd_reminder

def test_test():
    pass