import tkinter
from tkinter import ttk, font, messagebox
from tkinter import filedialog
import tkinter.constants
import mailbackend
from pathlib import Path

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / "assets" / "frame1"

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def setText(widget, text):
    widget.config(state=tkinter.NORMAL)
    widget.delete('1.0', tkinter.END)
    widget.insert(tkinter.END, text)
    widget.config(state=tkinter.DISABLED)
    
logged_in = False
backend = mailbackend.mailbackend()
    
# init window
root = tkinter.Tk()
root.title("Mail Client")
root.geometry("978x640")
root.resizable(False, False)
root.configure(bg="#FFFFFF")
# declare the default font 
DEFAULT_FONT = font.nametofont("TkDefaultFont")

# Diving inbox/mailviewer/header
line1 = tkinter.Frame(root, width=840, height=0, bg="#D4D4D4")
line1.place(x=138,y=62)
line2 = tkinter.Frame(root, width=0, height=578, bg="#D4D4D4")
line2.place(x=466,y=62)

# Header
headerFrame = tkinter.Frame(root, width=840, height=62, bg="#FFFFFF")
headerFrame.place(x=138,y=0)
email_text = tkinter.Label(headerFrame, textvariable=tkinter.StringVar(value="Email"), fg="black", bg="#FFFFFF")
email_text.place(x=24,y=22, anchor="nw")
email_text.configure(font=("Inter", 20 * -1))
profile_photo = tkinter.PhotoImage(file=relative_to_assets("profile.png"))
profile = tkinter.Label(headerFrame, image=profile_photo, bg="#FFFFFF")
profile.place(x=792, y=14)

# MailList 
mailList = tkinter.Listbox(root, background="#FFFFFF", borderwidth=0)
mailList.place(x=138, y=63, width=329, height=578)

# MailView
def showMailView():
    global mailView, mailSender, mailSubject, mailBody
    mailView = tkinter.Frame(root, width=510, height=578, bg="#FFFFFF")
    mailView.place(x=468,y=63)
    mailSubject = tkinter.Text(mailView, font=("Inter", 15 * -1), borderwidth=0)
    mailSubject.place(x=15,y=34,width=445, height=23)
    setText(mailSubject, "")

    from_label = tkinter.Label(mailView, textvariable=tkinter.StringVar(value="From:"), fg="black", bg="#FFFFFF")
    from_label.place(x=15,y=76)
    from_label.config(font=("Inter", 12 * -1))

    mailSender = tkinter.Text(mailView, font=("Inter", 12 * -1), borderwidth=0)
    mailSender.place(x=53,y=76,width=442, height=20)
    setText(mailSender, "")

    toyou = tkinter.Label(mailView, textvariable=tkinter.StringVar(value="To: You"), fg="black", bg="#FFFFFF")
    toyou.place(x=15,y=104)
    toyou.config(font=("Inter", 12 * -1))

    mailBody = tkinter.Text(mailView, font=("Inter", 12 * -1), fg="black", width=68, height=28, borderwidth=0, highlightthickness=1, highlightbackground="#DBDBDB")
    mailBody.place(x=8, y=141,width=490, height=407)
    setText(mailBody, "")
    
def showFrame():
    global emptyFrame, mail_image  # Declare mail_image as a global variable
    emptyFrame = tkinter.Frame(root, width=510, height=578, bg="#FFFFFF")
    emptyFrame.place(x=468,y=63)
    mail_image = tkinter.PhotoImage(file=relative_to_assets("empty.png"))  # Store in a global variable
    mail_photo = tkinter.Label(emptyFrame, image=mail_image, bg="#FFFFFF")
    mail_photo.place(x=229,y=231)
    mailText = tkinter.Label(emptyFrame, textvariable=tkinter.StringVar(value="Select mail to read"), fg="black", bg="#FFFFFF")
    mailText.place(x=205,y=305)
    
def hideFrame():
    emptyFrame.destroy()
showFrame()

    
cached_inbox = []
def showInbox():
    global cached_inbox
    if not logged_in:
        messagebox.showinfo("Error", "You must login before you view your inbox.")
        return
    mailList.delete('0','end')
    
    
    i = 0
    cached_inbox = backend.getInbox()
    for mail in cached_inbox:
        i = i + 1
        subject = mail["Subject"]
        if not subject:
            subject = "(No Subject)"
        mailList.insert(i, subject)
        
