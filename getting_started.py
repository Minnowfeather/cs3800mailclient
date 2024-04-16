from Google import create_service
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

CLIENT_FILE = 'junior/cs3800-sp24/MailClientServer/MailClientCredentials.json'
API_NAME = 'gmail'
API_VERSION = 'v1'
SCOPES = ['https://mail.google.com/']

service = create_service(CLIENT_FILE, API_NAME, API_VERSION, SCOPES)

emailMsg = 'This is a test email'
mimeMessage = MIMEMultipart()
mimeMessage['to'] = '<Recipient>@gmail.com'
mimeMessage['subject'] = 'Hello'
mimeMessage.attach(MIMEText(emailMsg, 'plain'))
raw_string = base64.urlsafe_b64encode(mimeMessage.as_bytes()).decode()

message = service.users().messages().send(userId='me', body={'raw': raw_string}).execute()
print(message)