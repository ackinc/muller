import os
import logging

from dotenv import load_dotenv
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

from utils import get_headers, get_attachment_details

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
    q=os.environ['EMAILS_SEARCH_QUERY']
).execute()

# get the full details for each message
cc_stmt_messages = [
    gmail_service.users().messages().get(usedId='me', id=msg['id']).execute()
    for msg in cc_stmt_messages['messages']
]

# extract just the details we care about
cc_stmt_messages = [
    {
        id: msg['id'],
        **get_headers(msg, ['Date', 'Subject', 'Content-Type']),
        **{
            'attachment_details': [
                # we only care about pdf attachments
                x for x in get_attachment_details(msg)
                if x['filename'].lower().endswith('.pdf')
            ]
        }
    }
    for msg in cc_stmt_messages
]

# drop messages without a pdf attachment
cc_stmt_messages = [
    msg for msg in cc_stmt_messages
    if len(msg['attachment_details']) > 0
]

if len(cc_stmt_messages) == 0:
    print("No credit card statement emails found in gmail. Exiting.")
    exit(0)

# messages are returned latest-first by google
latest_cc_stmt_message = cc_stmt_messages[0]

# assume the first pdf attachment is the statement
# this is not necessarily the best way; ideally there'd be something
#   in the filename to help us pick the right attachment
#   but in the absence of data to figure out a good heuristic,
#   I'm going with this
cc_stmt_id = latest_cc_stmt_message['attachment_details'][0]['id']
cc_stmt = gmail_service.users().messages().attachments().get(
    'me', latest_cc_stmt_message['id'], cc_stmt_id).execute()['data']
