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
            self._imapserver = "outlook.office365.com"
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

    def getInbox(self, batch_size=100):
        emails = []

        # Connect to IMAP server
        with imaplib.IMAP4_SSL(self._imapserver) as imap:
            # Login to server
            imap.login(self._email, self._password)

            # Select INBOX
            imap.select("INBOX")

            # Search for all emails
            _, data = imap.search(None, 'ALL')

            # Fetch UIDs for each email
            _, uid_data = imap.uid('search', None, 'ALL')
            uids = uid_data[0].split()

            # Process emails in batches
            for i in range(0, len(uids), batch_size):
                batch_uids = uids[i:i+batch_size]

                # Fetch messages for the current batch
                _, msg_data = imap.uid('fetch', ','.join(uid.decode() for uid in batch_uids), '(RFC822)')
                for response_part in msg_data:
                    if isinstance(response_part, tuple):
                        raw_email = response_part[1]
                        msg = email.message_from_bytes(raw_email)
                        
                        tmpMessage = {}
                        tmpMessage["UID"] = msg.get("Message-ID", "")  # Use Message-ID as UID if available

                        # Fetch subject and sender
                        tmpMessage["Subject"] = decode_mime_words(msg.get("Subject", ""))
                        tmpMessage["Sender"] = msg.get("From", "")

                        # Fetch body (if available)
                        body = ""
                        if msg.is_multipart():
                            for part in msg.walk():
                                if part.get_content_type() == "text/plain":
                                    charset = part.get_content_charset()
                                    body = part.get_payload(decode=True).decode(encoding=charset, errors="ignore")
                                    break
                        else:
                            body = msg.get_payload(decode=True)
                        tmpMessage["Body"] = body.strip()

                        emails.append(tmpMessage)

        # Reverse the order of emails (if needed)
        emails.reverse()
        return emails
    
    def getSentInbox(self, batch_size=30):
        sent_emails = []

        # Connect to IMAP server
        with imaplib.IMAP4_SSL(self._imapserver) as imap:
            # Login to server
            imap.login(self._email, self._password)

            # Select the "Sent" mailbox
            imap.select('"[Gmail]/Sent Mail"')  # Modify this to match your mailbox name

            # Search for emails sent by the user
            _, data = imap.search(None, 'FROM', self._email)

            # Fetch UIDs for each email
            _, uid_data = imap.uid('search', None, 'FROM', self._email)
            uids = uid_data[0].split()

            # Process emails in batches
            for i in range(0, len(uids), batch_size):
                batch_uids = uids[i:i+batch_size]

                # Fetch messages for the current batch
                _, msg_data = imap.uid('fetch', ','.join(uid.decode() for uid in batch_uids), '(RFC822)')
                for response_part in msg_data:
                    if isinstance(response_part, tuple):
                        raw_email = response_part[1]
                        msg = email.message_from_bytes(raw_email)

                        tmpMessage = {}
                        tmpMessage["UID"] = msg.get("Message-ID", "")  # Use Message-ID as UID if available

                        # Fetch subject and sender
                        tmpMessage["Subject"] = decode_mime_words(msg.get("Subject", ""))
                        tmpMessage["Sender"] = msg.get("From", "")

                        # Fetch body (if available)
                        body = ""
                        if msg.is_multipart():
                            for part in msg.walk():
                                if part.get_content_type() == "text/plain":
                                    charset = part.get_content_charset()
                                    body = part.get_payload(decode=True).decode(encoding=charset, errors="ignore")
                                    break
                        else:
                            body = msg.get_payload(decode=True)
                        tmpMessage["Body"] = body.strip()

                        sent_emails.append(tmpMessage)

        # Reverse the order of emails (if needed)
        sent_emails.reverse()
        return sent_emails
    
    def deleteEmail(self, email_uid):
        imap = imaplib.IMAP4_SSL(host=self._imapserver)
        try:
            imap.login(self._email, self._password)
            imap.select("INBOX")
            
            # Search directly for the UID
            status, messages = imap.search(None, f'UID {email_uid}')
            if status == 'OK' and messages[0]:
                for mail in messages[0].split():
                    imap.store(mail, "+FLAGS", "\\Deleted")
                imap.expunge()
            else:
                print(f"Email UID {email_uid} not found")

        except imaplib.IMAP4.error as e:
            print(f"IMAP error: {e}")
        except Exception as e:
            print(f"General error: {e}")
        finally:
            try:
                imap.close()
            except:
                pass
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
        
        