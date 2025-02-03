import tkinter as tk

import tkinter.messagebox

import cryptography.fernet

import st_sqlite_manager
import SarpTechCrypto as stc
from crypto_note import CryptoNote

def saveAndEncrypt():
    master_key = entryMasterKey.get().strip()
    content = textContent.get(1.0, tk.END).strip()
    title = entryTitle.get().strip()

    if master_key != "" and content != "" and title != "":
        encrypted_content = stc.encrypt(content, stc.generate_key(master_key))

        note_object = CryptoNote(title, encrypted_content)
        st_sqlite_manager.createNote(note_object)

        tk.messagebox.showinfo("Success", "Note saved successfully")
        getAll()
        clearContent()
    else:
        tk.messagebox.showerror("Error","Please enter a master key, content and title")

def decrypt():
    master_key = entryMasterKey.get().strip()
    global selectedTitle
    if master_key != "" and selectedTitle != None:
        object: CryptoNote = st_sqlite_manager.get_note_by_id(selectedTitle).pop()

        try:
            note = stc.decrypt(object.content, stc.generate_key(master_key))
            textContent.delete(1.0, tk.END)
            textContent.insert(tk.END, note)
            entryTitle.delete(0, tk.END)
            entryTitle.insert(0, object.title)
        except cryptography.fernet.InvalidToken:
            tk.messagebox.showerror("Error","Invalid Master Key")

    else:
        tk.messagebox.showerror("Error","Please select an item and enter a master key")

def updateNote():
    global selectedTitle
    deleteNote()
    saveAndEncrypt()

def deleteNote():
    global selectedTitle
    st_sqlite_manager.delete_note_by_id(selectedTitle)
    getAll()

def clearContent():
    textContent.delete(1.0,tk.END)
    entryTitle.delete(0,tk.END)
    entryMasterKey.delete(0,tk.END)
    global selectedTitle
    selectedTitle = ""
    listBox.selection_clear(0,tk.END)

def selectListBox(event):
    global selectedTitle
    selectedTitle = listBox.get(listBox.curselection()).strip()

def getAll():
    listBox.delete(0, tk.END)
    listx = st_sqlite_manager.get_all_notes()
    for (i, x) in enumerate(listx):
        listBox.insert(i, x.title)

getAll()

selectedTitle = ""

window = tk.Tk()
window.title("Enhanced Crypto Notes")
window.wm_minsize(width=500, height=800)

img = tk.PhotoImage(file="eth.png")

labelImage = tk.Label(window, image=img)
labelImage.pack()

label = tk.Label(window, text="Welcome to Enhanced Crypto Notes", font=("Arial",24,"bold"))
label.pack()

labelTitle = tk.Label(window, text="Title")
labelTitle.pack()

entryTitle = tk.Entry(window)
entryTitle.pack()

labelContent = tk.Label(window, text="Content")
labelContent.pack()
textContent = tk.Text(window, height=10, width=50)
textContent.pack()

labelMasterKey = tk.Label(window, text="Master Key")
labelMasterKey.pack()

entryMasterKey = tk.Entry(window)
entryMasterKey.pack()

listBox = tk.Listbox(window, height=10, width=40)
listBox.pack()

listBox.bind('<<ListboxSelect>>',selectListBox)

butEncrypt = tk.Button(text="Save & Encrypt", command=saveAndEncrypt)
butEncrypt.pack()
butDecrypt = tk.Button(text="Decrypt", command=decrypt)
butDecrypt.pack()
butUpdate = tk.Button(text="Update Note", command=updateNote)
butUpdate.pack()
butDelete = tk.Button(text="Delete Note", command=deleteNote)
butDelete.pack()
butClear = tk.Button(text="Clear", command=clearContent)
butClear.pack()

window.mainloop()