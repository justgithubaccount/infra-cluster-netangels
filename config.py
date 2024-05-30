import os

from dotenv import load_dotenv

load_dotenv() 

API_KEY = os.getenv('API_KEY')
SSH_KEY_VALUE = os.getenv('SSH_KEY_VALUE')
SSH_KEY_ID = int(os.getenv('SSH_KEY_ID'))