def showSentInbox():
    global cached_inbox
    if not logged_in:
        messagebox.showinfo("Error", "You must login before you view your inbox.")
        return
    mailList.delete('0','end')
    
    i = 0
    cached_inbox = backend.getSentInbox()
    for mail in cached_inbox:
        i = i + 1
        subject = mail["Subject"]
        if not subject:
            subject = "(No Subject)"
        mailList.insert(i, subject)

def onselect(evt):
    w = evt.widget
    if len(w.curselection()) < 1:
        return
    hideFrame()
    showMailView()
    index = int(w.curselection()[0])
    selected_mail = cached_inbox[index]
    setText(mailSender, selected_mail["Sender"])
    subject = selected_mail["Subject"] if selected_mail["Subject"] else "No Subject"
    setText(mailSubject, subject)
    setText(mailBody, selected_mail["Body"])
    
mailList.bind('<<ListboxSelect>>', onselect)

def showlogin():
    global login_window, user_email_entry
    login_window = tkinter.Toplevel()  # Use Toplevel window for login screen
    login_window.title("Mail Client")
    login_window.geometry("510x578")
    login_window.resizable(False, False)
    login_window.configure(bg="#FFFFFF")
    
    header = tkinter.Frame(login_window, width=510, height=70, bg="#25354C")
    header.place(x=0, y=0)
    title = tkinter.Label(header, text="MailClient", bg="#25354C", fg="#FFFFFF")
    title.place(x=217, y=25)
    title.configure(font=("Inter", 20 * -1))
    
    email_label = tkinter.Label(login_window, textvariable=tkinter.StringVar(value="Email Address"), fg="black", bg="#FFFFFF")
    email_label.place(x=200,y=195)
    email_label.configure(font=("Inter", 18 * -1))
    email_entry = tkinter.Entry(login_window, fg="black", borderwidth=0, highlightthickness=1, highlightbackground="#DBDBDB")
    email_entry.place(x=143,y=217,width=230, height=25)
    
    pass_label = tkinter.Label(login_window, textvariable=tkinter.StringVar(value="Password"), fg="black", bg="#FFFFFF")
    pass_label.place(x=218,y=317)
    pass_label.configure(font=("Inter", 18 * -1))
    pass_entry = tkinter.Entry(login_window, fg="black", show="•", borderwidth=0, highlightthickness=1, highlightbackground="#DBDBDB")
    pass_entry.place(x=143, y=339, width=230, height=25)
    
    
    login_button = tkinter.Button(
        login_window, 
        textvariable=tkinter.StringVar(value="Login"), 
        borderwidth=0, 
        fg="#6CC144",
        bg="#FFFFFF",
        font=("Inter", 16, "bold"),
        command=lambda: login(email_entry.get(), pass_entry.get())
        )
    login_button.place(x=200, y=460, width=120, height=30)
    
def login(emailaddress, apikey):
    global logged_in, user_email
    try:
        backend.login(emailaddress, apikey)
    except:
        messagebox.showinfo("Login failed", "Login failed. Please check your login info and try again.")
    else:
        logged_in = True
        user_email = emailaddress
        messagebox.showinfo("Login success", "Success. You are now logged in")
        account_button.configure(image=logout_image, command=logout)
        login_window.destroy()
        
def logout():
    global logged_in
    global image
    backend.logout()
    logged_in = False
    mailList.delete(0, tkinter.END)
    showFrame()
    messagebox.showinfo("Logout success", "Succesfully logged out.")
    account_button.configure(image=login_image, command=showlogin)
    
compose_attachment = None

def loadattachment():
    global compose_attachment
    compose_attachment = filedialog.askopenfilename()
    
