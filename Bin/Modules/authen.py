from __future__ import print_function
from apiclient.discovery import build
from apiclient import errors
from httplib2 import Http
from oauth2client import file, client, tools
import os

import base64
from email.mime.text import MIMEText
from email.mime.audio import MIMEAudio
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
import mimetypes

class authen:
    def __init__(self, SCOPES):
        self.SCOPES = SCOPES

    def set_api(self):
        store = file.Storage("Bin/Modules/api/credentials.json")
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets("Bin/Modules/api/client_secret.json", self.SCOPES)
            creds = tools.run_flow(flow, store)
        return build('gmail', 'v1', http=creds.authorize(Http()))

    def create_msg(self, sender, to, subject, msg_txt):
        msg = MIMEText(msg_txt)
        msg['to'] = to
        msg['from'] = sender
        msg['subject'] = subject
        return {'raw': base64.urlsafe_b64encode(msg.as_bytes()).decode()}

    def create_draft(self, service, user_id, msg_body):
        try:
            msg = {'message': msg_body}
            draft = service.users().drafts().create(userId=user_id, body=msg).execute()
            print('Draft id: %s\nDraft message: %s' % (draft['id'], draft['message']))
            return draft
        except errors.HttpError as error:
            print('An error occurred: %s' % error)
            return None

    def send_msg(self, service, user_id, msg):
        try:
            msg = (service.users().messages().send(userId=user_id, body=msg).execute())
            print("Message Id: %s" % msg['id'])
            return msg
        except errors.HttpError as error:
            print("An error occurred: %s" % error)
            return None

    def find_msg(self, service, user_id, query):
        try:
            response = service.users().messages().list(userId=user_id, q=query).execute()
            messages = []
            if 'messages' in response:
                messages.extend(response['messages'])

            while 'nextPageToken' in response:
                page_token = response['nextPageToken']
                response = service.users().messages().list(userId=user_id, q=query, pageToken=page_token).execute()
                messages.extend(response['messages'])
            return messages
        except errors.HttpError as error:
            print('An error occurred: %s' % error)
            return None

    def get_msg(self, service, user_id, msg_id):
        try:
            message = service.users().messages().get(userId=user_id, id=msg_id).execute()
            return message
        except errors.HttpError as error:
            print('An error occurred: %s' % error)
            return None

    def msg_to_thrash(self, service, user_id, msg_id):
        try:
            service.users().messages().trash(userId=user_id, id=msg_id).execute()
            return True
        except errors.HttpError as error:
            print('An error occurred: %s' % error)
            return False

    def show_labels(self, service):
        results = service.users().labels().list(userId='me').execute()
        labels = results.get('labels', [])
        if not labels:
            print('No labels found.')
        else:
            print('Labels:')
            for label in labels:
                print(label['name'])
