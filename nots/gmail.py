from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

token_storage = 'events.token.pickle'
cred_file = 'events_credentials.json'
base_email = 'pincomtz.events'


def init_service():
    SCOPES = ['https://www.googleapis.com/auth/gmail.modify',
              'https://www.googleapis.com/auth/gmail.settings.basic']
    creds = None
    if os.path.exists(token_storage):
        with open(token_storage, 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(cred_file, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(token_storage, 'wb') as token:
            pickle.dump(creds, token)
    return build('gmail', 'v1', credentials=creds)


def create_labels(service, name):
    m = f'ServiceNotifications/{name}'
    s = f'ServiceNotifications/{name}/Success'
    f = f'ServiceNotifications/{name}/Fail'
    labels = service.users().labels()
    res1 = labels.create(userId='me', body={'name': m}).execute()
    res2 = labels.create(userId='me', body={'name': s}).execute()
    res3 = labels.create(userId='me', body={'name': f}).execute()
    return (res1, res2, res3)


def setup_alias(service, name, email):
    res = create_labels(service, name)
    # alias_email = f'{base_email}+{name}@gmail.com'
    alias_email = email
    print(alias_email)
    fltr = {
        'criteria': {'to': alias_email},
        'action': {'addLabelIds': [res[0]['id']]}
    }
    settings = service.users().settings()
    return settings.filters().create(userId='me', body=fltr).execute()


def my_labels(service, name):
    results = service.users().labels().list(userId='me').execute()
    labels = results.get('labels', [])
    m = f'ServiceNotifications/{name}'
    s = f'ServiceNotifications/{name}/Success'
    f = f'ServiceNotifications/{name}/Fail'
    labels = list(
        filter(lambda x: x['name'] == m or x['name'] == s or x['name'] == f, labels))
    if len(labels) >= 2:
        res = {}
        for x in labels:
            if x['name'] == s:
                res['success'] = x['id']
            elif x['name'] == f:
                res['fail'] = x['id']
            elif x['name'] == m:
                res['main'] = x['id']
        return res
    return None
