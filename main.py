import os
import logging
from re import L

from dotenv import load_dotenv
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

load_dotenv()
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

SCOPES = ['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/gmail.readonly']
credentials = Credentials(
    '',
    refresh_token=os.environ['REFRESH_TOKEN'],
    token_uri='https://oauth2.googleapis.com/token',
    client_id=os.environ['CLIENT_ID'],
    client_secret=os.environ['CLIENT_SECRET'],
    scopes=SCOPES
)

gmail_service = build('gmail', 'v1', credentials=credentials)
users_resource = gmail_service.users()
user_profile = users_resource.getProfile(userId='me').execute()
print(user_profile)

cc_stmt_messages = gmail_service.users().messages().list(
  userId='me',
  q="subject:(Credit Card Statement)"
).execute()

cc_stmt_messages = [extractDetails(message) for message in cc_stmt_messages]
