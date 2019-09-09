from __future__ import print_function
from django.shortcuts import render
from google.cloud import pubsub_v1
import time

import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


topic = 'email-nots'
project_id = 'pincomtz'


# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


def main():
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
    service = build('gmail', 'v1', credentials=creds)

    results = service.users().labels().list(userId='me').execute()
    labels = results.get('labels', [])

    if not labels:
        print('No labels found.')
    else:
        print('Labels:')
        for label in labels:
            print(label['name'])


def enable_watch():
    topic_name = f'projects/{project_id}/topics/{topic}'
    request = {
        'labelIds': ['INBOX'],
        'topicName': topic_name
    }
    res = gmail.users().watch(userId='me', body=request).execute()
    print(res)


def create_topic():
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic)
    topic_created = publisher.create_topic(topic_path)
    print('Topic created: {}'.format(topic_created))


def subscribe():
    sub = 'email-nots'
    subscriber = pubsub_v1.SubscriberClient()
    topic_name = f'projects/{project_id}/topics/{topic}'
    subscription_name = f'projects/{project_id}/subscriptions/{sub}'
    subscriber.create_subscription(name=subscription_name, topic=topic_name)

    def callback(message):
        print(message.data)
        message.ack()

    future = subscriber.subscribe(subscription_name, callback)
    print(future)


def pull_mails():
    sub = 'email-nots'
    subscriber = pubsub_v1.SubscriberClient()
    subscription_name = f'projects/{project_id}/subscriptions/{sub}'
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(project_id, subscription_name)

    def callback(message):
        print('Received message: {}'.format(message))
        message.ack()

    subscriber.subscribe(subscription_path, callback=callback)
    print('Listening for messages on {}'.format(subscription_path))
    while True:
        print(f'Waiting new mail inbox ...')
        time.sleep(60)
