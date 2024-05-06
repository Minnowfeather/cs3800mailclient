from email.header import decode_header
import smtplib
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import imaplib
import os

SMTP_PORT = 587


def decode_mime_words(s):
    return u''.join(
        word.decode(encoding or 'utf8') if isinstance(word, bytes) else word
        for word, encoding in email.header.decode_header(s))

class mailbackend:
    def __init__(self):
        self._smtpserver = None
        self._imapserver = None
        self._email = None
        self._password = None
    

    # login with given credentials
    # raise smtplib exception if credentials don't work
    def login(self, email : str, password): #TODO: add more smtp servers
        if(email.endswith("@gmail.com")):
            self._smtpserver = "smtp.gmail.com"
            self._imapserver = "imap.gmail.com"
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
    def sendMail(self, recipient : str, subject : str, body : str, filename : str):
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

        attachment = None
        if filename is not None:
            with open(filename, "rb") as file:
                attachment = file.read()
                file.close()

        if attachment is not None:
            p = MIMEBase('application', 'octet-stream')  # Processing attachment
            p.set_payload(attachment)
            encoders.encode_base64(p)
            p.add_header('Content-Disposition', f'attachment; filename={os.path.basename(filename)}')
            msg.attach(p)
        
        server.sendmail(self._email, msg['To'], msg.as_string())
        server.quit()

    def getInbox(self):
        # connect to host using SSL
        imap = imaplib.IMAP4_SSL(host=self._imapserver)

        emails = []

        # login to server
        imap.login(self._email, self._password)
        imap.select("INBOX")
        typ, rawdata = imap.search(None, 'ALL')
        for num in rawdata[0].split():
            typ, rawdata = imap.fetch(num, '(RFC822)')
            msg = email.message_from_bytes(rawdata[0][1])
            tmpMessage = {}
            tmpMessage["Subject"] = decode_mime_words(msg["Subject"])
            tmpMessage["Sender"] = msg["From"]
            tmpMessage["Body"] = "Error retrieving body."
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == "text/plain":
                        charset = part.get_content_charset()
                        body = part.get_payload(decode=True).decode(encoding=charset, errors="ignore")
                        tmpMessage["Body"] = body
            else:
                tmpMessage["Body"] = msg.get_payload(decode=True)
            emails.append(tmpMessage)    

        imap.close()
        imap.logout()
        emails.reverse()
        return emails
    
    def deleteEmail(self, email_index):
        imap = imaplib.IMAP4_SSL(host=self._imapserver)

        try:
            imap.login(self._email, self._password)
            imap.select("INBOX")

            # Fetch the sequence number of the email based on its index
            status, messages = imap.search(None, 'ALL')
            messages = messages[0].split()

            for idx, mail in enumerate(messages, start=1):
                if idx == email_index:
                    _, msg = imap.fetch(mail, "(RFC822)")
                    imap.store(mail, "+FLAGS", "\\Deleted")
                    imap.expunge()
                    break

        except Exception as e:
            print("Error deleting email:", e)

        finally:
            imap.close()
            imap.logout()
            
    def replyTo(self, email_index):
        imap = imaplib.IMAP4_SSL(host=self._imapserver)
        
        try:
            imap.login(self._email, self._password)
            imap.select("INBOX")

            # Fetch the sequence number of the email based on its index
            status, messages = imap.search(None, 'ALL')
            messages = messages[0].split()

            msg_id = messages[email_index - 1]

            # Fetch the email message
            _, msg_data = imap.fetch(msg_id, "(RFC822)")
            raw_email = msg_data[0][1]
            email_message = email.message_from_bytes(raw_email)

            sender = email_message["From"]
            reply_body = "Dear " + sender + ",\n\n"

            self.sendMail(sender, reply_body, None)
            
        except Exception as e:
            print("Error replying to email:", e)

        finally:
            imap.close()
            imap.logout()
        
        