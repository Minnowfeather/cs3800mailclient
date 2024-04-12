class mailbackend:
    def __init__(self):
        # create smtp connection here
        print("wawa")
    
    def login(self):
        # login with given credentials
        # raise smtplib exception if credentials don't work
        raise Exception

    def getInbox(self):
        return [{"subject":"bingus", "sender": "mail1@gmail.com", "body":"bongus"},
                {"subject":"mailtwo", "sender": "mail2@gmail.com", "body":"this is the second email"},
                {"subject":"this is the third mail", "sender": "mail3@gmail.com", "body":"epic mail time"}

                ]

