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
import json
# import logging

# logger = logging.getLogger(__name__)

LABEL_SUCCESS = 'ReadMails/IOP1002/Success'
LABEL_FAIL = 'ReadMails/IOP1002/Fail'
COMPANY_EMAIL = 'nezatech.notification@gmail.com'

regex_lines = []
with open('trans_type_regex.properties', 'r') as regex_file:
    regex_lines = regex_file.readlines()


def record_payment(params, author, company):
    try:
        payer_account = params['payer_account'] if params['payer_account'].startswith('255') else f'255{params['payer_account']}'
        payment = Payment(trans_id=params['trans_id'],
                          payer_account=payer_account,
                          payer_name=params['payer_name'],
                          payee_account=company.account,
                          payee_name=company.name,
                          amount=params['amount'].replace(',', ''),
                          trans_date=datetime.datetime.strptime(
                              params['trans_date'].strip(), '%d/%m/%y %H:%M'),
                          author=author,
                          company=company,
                          channel=params['channel'],
                          receipt_no=params['receipt_no'])
        payment.save()
    except Exception as e:
        print(e)
        raise e


def authoring():
    (username, _) = tuple(COMPANY_EMAIL.split('@'))
    company = Company.objects.filter(email=COMPANY_EMAIL).first()
    author = User.objects.filter(username=username).first()
    return (author, company)


def parse_mail(msg_text, record_payment=True):
    try:
        for regex_line in regex_lines:
            key, regex = tuple(regex_line.split('='))
            test = re.findall(regex.strip(), msg_text.strip())
            match = test[0] if test else None
            if not match:
                continue
            pattern = ('prefix', 'amount', 'payer_account',
                       'payer_name', 'trans_id', 'trans_date', 'balance')
            if key == 'tigopesa.en':
                pattern = ('prefix', 'amount', 'payer_account',
                           'payer_name', 'trans_date', 'trans_id', 'balance')
            if key.startswith('iop.receiving'):
                pattern = ('prefix', 'balance', 'amount', 'channel', 'payer_account',
                           'payer_name', 'trans_id', 'receipt_no', 'trans_date')
            print(f'Match: {match}')
            if len(match) == len(pattern):
                result = dict(zip(pattern, match))
                result['msg_key'] = key
                if key.startswith('tigopesa'):
                    result['channel'] = 'Tigo'
                    result['receipt_no'] = 'ON-NET'
                print(result)
                if record_payment:
                    print(f'Recording payment...')
                    author, company = authoring()
                    record_payment(result, author, company)
                return True
            else:
                print(f'No match => {key}|{regex}|{msg_text}')
    except Exception as e:
        print(f'Error: {e}')
        # logger.error(e)
    print(f'No match for all available regex: {msg_text}')
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
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return build('gmail', 'v1', credentials=creds)


def mail_reader_thread():
    service = init_service()
    labels = my_labels(service)
    while True:
        print('Reading mail...')
        # logger.info(f'Reading mail ...')
        # results = service.users().messages().list(userId='me', labelIds=['INBOX'], q='is:unread').execute()
        results = service.users().messages().list(userId='me', labelIds=[
            'INBOX'], q='from:Tigo.Pesa@tigo.co.tz').execute()
        messages = results.get('messages', [])
        for message in messages:
            msg = service.users().messages().get(
                userId='me', id=message['id']).execute()
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
                        msg_text = base64.b64decode(
                            p['body']['data']).decode('UTF-8')
                        break
            else:
                msg_text = base64.b64decode(
                    payload['body']['data']).decode('UTF-8')

            if msg_text and parse_mail(msg_text):
                print('Successfully parsed the mail')
                # logger.info('Successfully parsed the mail')
                msg_labels = {'removeLabelIds': [
                    'INBOX'], 'addLabelIds': [labels['success']]}
                service.users().messages().modify(
                    userId='me', id=message['id'], body=msg_labels).execute()
            else:
                print('Failed to parse the mail')
                # logger.error('Successfully parsed the mail')
                msg_labels = {'removeLabelIds': [
                    'INBOX'], 'addLabelIds': [labels['fail']]}
                service.users().messages().modify(
                    userId='me', id=message['id'], body=msg_labels).execute()
            # break
        time.sleep(15)


def my_labels(service):
    results = service.users().labels().list(userId='me').execute()
    labels = results.get('labels', [])
    labels = list(
        filter(lambda x: x['name'] == LABEL_SUCCESS or x['name'] == LABEL_FAIL, labels))
    if len(labels) >= 2:
        res = {}
        for x in labels:
            if x['name'] == LABEL_SUCCESS:
                res['success'] = x['id']
            elif x['name'] == LABEL_FAIL:
                res['fail'] = x['id']
        return res
    return None


def test_messages():
    with open('sample_messages.json') as fp:
        messages = json.load(fp)
        for msg in messages:
            # print('\n', msg['id'])
            # print(msg['message'])
            parse_mail(msg['message'], record_payment=False)
            print('\n\n')
