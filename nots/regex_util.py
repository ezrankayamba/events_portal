import re

msg_text = '''Umepokea TSh 8,000 kutoka kwa 255714453267 - NERSON BABARA. Kumbukumbu No.: 57398119831 23/12/18 01:17. Salio lako jipya ni TSh 3,617,993. Asante kwa kutumia TigoPesa
[Tigo Tanzania]
Full details of Millicom and our disclaimer should be inspected at http://www.millicom.com/email_disclaimer.cfm This email should be read solely in conjunction with our disclaimer.'''

regex_lines = []
with open('trans_type_regex.properties', 'r') as regex_file:
    regex_lines = regex_file.readlines()


def parse_mail(msg_text):
    for regex_line in regex_lines:
        key, regex = tuple(regex_line.split('='))
        test = re.findall(regex.strip(), msg_text.strip())
        match = test[0] if test else None
        pattern = ('type', 'amount', 'sender_msisdn', 'sender_name', 'trans_id', 'trans_date', 'balance')
        if match:
            result = dict(zip(pattern, match))
            print(result)
            return True
        else:
            print(f'No match => {key}|{regex}|{msg_text}')
            return False