def compose():
    global compose_attachment, send_image, user_email
    compose_attachment = None
    if not logged_in:
        messagebox.showinfo("Error", "You must login before you can send a message.")
        return
    composeFrame = tkinter.Frame(root, width=510, height=578, bg="#FFFFFF")
    composeFrame.place(x=468,y=63)
    
    from_label = tkinter.Label(composeFrame, textvariable=tkinter.StringVar(value="From"), font=("Inter", 12 * -1), bg="#FFFFFF")
    from_label.place(x=12,y=12)
    from_text = tkinter.Entry(composeFrame, font=("Inter", 12 * -1), bg="#FFFFFF", width=69, borderwidth=0, highlightthickness=1, highlightbackground="#DBDBDB")
    from_text.place(x=12,y=28)
    from_text.insert(0, user_email)
    
    to_label = tkinter.Label(composeFrame, textvariable=tkinter.StringVar(value="To"), font=("Inter", 12 * -1), bg="#FFFFFF")
    to_label.place(x=12,y=48)
    to_text = tkinter.Entry(composeFrame, font=("Inter", 12 * -1), bg="#FFFFFF", width=69, borderwidth=0, highlightthickness=1, highlightbackground="#DBDBDB")
    to_text.place(x=12,y=64)
    
    subject_label = tkinter.Label(composeFrame, textvariable=tkinter.StringVar(value="Subject"), font=("Inter", 12 * -1), bg="#FFFFFF")
    subject_label.place(x=12,y=84)
    subject_text = tkinter.Entry(composeFrame, font=("Inter", 12 * -1), bg="#FFFFFF", width=69, borderwidth=0, highlightthickness=1, highlightbackground="#DBDBDB")
    subject_text.place(x=12,y=102)
    
    body_label = tkinter.Label(composeFrame, textvariable=tkinter.StringVar(value="Body"), font=("Inter", 12 * -1), bg="#FFFFFF")
    body_label.place(x=12,y=136)
    
    mailBody = tkinter.Text(composeFrame, font=("Inter", 12 * -1), fg="black", borderwidth=0, highlightthickness=1, highlightbackground="#DBDBDB")
    mailBody.place(x=12, y=154, width=489,height=397)
    
    attach_button = tkinter.Button(composeFrame, text="Attach", bg="#FFFFFF",borderwidth=.5,padx=0,pady=0,font=("Inter", 11 * -1), command=loadattachment)
    attach_button.configure(width=8)
    attach_button.place(x=445,y=131)
    
    send_image = tkinter.PhotoImage(file=relative_to_assets("send.png"))
    send_button = tkinter.Button(
        composeFrame,
        image=send_image,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: sendMail(to_text.get(), subject_text.get(), mailBody.get('1.0', tkinter.END), filename=compose_attachment),
        relief="flat"
    )
    send_button.place(x=221, y=552, width=70, height=22)
    
def sendMail(recipient, subject, body, filename=None):
    try:
        backend.sendMail(recipient=recipient, subject=subject, body=body, filename=filename)
        messagebox.showinfo("Success", "Email sent successfully")
        showFrame()
    except Exception as e:
        messagebox.showinfo("Error", "Failed to send email")
    
def delete():
    selected_index = mailList.curselection()
    if not logged_in:
        messagebox.showinfo("Error", "You must login to delete a message.")
        return
    elif not selected_index:
        messagebox.showinfo("Error", "Please select an email to delete.")
        return
    
    index = int(selected_index[0])
    selected_mail = cached_inbox[index]
    
    backend.deleteEmail(selected_mail["UID"])  # Delete the email based on its UID
    showFrame()
    cached_inbox.pop(index)
    mailList.delete(index)
    messagebox.showinfo("Success", "Email deleted successfully.")

    setText(mailSender, "")
    setText(mailSubject, "")
    setText(mailBody, "")
    
def reply():
    global send_image, user_email
    selected_index = mailList.curselection()
    if not logged_in:
        messagebox.showinfo("Error", "You must login before you can reply to an email.")
        return
    elif not selected_index:   
        messagebox.showinfo("Error", "Please select an email to reply to.")
        return
    
    selected_mail = cached_inbox[selected_index[0]] 
    sender_email = selected_mail["Sender"] 
    
    emptyFrame = tkinter.Frame(root, width=510, height=578, bg="#FFFFFF")
    emptyFrame.place(x=468,y=63)
    
    from_label = tkinter.Label(emptyFrame, textvariable=tkinter.StringVar(value="From"), font=("Inter", 12 * -1), bg="#FFFFFF")
    from_label.place(x=12,y=12)
    from_text = tkinter.Entry(emptyFrame, font=("Inter", 12 * -1), bg="#FFFFFF", width=69, borderwidth=0, highlightthickness=1, highlightbackground="#DBDBDB")
    from_text.place(x=12,y=28)
    from_text.insert(0, user_email)
    
    to_label = tkinter.Label(emptyFrame, textvariable=tkinter.StringVar(value="To"), font=("Inter", 12 * -1), bg="#FFFFFF")
    to_label.place(x=12,y=48)
    to_text = tkinter.Entry(emptyFrame, font=("Inter", 12 * -1), bg="#FFFFFF", width=69, borderwidth=0, highlightthickness=1, highlightbackground="#DBDBDB")
    to_text.place(x=12,y=64)
    to_text.insert(0, selected_mail["Sender"])
    
    body_label = tkinter.Label(emptyFrame, textvariable=tkinter.StringVar(value="Reply"), font=("Inter", 12 * -1), bg="#FFFFFF")
    body_label.place(x=12,y=136)
    
    mailBody = tkinter.Text(emptyFrame, font=("Inter", 12 * -1), fg="black", borderwidth=0, highlightthickness=1, highlightbackground="#DBDBDB")
    mailBody.place(x=12, y=154, width=489,height=397)
    
    attach_button = tkinter.Button(emptyFrame, text="Attach", bg="#FFFFFF",borderwidth=.5,padx=0,pady=0,font=("Inter", 11 * -1), command=loadattachment)
    attach_button.configure(width=8)
    attach_button.place(x=445,y=131)
    
    send_image = tkinter.PhotoImage(file=relative_to_assets("send.png"))
    send_button = tkinter.Button(
        emptyFrame,
        image=send_image,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: send_reply(sender_email, mailBody.get("1.0", tkinter.END)),
        relief="flat"
    )
    send_button.place(x=221, y=552, width=70, height=22)
    
    
