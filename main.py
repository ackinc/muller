import os
import logging
import subprocess

from base64 import urlsafe_b64decode
from dotenv import load_dotenv
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from tempfile import gettempdir, NamedTemporaryFile

from utils.gmail import get_headers, get_attachment_details
from utils.tempfile import get_tempfile_name

load_dotenv()
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

SCOPES = [
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/gmail.readonly'
]
credentials = Credentials(
    '',
    refresh_token=os.environ['REFRESH_TOKEN'],
    token_uri='https://oauth2.googleapis.com/token',
    client_id=os.environ['CLIENT_ID'],
    client_secret=os.environ['CLIENT_SECRET'],
    scopes=SCOPES
)

gmail_service = build('gmail', 'v1', credentials=credentials)

cc_stmt_message_candidates = gmail_service.users().messages().list(
    userId='me',
    q=os.environ['EMAILS_SEARCH_QUERY']
).execute()['messages']

cc_stmt_message = None

# messages are returned latest-first by google, so we
# just find the first message in the list with a pdf attachment
for cdt in cc_stmt_message_candidates:
    # get the full details of the candidate msg
    msg_full = gmail_service.users().messages().get(
        userId='me', id=cdt['id']).execute()

    # extract just the details we care about
    msg_details = {
        'id': msg_full['id'],
        **get_headers(msg_full, ['Date', 'Subject', 'Content-Type']),
        **{
            'attachment_details': [
                # we only care about pdf attachments
                x for x in get_attachment_details(msg_full)
                if x['filename'].lower().endswith('.pdf')
            ]
        }
    }

    if len(msg_details['attachment_details']) > 0:
        cc_stmt_message = msg_details
        break


if cc_stmt_message is None:
    print("No credit card statement emails found in your gmail. Exiting.")
    exit(0)


# assume the first pdf attachment is the statement
# this is not necessarily the best way; ideally there'd be something
#   in the filename to help us pick the right attachment
#   but in the absence of data to figure out a good heuristic,
#   I'm going with this
cc_stmt_id = cc_stmt_message['attachment_details'][0]['id']
cc_stmt_b64url_encoded = gmail_service.users().messages().attachments().get(
    userId='me', messageId=cc_stmt_message['id'], id=cc_stmt_id
).execute()['data']
cc_stmt_binary = urlsafe_b64decode(cc_stmt_b64url_encoded)

tmpfile = NamedTemporaryFile()
tmpfile.write(cc_stmt_binary)

nopassfilename = os.path.join(
    gettempdir(),
    f"{get_tempfile_name(tmpfile)}-nopass.pdf"
)
subprocess.run([
    'pdftops',
    '-upw',
    os.environ['CREDIT_CARD_STATEMENT_PDF_PASSWORD'],
    tmpfile.name,
    nopassfilename
])

# TODO:
# - use ghostscript to repair pdf if necessary
# - use pdfseparate to extract the first page
# - upload to gdrive

print('Done')
