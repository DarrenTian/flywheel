import base64
import json
import pickle
import os.path
import datetime
import pytz

from apiclient import errors
from email.mime.text import MIMEText
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request # pylint: disable=no-name-in-module,import-error

# TODO: offline access, otherwise token will expire
SCOPES = ['https://www.googleapis.com/auth/gmail.compose']

TOKEN_PATH = './app/service/token.pickle'
CREDENTIAL_PATH = './app/service/credentials.json'

RECIPIENT = ','.join(['darrentianyy@gmail.com'])

class GoogleService:
  """docstring for ClassName"""
  def __init__(self):
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(TOKEN_PATH):
        with open(TOKEN_PATH, 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIAL_PATH, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(TOKEN_PATH, 'wb') as token:
            pickle.dump(creds, token)
    self.creds = creds

  def get_mail_service(self):
    service = build('gmail', 'v1', credentials=self.creds)
    return service

  def send_mail(self, content):
    try:
      body = MIMEText(content)
      body['to'] = RECIPIENT
      body['subject'] = '['+datetime.datetime.now(pytz.timezone('US/Pacific')).strftime("%m/%d/%Y")+'] Flywheel Summary'
      message = (self.get_mail_service().users().messages().send(userId='me', body={'raw': base64.urlsafe_b64encode(body.as_bytes()).decode()}) # pylint: disable=no-member
                 .execute())
      print('Message Id: %s' % message['id'])
      return message
    except errors.HttpError as error:
      print('An error occurred: %s' % error)
