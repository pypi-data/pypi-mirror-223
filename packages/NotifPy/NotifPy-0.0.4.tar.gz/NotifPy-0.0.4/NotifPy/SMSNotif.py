from twilio.rest import Client


class SMS_notif:
    def __init__(self, body, recipient_phone_number):
        self.body = body 
        self.recipient_phone_number = recipient_phone_number 
    def twillio(self, account_sid, auth_token, twilio_phone_number):
        self.account_sid = account_sid
        self.auth_token = auth_token
        self.twilio_phone_number = twilio_phone_number

        try:
            # Create a Twilio client
            client = Client(self.account_sid, self.auth_token)

            # Send the SMS
            message = client.messages.create(
                body=self.body,
                from_=self.twilio_phone_number,
                to=self.recipient_phone_number
            )

            print("SMS sent successfully! SID:", message.sid) #message.sid is like unqiue id of an SMS
        except Exception as e:
            print("Error sending SMS:", e)

