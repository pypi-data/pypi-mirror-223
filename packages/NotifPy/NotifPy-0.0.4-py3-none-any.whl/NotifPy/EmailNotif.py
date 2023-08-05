import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class email_notif: 
    def __init__(self, sender_address=None, sender_password=None, recipient_email=None ):
        self.sender_address = sender_address
        self.sender_password = sender_password
        self.recipient_email = recipient_email

    def EmailSender(self, subject='', body='', html='', email_provider='gmail', custom_server=None, custom_port=None):
        sender_email = self.sender_address  #your email address eg 'foo@example.com'
        sender_password = self.sender_password      #your email password eg '123'
        recipient_email = self.recipient_email  #recipient's email address eg 'foo2@example.com'

        # Create a message object
        if html:
            msg = MIMEMultipart('alternative')
            

            part1 = MIMEText(body, 'plain')
            part2 = MIMEText(html, 'html')


            msg.attach(part1)
            msg.attach(part2)
        else:
            msg = MIMEText(body)

        msg['Subject'] = subject
        msg['From'] = sender_email
        msg['To'] = recipient_email

        try:

            #gmail
            if email_provider.lower() == 'gmail':
                print('Note: Due to recent google policy, 16 character app password is needed for gmail. How to get it? https://support.google.com/accounts/answer/6010255?hl=en')
                server = smtplib.SMTP('smtp.gmail.com', 587)  # Gmail SMTP server and port
            elif email_provider.lower() == 'yahoo':
            #yahoo
                server = smtplib.SMTP('smtp.mail.yahoo.com', 587)  # Yahoo SMTP server and port
            #outlook/hotmail
            elif email_provider.lower() == 'outlook':
                server = smtplib.SMTP('smtp-mail.outlook.com', 587)
            else:
                print(f'None of gmail, yahoo and outlook. Then on custom using server {custom_server} and port {custom_port}')
                server = smtplib.SMTP(custom_server, custom_port)
            server.starttls()

            # Log in to the sender's email account
            server.login(sender_email, sender_password)

            # Send the email
            server.sendmail(sender_email, recipient_email, msg.as_string())

            # Close the connection
            server.quit()
            print("Email sent successfully!")
        except Exception as e:
            print("Error sending email:", e)

