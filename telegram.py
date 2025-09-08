import requests
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
MESSAGE = 'Hello, this is a test message from my bot!'

url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'

def update_message(message):    
    params = {
        'chat_id': CHAT_ID,
        'text': message,
    }

    response = requests.post(url, params=params)
    if response.status_code == 200:
        print('Message sent successfully!')
    else:
        print('Failed to send message. Error:')

def notifier(message: str, user_id: int):
    params = {
        'chat_id': user_id,
        'text': message
    }

    response = requests.post(url, params=params)
    if response.status_code == 200:
        print('Message sent successfully!')
    else:
        print('Failed to send message. Error:')

if __name__ == "__main__":
    update_message(message= "test")