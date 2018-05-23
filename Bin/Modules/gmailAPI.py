from __future__ import print_function
from apiclient.discovery import build
from apiclient import errors
from httplib2 import Http
from oauth2client import file
import os


def set_api():
    try:
        cred_path = os.getcwd() + "\\Bin\\Modules\\api\\credentials.json"
        if not os.path.isfile(cred_path):
            raise FileNotFoundError("Can't find " + cred_path)
        store = file.Storage(cred_path)
        creds = store.get()
        return build('gmail', 'v1', http=creds.authorize(Http()))
    except Exception as err:
        print("[!]Error: " + str(err))
        return None


class gmailAPI:
    def __init__(self, mail):
        self.MAIL = mail
        self.SERVICE = set_api()
        if self.SERVICE is None:
            print("[!]Please, run 'configure.py' again")
            raise SystemExit(1)

    def find_msg(self, query=''):
        try:
            response = self.SERVICE.users().messages().list(userId=self.MAIL, q=query).execute()
            messages = []
            if 'messages' in response:
                messages.extend(response['messages'])

            while 'nextPageToken' in response:
                page_token = response['nextPageToken']
                response = self.SERVICE.users().messages().list(userId=self.MAIL, q=query, pageToken=page_token).execute()
                messages.extend(response['messages'])
            return messages
        except errors.HttpError as error:
            print('An error occurred: %s' % error)
            return None

    def get_msg(self, msg_id):
        try:
            message = self.SERVICE.users().messages().get(userId=self.MAIL, id=msg_id).execute()
            return message
        except errors.HttpError as error:
            print('An error occurred: %s' % error)
            return None

    def msg_to_thrash(self, msg_id):
        try:
            self.SERVICE.users().messages().trash(userId=self.MAIL, id=msg_id).execute()
            return True
        except errors.HttpError as error:
            print('An error occurred: %s' % error)
            return False
