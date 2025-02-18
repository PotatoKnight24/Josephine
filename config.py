import os
from dotenv import load_dotenv
load_dotenv()
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
OPEN_API_KEY = os.getenv('OPEN_API_KEY')

FIREBASSE_CREDENTIALS = os.getenv('')
print(OPEN_API_KEY)
