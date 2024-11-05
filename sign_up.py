from tkinter import *
import tkinter as tk
import subprocess
import sqlite3
import tkinter.messagebox as message
from PIL import Image, ImageTk

conn = sqlite3.connect('signup.db')
cur = conn.cursor()
cur.execute(''' CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY AUTOINCREMENT, username VARCHAR (50), email VARCHAR (10), password VARCHAR(10), confirm VARCHAR (15))''')


def sign_up():
    username = username_entry.get()
    email = email_entry.get()
    password = password_ent.get()
    confirm = con_password_ent.get()

    if username == "" or email == "" or password == "" or confirm == "":
        message.showinfo("Prompt", "Empty record is not allowed, please fill the form properly")
        return
    elif not password == confirm:
        message.showinfo("Prompt", "Please check your password correctly")
        return

    conn = sqlite3.connect('signup.db')
    cur = conn.cursor()

    cur.execute("SELECT * FROM users WHERE username = ? OR email = ?", (username, email))
    existing_user = cur.fetchone()

    if existing_user:
        message.showerror("Error", "Username or email already exists. Please use a different one.")
        conn.close()
        return


    try:
        cur.execute(''' INSERT INTO users(username, email, password, confirm) VALUES(?,?,?,?)''', 
                    (username, email, password, confirm))
        conn.commit()
        username_entry.delete(0, END)
        email_entry.delete(0, END)
        password_ent.delete(0, END)
        con_password_ent.delete(0, END)
        
        message.showinfo("PROMPT", "Record Successfully Signed Up")
        sign_in()
    except sqlite3.IntegrityError:
        message.showerror("Error", "An error occurred while signing up.")
    finally:
        conn.close()


def sign_in():
    subprocess.Popen(["python", "sign_in.py"])
    root.destroy()
    



root = Tk()
root.title("Ai chatbot")
root.geometry('1100x500+500+200')
root.resizable(0,0)
root.config(bg="white")

# left frame
left_frame=Frame(root, width=500, height=1000, bg="white")
spath="images/ai_1.jpg"
simg=ImageTk.PhotoImage(Image.open(spath))
img=Label(left_frame,image=simg)
img.image=simg
img.place(x=0, y=0, relwidth=1, relheight=1)

left_frame.pack(side="left")

# right frame 
right_frame =Frame(root, width=600, height=1000, bg="#011627")

header_label = Label(right_frame, text="Sign up", font=("Arial", 20, "bold"), fg="white", bg="#011627")
header_label.place(x=250, y=30)

username_label = Label(right_frame, text="Username:", font=("Arial", 12, "bold"), fg="white", bg="#011627")
username_label.place(x=40, y=100)
username_entry = Entry(right_frame, width=40, font=("Arial", 12), bg="#EFEFEF")
username_entry.place(x=200, y=100)

email_label = Label(right_frame, text="Email:", font=("Arial", 12, "bold"), fg="white", bg="#011627")
email_label.place(x=40, y=150)
email_entry = Entry(right_frame, width=40, font=("Arial", 12), bg="#EFEFEF")
email_entry.place(x=200, y=150)

password_lbl = Label(right_frame, text="Password: ", font=("Arial", 12, "bold"), fg="white", bg="#011627")
password_lbl.place(x=40, y=200)
password_ent = Entry(right_frame, width=40, font=("Arial", 12), bg="#EFEFEF")
password_ent.place(x=200, y=200)

con_password_lbl = Label(right_frame, text="Confirm password:", font=("Arial", 12, "bold"), fg="white", bg="#011627")
con_password_lbl.place(x=40, y=250)
con_password_ent = Entry(right_frame, width=40, font=("Arial", 12), bg="#EFEFEF")
con_password_ent.place(x=200, y=250)

signup_button = Button(right_frame, text="Sign Up", font=("Arial", 12, "bold"), fg="white", bg="#15b097", command=sign_up)
signup_button.place(x=310, y=300)

signup_button = Button(right_frame, text="Already registered! sign-in", font=("Arial", 12, "bold"), fg="white", bg="gray", command=sign_in)
signup_button.place(x=240, y=350)
right_frame.pack(side="right")
root.mainloop()
