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

# init window
root = tkinter.Tk()
root.title("Mail Client")
root.resizable(False, False)
# declare the default font 
DEFAULT_FONT = tkinter.font.nametofont("TkDefaultFont")

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
    global mailList
    mailList.delete('0','end')
    
    setText(mailSender, "")
    setText(mailSubject, "")
    setText(mailBody, "")
    i = 0
    for mail in mailbackend.getInbox():
        i = i + 1
        mailList.insert(i, mail["subject"])
def showtrash():
    print("wawa")


def onselect(evt):
    global mailBodyText
    w = evt.widget
    if len(w.curselection()) < 1:
        return
    index = int(w.curselection()[0])
    tmpSubject = w.get(index)
    for mail in mailbackend.getInbox():
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
# pad each child in root 
for child in root.winfo_children():
    child.grid_configure(padx=2, pady=0)

showinbox()
# run
root.mainloop()
