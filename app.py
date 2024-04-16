import tkinter
from tkinter import ttk, font
import mailbackend

# widget - a Text object
# text - a string of what to insert
def setText(widget, text):
    widget.config(state=tkinter.NORMAL)
    widget.delete('1.0', tkinter.END)
    widget.insert(tkinter.END, text)
    widget.config(state=tkinter.DISABLED)

# create instance of backend (this should create an SMTP conection to gmail)
backend = mailbackend.mailbackend()

# init window
root = tkinter.Tk()
root.title("Mail Client")
root.resizable(False, False)
# declare the default font 
DEFAULT_FONT = font.nametofont("TkDefaultFont")

# list of mail
mailList = tkinter.Listbox(root)
mailList.grid(rowspan=15,column=1, sticky="ns")

# sender label
label_sender = tkinter.Label(root, textvariable=tkinter.StringVar(value="Sender"))
label_sender.grid(row=0, column=2, sticky="w")
# actual sender box
frame_mailsender = tkinter.Frame(root, height=20)
frame_mailsender.grid(row=1, column=2, sticky="we")
frame_mailsender.grid_propagate(False)
mailSender = tkinter.Text(frame_mailsender, font=DEFAULT_FONT)
mailSender.grid(row=0, column=0)
setText(mailSender, "")

# subject label
label_subject = tkinter.Label(root, textvariable=tkinter.StringVar(value="Subject"))
label_subject.grid(row=2, column=2, sticky="w")
# actual subject box
frame_mailsubject = tkinter.Frame(root, height=20)
frame_mailsubject.grid(row=4, column=2, sticky="we")
frame_mailsubject.grid_propagate(False)
mailSubject = tkinter.Text(frame_mailsubject, font=DEFAULT_FONT)
mailSubject.grid(row=0, column=0)
setText(mailSubject, "")

# body label
label_body = tkinter.Label(root, textvariable=tkinter.StringVar(value="Body"))
label_body.grid(row=5, column=2, sticky="w")
# actual body box
mailBody = tkinter.Text(root, font=DEFAULT_FONT)
mailBody.grid(row=6, column=2)
setText(mailBody, "")

def showinbox():
    mailList.delete('0','end')
    
    setText(mailSender, "")
    setText(mailSubject, "")
    setText(mailBody, "")
    i = 0
    for mail in backend.getInbox():
        i = i + 1
        mailList.insert(i, mail["subject"])
def showtrash():
    print("wawa")


def onselect(evt):
    w = evt.widget
    if len(w.curselection()) < 1:
        return
    index = int(w.curselection()[0])
    tmpSubject = w.get(index)
    for mail in backend.getInbox():
        if mail["subject"] == tmpSubject:
            setText(mailSender, mail["sender"])
            setText(mailSubject, mail["subject"])
            setText(mailBody, mail["body"])
            return

mailList.bind('<<ListboxSelect>>', onselect)
# if you wanna pass arguments, do this
# command=lambda: myfunction("args")
inboxButton = ttk.Button(root, text="Inbox", command=showinbox)
inboxButton.grid(row=0,column=0)
trashButton = ttk.Button(root, text="Trash", command=showtrash)
trashButton.grid(row=1,column=0)

def login(emailaddress, apikey):
    try:
        backend.login(emailaddress, apikey)
    except:
        error_popup = tkinter.Toplevel(root)
        error_popup.title("Login failed.")
        error_popup.resizable(False,False)
        error_msg = tkinter.Label(error_popup, text="Login failed. Please check your login info and try again.")
        error_msg.grid(row=0, column=0)
        error_dismissbutton = tkinter.Button(error_popup, text="Ok", command=error_popup.destroy)
        error_dismissbutton.grid(row=1, column=0)
        # padding
        for child in error_popup.winfo_children():
            child.grid_configure(padx=2, pady=2)

def compose():
    # create popup
    composePopup = tkinter.Toplevel(root)
    composePopup.title("Compose new email")
    composePopup.resizable(False, False)

    # recipient label
    compose_label_recipient = tkinter.Label(composePopup, textvariable=tkinter.StringVar(value="To"))
    compose_label_recipient.grid(row=0, column=0, sticky="w")
    # actual sender box
    compose_frame_mailrecipient = tkinter.Frame(composePopup, height=20)
    compose_frame_mailrecipient.grid(row=1, column=0, sticky="we")
    compose_frame_mailrecipient.grid_propagate(False)
    compose_mailRecipient = tkinter.Text(compose_frame_mailrecipient, font=DEFAULT_FONT)
    compose_mailRecipient.grid(row=0, column=0)
    setText(compose_mailRecipient, "")

    # subject label
    compose_label_subject = tkinter.Label(composePopup, textvariable=tkinter.StringVar(value="Subject"))
    compose_label_subject.grid(row=2, column=0, sticky="w")
    # actual subject box
    compose_frame_mailsubject = tkinter.Frame(composePopup, height=20)
    compose_frame_mailsubject.grid(row=3, column=0, sticky="we")
    compose_frame_mailsubject.grid_propagate(False)
    compose_mailSubject = tkinter.Text(compose_frame_mailsubject, font=DEFAULT_FONT)
    compose_mailSubject.grid(row=0, column=0)

    # body label
    compose_label_body = tkinter.Label(composePopup, textvariable=tkinter.StringVar(value="Body"))
    compose_label_body.grid(row=4, column=0, sticky="w")
    # actual body box
    compose_mailBody = tkinter.Text(composePopup, font=DEFAULT_FONT)
    compose_mailBody.grid(row=5, column=0)

    compose_mailRecipient.config(state=tkinter.NORMAL)
    compose_mailSubject.config(state=tkinter.NORMAL)
    compose_mailBody.config(state=tkinter.NORMAL)

    send_button = ttk.Button(composePopup, text="Send", command=lambda: [sendMail(compose_mailRecipient.get('1.0', tkinter.END), compose_mailSubject.get('1.0', tkinter.END), compose_mailBody.get('1.0', tkinter.END)), composePopup.destroy()])
    send_button.grid(row=6, column=0, sticky="e")

    # pad each child in root 
    for child in composePopup.winfo_children(): 
        child.grid_configure(padx=2, pady=0)

def sendMail(recipient, subject, body):
    backend.sendMail(recipient=recipient, subject=subject, body=body)


def showlogin():
    popup = tkinter.Toplevel(root)
    popup.title("Login")
    popup.resizable(False, False)

    label_address = tkinter.Label(popup, text="Email Address:")
    label_address.grid(row=0, column=0)
    entry_address = tkinter.Entry(popup)
    entry_address.grid(row=0, column=1)

    label_apikey = tkinter.Label(popup, text="API key:")
    label_apikey.grid(row=1, column=0)
    entry_apikey = tkinter.Entry(popup)
    entry_apikey.grid(row=1, column=1)

    login_sumbit = tkinter.Button(popup, text="Login", command=lambda: login(entry_address.get(), entry_apikey.get()))
    login_sumbit.grid(row=2, column=0, columnspan=2)
    # popup.mainloop()
    

# accountButton = ttk.Button(root, text="Login", command=showlogin)

composeButton = ttk.Button(root, text="Compose", command=compose)
# pad each child in root 
for child in root.winfo_children(): 
    child.grid_configure(padx=2, pady=0)

showinbox()

passwordfile = open("apppass.txt")
backend.login("matthewparedes2k3@gmail.com", password=passwordfile.read())
# run
root.mainloop()
