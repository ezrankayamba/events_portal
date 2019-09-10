from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from companies.models import Company
from django.contrib.auth.models import User
from payments.models import Payment
import time
import re
import base64
import datetime

LABEL_SUCCESS = 'ReadMails/IOP1002/Success'
LABEL_FAIL = 'ReadMails/IOP1002/Fail'
COMPANY_EMAIL = 'nezatech.notification@gmail.com'

regex_lines = []
with open('trans_type_regex.properties', 'r') as regex_file:
    regex_lines = regex_file.readlines()


def record_payment(params, author, company):
    try:
        payment = Payment(trans_id=params['trans_id'],
                          payer_account=params['payer_account'],
                          payer_name=params['payer_name'],
                          payee_account=company.account,
                          payee_name=company.name,
                          amount=params['amount'].replace(',', ''),
                          trans_date=datetime.datetime.strptime(params['trans_date'], '%d/%m/%y %H:%M'),
                          author=author,
                          company=company)
        payment.save()
    except Exception as e:
        print(e)


def authoring():
    (username, _) = tuple(COMPANY_EMAIL.split('@'))
    company = Company.objects.filter(email=COMPANY_EMAIL).first()
    author = User.objects.filter(username=username).first()
    return (author, company)


def parse_mail(msg_text):
    for regex_line in regex_lines:
        key, regex = tuple(regex_line.split('='))
        test = re.findall(regex.strip(), msg_text.strip())
        match = test[0] if test else None
        pattern = ('type', 'amount', 'payer_account', 'payer_name', 'trans_id', 'trans_date', 'balance')
        if key == 'tigopesa.en':
            pattern = ('type', 'amount', 'payer_account', 'payer_name', 'trans_date', 'trans_id', 'balance')
        if match and len(match) == len(pattern):
            result = dict(zip(pattern, match))
            result['category'] = key
            print(result)
            author, company = authoring()
            record_payment(result, author, company)
            return True
        else:
            print(f'No match => {key}|{regex}|{msg_text}')
    return False


def init_service():
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
    return build('gmail', 'v1', credentials=creds)


def mail_reader_thread():
    service = init_service()
    labels = my_labels(service)
    while True:
        print('Reading mail...')
        # results = service.users().messages().list(userId='me', labelIds=['INBOX'], q='is:unread').execute()
        results = service.users().messages().list(userId='me', labelIds=['INBOX']).execute()
        messages = results.get('messages', [])
        for message in messages:
            msg = service.users().messages().get(userId='me', id=message['id']).execute()
            payload = msg['payload']
            subject = None
            for h in payload['headers']:
                if h['name'] == 'Subject':
                    subject = h['value']
                    break
            msg_text = None
            if 'parts' in payload:
                for p in payload['parts']:
                    print(p)
                    if p['mimeType'] == 'text/plain':
                        msg_text = base64.b64decode(p['body']['data']).decode('UTF-8')
                        break
            else:
                msg_text = base64.b64decode(payload['body']['data']).decode('UTF-8')

            if msg_text:
                parse_mail(msg_text)
                print('Successfully parsed the mail')
                msg_labels = {'removeLabelIds': ['INBOX'], 'addLabelIds': [labels['success']]}
                service.users().messages().modify(userId='me', id=message['id'], body=msg_labels).execute()
            else:
                print('Failed to parse the mail')
                msg_labels = {'removeLabelIds': ['INBOX'], 'addLabelIds': [labels['fail']]}
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
