from imapidle import imaplib


def read_incoming():
    print('Waiting inbox ...')
    m = imaplib.IMAP4_SSL('imap.gmail.com')
    m.login('robert', 'pa55w0rd')
    m.select()
    for uid, msg in m.idle():
        print(msg)