def send_reply(sender_email, reply_text, filename=None):
    selected_index = mailList.curselection()
    if not selected_index:
        messagebox.showinfo("Error", "Please select an email to reply to.")
        return
    
    selected_mail = cached_inbox[selected_index[0]]  # Get the selected email
    
    # Extract the recipient's email address from the "To" field
    recipient_email = sender_email
    
    # Send the reply using the backend
    backend.sendMail(recipient=recipient_email, subject="", body=reply_text, filename=filename)
    
    # Close the reply window after sending the reply
    messagebox.showinfo("Success", "Reply Sent.")

# Mailclient rectangle w/ buttons
buttonFrame = tkinter.Frame(root, width=138.0, height=640.0, bg="#25344C")
buttonFrame.place(x=0,y=0)
title_text = tkinter.Label(buttonFrame, textvariable=tkinter.StringVar(value="MailClient"), fg="#FFFFFF", bg="#25344C")
title_text.place(x=16, y=21, anchor="nw")
title_text.config(font=("Inter", 22 * -1))

# Inbox BUTTON
inbox_image = tkinter.PhotoImage(file=relative_to_assets("inbox.png"))
inbox_button = tkinter.Button(
    buttonFrame,
    image=inbox_image,
    borderwidth=0,
    highlightthickness=0,
    command=showInbox,
    relief="flat"
)
inbox_button.configure(bg="#25344C")
inbox_button.place(x=0, y=62, width=136, height=49)

# Compose BUTTON
compose_image = tkinter.PhotoImage(file=relative_to_assets("compose.png"))
compose_button = tkinter.Button(
    buttonFrame,
    image=compose_image,
    borderwidth=0,
    highlightthickness=0,
    command=compose,
    relief="flat"
)
compose_button.configure(bg="#25344C")
compose_button.place(x=0.0, y=113.0, width=136.0, height=49.0)

# Send BUTTON
sent_image = tkinter.PhotoImage(file=relative_to_assets("sent.png"))
sentInbox_button = tkinter.Button(
    buttonFrame,
    image=sent_image,
    borderwidth=0,
    highlightthickness=0,
    command=showSentInbox,
    relief="flat"
)
sentInbox_button.configure(bg="#25344C")
sentInbox_button.place(x=0.0, y=164.0, width=136.0, height=49.0)

delete_image = tkinter.PhotoImage(file=relative_to_assets("delete.png"))
delete_button = tkinter.Button(
    buttonFrame,
    image=delete_image,
    borderwidth=0,
    highlightthickness=0,
    command=delete,
    relief="flat"
)
delete_button.configure(bg="#25344C")
delete_button.place(x=0.0, y=215.0, width=136.0, height=49.0)

reply_image = tkinter.PhotoImage(file=relative_to_assets("reply.png"))
reply_button = tkinter.Button(
    buttonFrame,
    image=reply_image,
    borderwidth=0,
    highlightthickness=0,
    command=reply,
    relief="flat"
)
reply_button.configure(bg="#25344C")
reply_button.place(x=0.0, y=266.0, width=136.0, height=49.0)

login_image = tkinter.PhotoImage(file=relative_to_assets("login.png"))
logout_image = tkinter.PhotoImage(file=relative_to_assets("logout.png"))
account_button = tkinter.Button(
    buttonFrame,
    borderwidth=0,
    highlightthickness=0,
    command= showlogin,
    relief="flat"
)
account_button.configure(bg="#25344C")
account_button.place(x=0.0, y=589.0, width=136.0, height=37.0)
account_button.config(image=login_image)

root.mainloop()