from tkinter import Tk, Label, Entry, Button

def submit():
    username = uname_entry.get()
    uid = uid_entry.get()
    hash = hash_entry.get()
    root.destroy()
    return username, uid, hash

root = Tk()

uname_label = Label(root, text="Username:")
uname_label.pack()

uname_entry = Entry(root)
uname_entry.pack()

uid_label = Label(root, text="UID:")
uid_label.pack()

uid_entry = Entry(root)
uid_entry.pack()

hash_label = Label(root, text="Hash:")
hash_label.pack()

hash_entry = Entry(root, show="*")
hash_entry.pack()

submit_button = Button(root, text="Submit", command=submit)
submit_button.pack()

root.mainloop()
