from tkinter import *
from tkinter import ttk, messagebox
import sqlite3

db = sqlite3.connect("contacts.db")
cursor = db.cursor()
# cursor.execute("CREATE TABLE contacts(Contactname VARCHAR(100), gender VARCHAR(10), email VARCHAR(50), "
#                "phoneno NUMBER(15) PRIMARY KEY)")


def add_contact():
    name = contact_name.get()
    number = telephone.get()
    email = email_entry.get()
    gender = gender_entry.get()
    if name == "" or number == "" or email == "" or gender == "":
        messagebox.showwarning(title="Error", message="Enter all the details.")
        return 0
    if len(number) != 10:
        messagebox.showwarning(title="Error", message="Enter a valid ten digit number.")
        return 0
    if '@' not in email:
        messagebox.showwarning(title="Error", message="Enter a valid email.")
        return 0
    params = (name, gender, email, number)
    cursor.execute("INSERT INTO contacts VALUES(?, ?, ?, ?)", params)
    db.commit()
    messagebox.showinfo(title="Successful", message="Contact saved successfully.")
    contact_name.delete(0, END)
    telephone.delete(0, END)
    email_entry.delete(0, END)
    gender_entry.set("")


def search():
    name_to_search = search_entry.get()
    if name_to_search == "":
        messagebox.showwarning(title="Error", message="Enter the name to be searched.")
    name = (name_to_search,)
    data = cursor.execute(f"SELECT * FROM contacts WHERE contacts.Contactname == (?)", name)
    for row in data:
        contact_name.insert(0, row[0])
        gender_entry.set(row[1])
        email_entry.insert(0, row[2])
        telephone.insert(0, row[3])
    if contact_name.get() == "":
        messagebox.showwarning(title="Error", message="Contact does not exist.")
        search_entry.delete(0, END)


def delete():
    num = telephone.get()
    if num == "":
        messagebox.showwarning(title="Error", message="Please search the contact before deleting")
        return 0
    num = (num,)
    cursor.execute("DELETE FROM contacts WHERE phoneno == (?)", num)
    db.commit()
    contact_name.delete(0, END)
    telephone.delete(0, END)
    email_entry.delete(0, END)
    gender_entry.set("")
    messagebox.showinfo(title="Successful", message="Contact deleted successfully.")


def update():
    name = contact_name.get()
    phone = telephone.get()
    phone_condition = phone
    gender = gender_entry.get()
    email = email_entry.get()
    if name == "":
        messagebox.showwarning(title="Error", message="Please update the contact before deleting")
        return 0
    param = (name, gender, email, phone_condition)
    param2 = (phone, email)
    cursor.execute("UPDATE contacts SET Contactname = (?), gender = (?), email = (?) WHERE phoneno = (?)", param)
    cursor.execute("UPDATE contacts SET phoneno = (?) WHERE email = (?)", param2)
    db.commit()
    contact_name.delete(0, END)
    telephone.delete(0, END)
    email_entry.delete(0, END)
    gender_entry.set("")
    messagebox.showinfo(title="Successful", message="Contact updated successfully.")


def show_all():
    window2 = Tk()
    window2.geometry("400x400+20+20")
    window2.resizable(False, False)
    window2.title("All Contacts")
    data = cursor.execute("SELECT * FROM contacts")
    i = 0  # row value inside the loop
    for student in data:
        for j in range(len(student)):
            e = Entry(window2, width=10, fg='blue')
            e.grid(row=i, column=j)
            e.insert(END, student[j])
        i = i + 1


window = Tk()
window.geometry("500x250+20+20")
window.resizable(False, False)
window.title("Phonebook")
frame = Frame(window, height=50, width=500, bg="mediumblue")
frame.grid(row=0, column=0, columnspan=4)
label = Label(frame, compound=TOP, text="Phonebook", font='Verdana 17 bold', fg="white", bg="mediumblue")
label.place(x=5, y=5)
name_label = Label(text="Name: ")
contact_name = Entry(width=23)
name_label.grid(row=1, column=0)
contact_name.grid(row=1, column=1)
gender_label = Label(text="Gender: ")
gender_entry = StringVar()
gender_combobox = ttk.Combobox(textvariable=gender_entry, values=["", "F", "M"])
gender_label.grid(row=2, column=0)
gender_combobox.grid(row=2, column=1)
add_button = Button(text="Add", bg="mediumblue", fg="white", width=10, highlightthickness=0, command=add_contact)
add_button.grid(row=1, column=3)
telephone_label = Label(text="Telephone: ")
telephone = Entry(width=23)
telephone_label.grid(row=3, column=0)
telephone.grid(row=3, column=1)
update_button = Button(text="Update", bg="mediumblue", fg="white", width=10, highlightthickness=0, command=update)
update_button.grid(row=2, column=3)
email_label = Label(text="Email: ")
email_entry = Entry(width=23)
email_label.grid(row=4, column=0)
email_entry.grid(row=4, column=1)
delete_button = Button(text="Delete", bg="mediumblue", fg="white", width=10, highlightthickness=0, command=delete)
delete_button.grid(row=3, column=3)
search_label = Label(text="Enter name to search:")
search_label.grid(row=6, column=0)
search_button = Button(text="Search", bg="mediumblue", fg="white", width=10, highlightthickness=0, command=search)
search_entry = Entry(width=23)
search_button.grid(row=6, column=2)
search_entry.grid(row=6, column=1)
all_button = Button(text="Show all contacts", bg="mediumblue", fg="white", width=20, command=show_all, highlightthickness=0)
all_button.grid(row=5, column=0, columnspan=2)
window.mainloop()



