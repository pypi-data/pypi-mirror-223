# NotifPy 
Available on https://pypi.org/project/NotifPy/

NotifPy is an all-in-one Python package designed to enable users to effortlessly send email and SMS notifications or alerts to designated email addresses and phone numbers. With NotifPy, integrating robust email and SMS functionalities into applications becomes seamless, facilitating prompt communication with target audiences.

Start Using NotifPy by 

```bash
pip install NotifPy
```

To employ email services follow the below steps:

```python
from NotifPy import EmailNotif
sender = EmailNotif.email_notif(sender_address='A@B.com', sender_password='your_email_password', recipient_email='B@C.com')
sender.EmailSender(subject = "It's me! Hi!", body='This is a test')
```

It is noteworthy, the default email service provider of package is gmail while simply it can be configured to yahoo, outlook/hotmail and the customized mode:
```python
sender.EmailSender(subject = "It's me! Hi!", body='This is a test', email_provider='yahoo')
sender.EmailSender(subject = "It's me! Hi!", body='This is a test', email_provider='outlook')
```

For customized mode, it can be set based on SMTP server and port of your choice. For instance, for AOL mail:
```python
sender.EmailSender(subject = "It's me! Hi!", body='This is a test', email_provider='', custom_server='smtp.aol.com', custom_port=587)
```

Furthermore, to use gmail service, due to recent Google policy, you need to first activate 2-step verfication then generate a 16-character app password for your email and use that password here. [Google App Password](https://support.google.com/accounts/answer/6010255?hl=en)

For SMS Notification, the current package version support Twillio service where based on account credentials the user is authenticated in our package. It should be noted, free trial is available
in Twillio. [Twillio Link](https://pages.twilio.com/twilio-brand-sales-namer-1?utm_source=bing&utm_medium=cpc&utm_term=twilio&utm_campaign=B_S_NAMER_Brand_Twilio&cq_src=bing_ads&cq_cmp=B_S_NAMER_Brand_Twilio&cq_con=Twilio%20-%20Phrase&cq_term=twilio&cq_med=&cq_net=o&cq_plt=bp&msclkid=ff15212c0a65142c696945e67a200330&utm_content=Twilio%20-%20Phrase)

To utilize SMS service please follow below steps:

```python
from NotifPy import SMSNotif
sender = SMSNotif.SMS_notif(body = "it's me Hi", recipient_phone_number= '+1...')
sender.twillio(account_sid="your account_sid from Twillio", auth_token="your auth_token from Twillio", twilio_phone_number="your number from Twillio")
```





## How to create this package

To create this package, you need to establish a directory of your choice (e.g., NotifPy) where you should place the __init__.py file and your Python files. It is worth noting that creating a directory like NotifPy.egg_info is unnecessary as it will be generated automatically. The package configuration can be facilitated with the setup.cfg file. You may adjust the version available on this repository to suit your package requirements.

In addition, the pyproject.toml file serves to specify the build backend and the essential build tools for the Python project. For the README.md file, it is important to recognize that this version may differ from the one displayed on pypi.org; therefore, it should be modified accordingly. Lastly, the license holds significance in clarifying the legal aspects of the app. If your package is intended for public accessibility, you can utilize the LICENSE of this package (with minor modifications such as changing the name and date). Alternatively, for more specific cases, you can refer to choosealicense.com.

Once all configurations are set, in this directory, execute the following command:

```
py -m build
```
Subsequently, a folder named "dist" will be generated. Ensure that you have active accounts on both [test.pypi.org](https://test.pypi.org/) and [pypi.org](https://pypi.org/).

It is advisable to begin by testing your package on [test.pypi.org](https://test.pypi.org/) to assure its performance before proceeding to upload it on [pypi.org](https://pypi.org/). The following steps should be followed for the upload process:

```
python -m twine upload --repository testpypi dist/*
```

```
python -m twine upload --repository pypi dist/*
```

