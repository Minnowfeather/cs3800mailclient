import mailbackend
import smtplib

b = mailbackend.mailbackend()

try:
    b.login("your email address goes here", "app password goes here")
except smtplib.SMTPAuthenticationError:
    print("womp womp :(")
    quit()
b.sendMail("destination address goes here", "Hello", "testing from thing")