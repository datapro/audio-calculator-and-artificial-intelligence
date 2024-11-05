import tkinter as tk
from tkinter import *
import subprocess
import sqlite3
import tkinter.messagebox as message
from PIL import Image, ImageTk


def sign_in():
    email=email_entry.get()
    password=password_ent.get()

    if email=="" and password=="":
        message.showinfo("Prompt","Empty record is not allowed, please fill the form properly")
        return
    conn=sqlite3.connect('signup.db')
    cur=conn.cursor()
    cur.execute(''' select * from users WHERE email=? AND password=? ''', (email,password))
    result=cur.fetchone()
    if result:
        message.showinfo("Prompt","Login Successful")
        email_entry.delete(0, END)
        password_ent.delete(0, END)
        conn.close()
        subprocess.Popen(["python", "Ai_chatbot.py"])
        root.destroy()
    else:
        message.showinfo("Alert", "UNAUTHORIZED ACCESS")

root = Tk()
root.title("Sign-in form")
root.geometry('1100x500+500+200')
root.resizable(0,0)
root.config(bg="white")

# left frame
left_frame=Frame(root, width=500, height=1000, bg="white")
spath="images/robot_1.jpg"
simg=ImageTk.PhotoImage(Image.open(spath))
img=Label(left_frame,image=simg)
img.image=simg
img.place(x=0, y=0, relwidth=1, relheight=1)

left_frame.pack(side="left")
# right frame
right_frame=Frame(root, width=600, height=1000, bg="#011627")
header_label = Label(right_frame, text="Sign in", font=("Arial", 30, "bold"), fg="white", bg="#011627")
header_label.place(x=250, y=30)


email_label = Label(right_frame, text="Email:", font=("Arial", 12, "bold"), fg="white", bg="#011627")
email_label.place(x=80, y=120)
email_entry = Entry(right_frame, width=40, font=("Arial", 12),bg="#EFEFEF")
email_entry.place(x=190, y=120)

password_lbl = Label(right_frame, text="Password:", font=("Arial", 12, "bold"), fg="white", bg="#011627")
password_lbl.place(x=80, y=170)
password_ent = Entry(right_frame, width=40, font=("Arial", 12), bg="#EFEFEF")
password_ent.place(x=190, y=170)

signin_button = Button(right_frame, text="Sign In", font=("Arial", 12, "bold"), fg="white", bg="#15b097", width=10, height=1, relief=GROOVE, command=sign_in)
signin_button.place(x=250, y=230)
right_frame.pack(side="right")


root.mainloop()
