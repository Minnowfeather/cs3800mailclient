import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587

class mailbackend:

    def __init__(self):
        # Establishing a connection to SMTP server with TLS encryption
        self._server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        self._server.starttls()
    
    def login(self, email, password):
        # login with given credentials
        # raise smtplib exception if credentials don't work
        try:
            self._email = email
            self._server.login(self._email, password)
        except smtplib.SMTPAuthenticationError:
            print("waow")
    
    def sendMail(self, recipient, subject, body, attachment=None):
        # Header
        msg = MIMEMultipart()
        msg['From'] = self._email
        msg['To'] = recipient
        msg['Subject'] = subject
        # Message
        msg.attach(MIMEText(body, 'plain'))  # Attaching

        if attachment is not None:
            p = MIMEBase('application', 'octet-stream')  # Processing attachment
            encoders.encode_base64(p)
            p.set_payload(attachment)
            p.add_header('Content-Disposition', f'attachment; filename={filename}')
            msg.attach(p)
        
        self._server.sendmail(self._email, msg['To'], msg.as_string())

    def getInbox(self):
        return [{"subject":"bingus", "sender": "mail1@gmail.com", "body":"bongus"},
                {"subject":"mailtwo", "sender": "mail2@gmail.com", "body":"this is the second email"},
                {"subject":"this is the third mail", "sender": "mail3@gmail.com", "body":"epic mail time"}

                ]

