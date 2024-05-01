import tkinter
from tkinter import ttk, font, filedialog
import mailbackend

import debug_credentials
# widget - a Text object
# text - a string of what to insert
def setText(widget, text):
    widget.config(state=tkinter.NORMAL)
    widget.delete('1.0', tkinter.END)
    widget.insert(tkinter.END, text)
    widget.config(state=tkinter.DISABLED)


logged_in = False

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

cached_inbox = []
def showinbox():
    global cached_inbox
    if not logged_in:
        print("fail")
        return
    mailList.delete('0','end')
    
    setText(mailSender, "")
    setText(mailSubject, "")
    setText(mailBody, "")
    i = 0
    cached_inbox = backend.getInbox()
    for mail in cached_inbox:
        i = i + 1
        mailList.insert(i, mail["Subject"])
def showtrash():
    print("wawa")


def onselect(evt):
    w = evt.widget
    if len(w.curselection()) < 1:
        return
    index = int(w.curselection()[0])
    selected_mail = cached_inbox[index]
    setText(mailSender, selected_mail["Sender"])
    setText(mailSubject, selected_mail["Subject"])
    setText(mailBody, selected_mail["Body"])
        

mailList.bind('<<ListboxSelect>>', onselect)
# if you wanna pass arguments, do this
# command=lambda: myfunction("args")
inboxButton = ttk.Button(root, text="Inbox", command=showinbox)
inboxButton.grid(row=0,column=0)
# trashButton = ttk.Button(root, text="Trash", command=showtrash)
# trashButton.grid(row=1,column=0)


def makepopup(title : str, body : str, dismisstext : str = "Okay"):
    popup = tkinter.Toplevel(root)
    popup.title(title)
    popup.resizable(False,False)
    popup_msg = tkinter.Label(popup, text=body)
    popup_msg.grid(row=0, column=0)
    popup_dismiss = tkinter.Button(popup, text=dismisstext, command=popup.destroy)
    popup_dismiss.grid(row=1, column=0)
    # padding
    for child in popup.winfo_children():
        child.grid_configure(padx=2, pady=2)

def logout():
    global logged_in
    backend.logout()
    logged_in = False
    makepopup("Logout success", "Succesfully logged out.")
    accountButton.config(text="Login", command=showlogin)


def login(sourcepopup : tkinter.Toplevel, emailaddress, apikey):
    global logged_in
    try:
        backend.login(emailaddress, apikey)
        sourcepopup.destroy()
    except:
        makepopup("Login failed", "Login failed. Please check your login info and try again.")
    else:
        logged_in = True
        makepopup("Login success", "Success. You are now logged in")
        accountButton.config(text="Logout", command=logout)



compose_attachment = None

def loadattachment():
    global compose_attachment
    compose_attachment = filedialog.askopenfilename()
def compose():
    global compose_attachment
    compose_attachment = None
    if not logged_in:
        makepopup("Error", "You must login before you can send a message.")
        return
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
    
    # frame at the bottom so that nothing extends past the body
    bottombar_frame = tkinter.Frame(composePopup)
    bottombar_frame.grid(row=6, column=0, sticky="we")
    # 50/50 split of column 0 and 1
    bottombar_frame.grid_columnconfigure(0, weight=1)
    bottombar_frame.grid_columnconfigure(1, weight=1)
    addattachment_button = ttk.Button(bottombar_frame, text="Add attachment...", command=loadattachment)
    addattachment_button.grid(row=0, column=0, sticky="w")
    send_button = ttk.Button(bottombar_frame, text="Send", command=lambda: [sendMail(compose_mailRecipient.get('1.0', tkinter.END), compose_mailSubject.get('1.0', tkinter.END), compose_mailBody.get('1.0', tkinter.END), filename=compose_attachment), composePopup.destroy()])
    send_button.grid(row=0, column=1, sticky="e")

    # pad each child in root 
    for child in composePopup.winfo_children(): 
        child.grid_configure(padx=2, pady=0)

def sendMail(recipient, subject, body, filename=None):
    backend.sendMail(recipient=recipient, subject=subject, body=body, filename=filename)


def showlogin():
    popup = tkinter.Toplevel(root)
    popup.title("Login")
    popup.resizable(False, False)

    label_address = tkinter.Label(popup, text="Email Address:")
    label_address.grid(row=0, column=0)
    entry_address = tkinter.Entry(popup)
    entry_address.grid(row=0, column=1)

    label_password = tkinter.Label(popup, text="Password:")
    label_password.grid(row=1, column=0)
    entry_password = tkinter.Entry(popup, show="*")
    entry_password.grid(row=1, column=1)

    login_sumbit = tkinter.Button(popup, text="Login", command=lambda: login(popup, entry_address.get(), entry_password.get()))
    login_sumbit.grid(row=2, column=0, columnspan=2)
    # popup.mainloop()
    

accountButton = ttk.Button(root, text="Login", command=showlogin)

composeButton = ttk.Button(root, text="Compose", command=compose)
composeButton.grid(column=0, row=2, sticky="s")
# pad each child in root 
for child in root.winfo_children(): 
    child.grid_configure(padx=2, pady=0)

backend.login(debug_credentials.email, debug_credentials.password)
logged_in = True
# run
root.mainloop()
