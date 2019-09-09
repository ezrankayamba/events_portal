from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import time

LABEL_SUCCESS = 'ReadMails/IOP1002/Success'
LABEL_FAIL = 'ReadMails/IOP1002/Fail'


def main():
    SCOPES = ['https://www.googleapis.com/auth/gmail.modify']
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    service = build('gmail', 'v1', credentials=creds)
    labels = my_labels(service)
    while True:
        print('Reading mail...')
        # results = service.users().messages().list(userId='me', labelIds=['INBOX'], q='is:unread').execute()
        results = service.users().messages().list(userId='me', labelIds=['INBOX']).execute()
        messages = results.get('messages', [])
        for message in messages:
            msg = service.users().messages().get(userId='me', id=message['id']).execute()
            print(msg['snippet'])
            msg_labels = {'removeLabelIds': ['INBOX'], 'addLabelIds': [labels['success']]}
            service.users().messages().modify(userId='me', id=message['id'], body=msg_labels).execute()
            # break
        time.sleep(15)


def my_labels(service):
    results = service.users().labels().list(userId='me').execute()
    labels = results.get('labels', [])
    labels = list(filter(lambda x: x['name'] == LABEL_SUCCESS or x['name'] == LABEL_FAIL, labels))
    if len(labels) >= 2:
        res = {}
        for x in labels:
            if x['name'] == LABEL_SUCCESS:
                res['success'] = x['id']
            elif x['name'] == LABEL_FAIL:
                res['fail'] = x['id']
        return res
    return None
