from __future__ import print_function
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools, clientsecrets
import os
import json

def main():
    scopes = 'https://mail.google.com/'
    if not os.path.exists('Log'):
        os.makedirs('Log')
    if not os.path.exists(os.getcwd() + '\\Bin\\Modules\\api'):
        os.makedirs(os.getcwd() + '\\Bin\\Modules\\api')
    if not os.path.isfile(os.getcwd() + "\\Bin\\Modules\\api\\client_secret.json"):
        print("{!]Error: Can't find " + os.getcwd() + "\\Bin\\Modules\\api\\client_secret.json")
        print("[!]Please, put 'client_secret.json' file in " + os.getcwd() + "\Bin\Modules\\api\\")
        return None
    store = file.Storage(os.getcwd() + "\\Bin\\Modules\\api\\credentials.json")
    creds = store.get()
    if not creds or creds.invalid:
        try:
            flow = client.flow_from_clientsecrets(os.getcwd() + "\\Bin\\Modules\\api\\client_secret.json", scopes)
        except json.decoder.JSONDecodeError:
            print("[!]Error: 'client_secret.json' file is invalid")
            return None
        creds = tools.run_flow(flow, store)
    build('gmail', 'v1', http=creds.authorize(Http()))

if __name__ == '__main__':
    main()