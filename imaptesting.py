import imaplib
import email

import debug_credentials
def decode_mime_words(s):
    return u''.join(
        word.decode(encoding or 'utf8') if isinstance(word, bytes) else word
        for word, encoding in email.header.decode_header(s))


imap_host = 'outlook.office365.com'
imap_user = debug_credentials.email
imap_pass = debug_credentials.password

# connect to host using SSL
imap = imaplib.IMAP4_SSL(host=imap_host)

## login to server
imap.login(imap_user, imap_pass)
imap.select("INBOX")
typ, rawdata = imap.search(None, 'ALL')
for num in rawdata[0].split():
    typ, rawdata = imap.fetch(num, '(RFC822)')
    _, uid = imap.fetch(num, "UID")
    for i in uid: 
        tmpUID = email.message_from_bytes(i)
        print(str(tmpUID).split("UID ")[1].split(")")[0]) # holy split
        
    print("new")
    msg = email.message_from_bytes(rawdata[0][1])
    mysubj = decode_mime_words(msg["Subject"])
    # print(mysubj)
    # decoded_header, charset = email.header.decode_header()
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                charset = part.get_content_charset()
                body = part.get_payload(decode=True).decode(encoding=charset, errors="ignore")
                # print(body)
    # else:
        # for part in msg.walk():
            # if part.get_content_type() == "None":
        # print(msg.get_payload())
    
imap.close()
imap.logout()