import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

SMTP_PORT = 587

class mailbackend:
    def __init__(self):
        self._smtpserver = None
        self._email = None
        self._password = None
    

    # login with given credentials
    # raise smtplib exception if credentials don't work
    def login(self, email : str, password):
        if(email.endswith("@gmail.com")):
            self._smtpserver = "smtp.gmail.com"
        elif(email.endswith("@yahoo.com")):
            self._smtpserver = "smtp.mail.yahoo.com"
        elif(email.endswith("@outlook.com")):
            self._smtpserver = "smtp-mail.outlook.com"
        else:
            raise Exception("Invalid email address.")

        self._email = email
        self._password = password

        # Test credentials
        server = smtplib.SMTP(self._smtpserver, SMTP_PORT)
        server.starttls()
        server.login(self._email, self._password)
        server.quit()
    
    def logout(self):
        self._email = None
        self._password = None
        self._smtpserver = None
    # sends mail
    # attachment should be an attachment by created by opening and then reading as binary
    # ex:
    # with open(filename, 'rb') as f:
    #   attachment = f.read()
    def sendMail(self, recipient : str, subject : str, body : str, attachment : bytes):
        # Establishing a connection to SMTP server with TLS encryption
        server = smtplib.SMTP(self._smtpserver, SMTP_PORT) # creates connection
        server.starttls() # sets TLS encryption (requires an EHLO after)
        server.login(self._email, self._password) #login (implicitly calls EHLO if hasn't happened yet)
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
        
        server.sendmail(self._email, msg['To'], msg.as_string())
        server.quit()

    def getInbox(self):
        return [{"subject":"test mail", "sender": "mail1@gmail.com", "body":"bongus"},
                {"subject":"mailtwo", "sender": "mail2@gmail.com", "body":"this is the second email"},
                {"subject":"this is the third mail", "sender": "mail3@gmail.com", "body":"epic mail time"}

                ]
