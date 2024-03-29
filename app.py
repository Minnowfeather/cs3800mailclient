import tkinter
from tkinter import ttk, font
import mailbackend

# init window
root = tkinter.Tk()
root.title("Mail Client")
root.resizable(False, False)

mailList = tkinter.Listbox(root)
mailList.grid(rowspan=15,column=1, sticky="nw")

mailBodyFrame = tkinter.Frame(root, height=200, width=200)
mailBodyFrame.grid(row=0, column=2)
mailBodyFrame.columnconfigure(0, weight=10)
mailBodyFrame.pack_propagate(False)

mailBodyText = tkinter.StringVar()
mailBodyLabel = tkinter.Label(mailBodyFrame, textvariable=mailBodyText)
mailBodyLabel.place(relx=0, rely=0, anchor="w")
mailBodyLabel.configure(font=("Arial",50))

def showinbox():
    global mailList
    mailList.delete('0','end')
    mailBodyText.set("")
    i = 0
    for mail in mailbackend.getInbox():
        i = i + 1
        mailList.insert(i, mail["subject"])
def showtrash():
    print("wawa")


def onselect(evt):
    global mailBodyText
    w = evt.widget
    index = int(w.curselection()[0])
    mailSubject = w.get(index)
    mailBodyText.set("")
    for mail in mailbackend.getInbox():
        if mail["subject"] == mailSubject:
            mailBodyText.set(mail["body"])
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
    child.grid_configure(padx=2, pady=2)

showinbox()
# run
root.mainloop()
