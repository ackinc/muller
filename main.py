import os
import logging

from base64 import urlsafe_b64decode
from dotenv import load_dotenv
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from tempfile import gettempdir, NamedTemporaryFile

from utils.gmail import get_relevant_message_details
from utils.misc import get_filename, extract_pdf_first_page, \
    remove_pdf_password

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
#   just find the first message in the list with a pdf attachment
for cdt in cc_stmt_message_candidates:
    # get the full details of the candidate msg
    msg_full = gmail_service.users().messages().get(
        userId='me', id=cdt['id']).execute()

    # extract just the details we care about
    msg_details = get_relevant_message_details(msg_full)

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


# extract first page of statement (usually the page that has the address)
tmpfilename = get_filename(tmpfile.name)

nopass_filepath = os.path.join(gettempdir(), f"{tmpfilename}-nopass.pdf")
remove_pdf_password(tmpfile.name, nopass_filepath)

first_page_path = os.path.join(gettempdir(), f"{tmpfilename}-nopass-pg-1.pdf")
extract_pdf_first_page(nopass_filepath, first_page_path)

# TODO: upload to gdrive

# remove intermediate files
os.remove(nopass_filepath)
os.remove(first_page_path)


print('Done')
