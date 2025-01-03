import os

from dotenv import load_dotenv

load_dotenv() 

API_KEY_NETANGELS = os.getenv('API_KEY_NETANGELS')
SSH_KEY_PUBLIC = os.getenv('SSH_KEY_PUBLIC')
SSH_KEY_PUBLIC_ID = int(os.getenv('SSH_KEY_PUBLIC_ID'))

MASTER_COUNT = int(os.getenv('MASTER_COUNT', 3))
CLIENT_COUNT = int(os.getenv('CLIENT_COUNT', 2))