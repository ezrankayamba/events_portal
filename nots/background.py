from __future__ import print_function
from companies.models import Company
from django.contrib.auth.models import User
from payments.models import Payment
import time
import re
import base64
import datetime
import json
from nots import gmail

regex_lines = []
with open('trans_type_regex.properties', 'r') as regex_file:
    regex_lines = regex_file.readlines()


def record_payment(params, author, company):
    try:
        print('Recording ...', params, author, company)
        pa = params['payer_account']
        payer_account = pa if pa.startswith('255') else f'255{pa}'
        payment = Payment(trans_id=params['trans_id'],
                          payer_account=payer_account,
                          payer_name=params['payer_name'],
                          payee_account=company.account,
                          payee_name=company.name,
                          amount=params['amount'].replace(',', ''),
                          trans_date=datetime.datetime.strptime(params['trans_date'].strip(), '%d/%m/%y %H:%M'),
                          author=author,
                          company=company,
                          channel=params['channel'],
                          receipt_no=params['receipt_no'])
        # print('Unsaved', payment)
        payment.save()
        print('Saved: ', payment)
    except Exception as e:
        print('Error during saving? ', e)
        # raise e


def authoring(email):
    (username, name) = tuple(email.split('@')[0].split('+'))
    company = Company.objects.filter(email=email).first()
    author, created = User.objects.get_or_create(
        username=username,
        email=f'{username}@gmail.com',
        password='notapplicable'
    )
    return (author, company)


def parse_mail(author, company, msg_text, dry_run=False):
    try:
        for regex_line in regex_lines:
            key, regex = tuple(regex_line.split('='))
            test = re.findall(regex.strip(), msg_text.strip())
            match = test[0] if test else None
            if not match:
                continue
            pattern = ('prefix', 'amount', 'payer_account', 'payer_name', 'trans_id', 'trans_date', 'balance')
            if key == 'tigopesa.en':
                pattern = ('prefix', 'amount', 'payer_account', 'payer_name', 'trans_date', 'trans_id', 'balance')
            if key.startswith('iop.receiving'):
                pattern = ('prefix', 'balance', 'amount', 'channel', 'payer_account', 'payer_name', 'trans_id', 'receipt_no', 'trans_date')
            print(f'Match: {match}')
            if len(match) == len(pattern):
                result = dict(zip(pattern, match))
                result['msg_key'] = key
                if key.startswith('tigopesa'):
                    result['channel'] = 'Tigo'
                    result['receipt_no'] = 'ON-NET'
                print(result)
                if not dry_run:
                    print(f'Recording payment...')
                    record_payment(result, author, company)
                return True
            else:
                print(f'No match => {key}|{regex}|{msg_text}')
    except Exception as e:
        print(f'Error: {e}')
        # logger.error(e)
    print(f'No match for all available regex: {msg_text}')
    return False


def mail_reader_thread():
    service = gmail.init_service()

    while True:
        print('Reading mail...')
        for c in Company.objects.all():
            author, company = authoring(c.email)
            name = c.email.split('@')[0].split('+')[1]
            labels = gmail.my_labels(service, name)
            q = 'from:Tigo.Pesa@tigo.co.tz'
            # q = 'from:ezrankayamba@gmail.com'
            msg_obj = service.users().messages()
            lbs_m = [labels['main']]
            lbs_s = [labels['success']]
            lbs_f = [labels['fail']]
            results = msg_obj.list(userId='me', labelIds=lbs_m, q=q).execute()
            messages = results.get('messages', [])
            for message in messages:
                msg = msg_obj.get(userId='me', id=message['id']).execute()
                payload = msg['payload']
                msg_text = None
                if 'parts' in payload:
                    for p in payload['parts']:
                        if p['mimeType'] == 'text/plain':
                            data = p['body']['data']
                            msg_text = base64.b64decode(data).decode('UTF-8')
                            break
                else:
                    data = payload['body']['data']
                    msg_text = base64.b64decode(data).decode('UTF-8')

                if msg_text and parse_mail(author, company, msg_text):
                    print('Successfully parsed the mail')
                    msg_labels = {'removeLabelIds': lbs_m, 'addLabelIds': lbs_s}
                    service.users().messages().modify(userId='me', id=message['id'], body=msg_labels).execute()
                else:
                    print('Failed to parse the mail')
                    msg_labels = {'removeLabelIds': lbs_m, 'addLabelIds': lbs_f}
                    service.users().messages().modify(userId='me', id=message['id'], body=msg_labels).execute()
                # break
        time.sleep(15)


def test_messages():
    with open('sample_messages.json') as fp:
        messages = json.load(fp)
        for msg in messages:
            parse_mail(msg['message'], dry_run=False)
            print('\n\n')
