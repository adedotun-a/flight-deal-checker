import os
from twilio.rest import Client

account_sid = os.environ['TWILIO_SID']
auth_token = os.environ['TWILIO_TOKEN']
twilio_phone_number = os.environ['TWILIO_PHONE_NUMBER']
my_phone_number = os.environ['MY_PHONE_NUMBER']


class NotificationManager:
    # This class is responsible for sending notifications with the deal flight details.
    def __init__(self):
        self.client = Client(account_sid, auth_token)

    def send_sms(self, msg):
        message = self.client.messages.create(body=msg, from_=twilio_phone_number, to=my_phone_number)
        print(message.sid)
