from tkinter import*
from tkinter import filedialog as fd
from tkinter import ttk
import smtplib
import re
import pandas as pd

print("Program By: Skyler Guha")

#global variables
email_ids=None
your_email=None
session=None

def popup_box(msg):
    popup = Tk()
    popup.wm_title("Error!!")
    label = ttk.Label(popup, text=msg)
    label.pack(side="top", fill="x", pady=10)
    B1 = ttk.Button(popup, text="Okay", command = popup.destroy )
    B1.pack()

def cls_email(event):
    if(email_entry.get()=="Email"):
        email_entry.delete(0,END)
    if(pass_entry.get()==""):
        pass_entry.config(show="")
        pass_entry.insert (0,"Password")

def cls_pass(event):
    if(pass_entry.get()=="Password" and event!="cb"):
        pass_entry.delete(0,END)
    if(pass_checkvar.get()==0 and pass_entry.get()!="Password"):
        pass_entry.config(show="*")
    elif(pass_entry.get()!="Password"):
        pass_entry.config(show="")
    else:
        pass
    if(email_entry.get()=="" and event!="cb"):
        email_entry.insert (0,"Email")

def cls_recip(event):
    if(recipient_entry.get()=="Recipient"):recipient_entry.delete(0,END)
    if(content_entry.get("1.0", "end-1c")==""):content_entry.insert (INSERT,"Your Message Here")
    if(subject_entry.get()==""):subject_entry.insert (0,"Subject")

def cls_sub(event):
    if(subject_entry.get()=="Subject"):subject_entry.delete(0,END)
    if(content_entry.get("1.0", "end-1c")==""):content_entry.insert (INSERT,"Your Message Here")
    if(recipient_entry.get()==""):recipient_entry.insert (0,"Recipient")

def cls_con(event):
    if(content_entry.get("1.0", "end-1c")=="Your Message Here"):content_entry.delete("1.0", "end-1c")
    if(subject_entry.get()==""):subject_entry.insert (0,"Subject")
    if(recipient_entry.get()==""):recipient_entry.insert (0,"Recipient")

def email_valid(email):
    regex= re.compile(r"([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\"([]!#-[^-~ \t]|(\\[\t -~]))+\")@([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\[[\t -Z^-~]*])")
    if(re.fullmatch(regex,email)):
        return(True)
    else:
        return(False)

def log_to_writeup():
    global your_email
    global session
    try:
        your_email = email_entry.get()
        if(email_valid(your_email)==False):
            raise Exception("Invalid Email Address")

        # creates SMTP session
        session = smtplib.SMTP('smtp.gmail.com', 587)
        # start TLS for security
        session.starttls()
        # Authentication
        session.login(your_email, pass_entry.get())

        #gui cleaning stuff
        pass_entry.delete(0,END)
        pass_entry.config(show="")
        pass_entry.insert (0,"Password")
        email_entry.delete(0,END)
        email_entry.insert (0,"Email")

        log_panel.place_forget()
        writeup_panel.place(x=0,y=0)

    except Exception as x:
        try:
            session.quit()
        except Exception as y:
            pass
        print(x)

        if("Invalid Email Address" == str(x)):
            popup_box(str(x))
        else:
            popup_box("Could not login.\nHave you enabled 'Allow sending email via Less secure apps' for your email account?")
            popup_box(str(x))

def writeup_to_log():
    try:
        session.quit()
        recipient_entry.delete(0,END)
        subject_entry.delete(0,END)
        content_entry.delete("1.0", "end-1c")
        recipient_entry.insert (0,"Recipient")
        subject_entry.insert (0,"Subject")
        content_entry.insert (INSERT,"Your Message Here")
        writeup_panel.place_forget()
        log_panel.place(x=0,y=0)
    except Exception as x:
        pass

def import_CVS():
    global email_ids
    email_ids=None
    filename = fd.askopenfilename()
    if(filename[-4:].lower()!=".csv"):
        popup_box("wrong file type selected")
    else:
        email_ids=pd.read_csv(filename)
        email_ids = email_ids["email_ids"]

def recip_selector():
    if(recipient_checkvar.get()==0):
        CVS_button.place_forget()
        recipient_entry.place(x=50,y=50)
    else:
        recipient_entry.place_forget()
        CVS_button.place(x=50,y=50,height=20)

def send_mail():
    try:
        if(recipient_checkvar.get()==0):
            if(email_valid(recipient_entry.get())==False):
                popup_box("Please enter valid email")
            else:
                session.sendmail(your_email,recipient_entry.get(), """Subject:"""+subject_entry.get()+"""\n\n"""+content_entry.get("1.0", "end-1c"))
                popup_box("Email Sent Sucessfully!!")
        else:
            if(type(email_ids)==type(None)):
                    popup_box("Please select a CSV file")
            else:
                # sending the mail
                for address in email_ids.tolist():
                    session.sendmail(your_email, address, """Subject:"""+subject_entry.get()+"""\n\n"""+content_entry.get("1.0", "end-1c"))
                popup_box("Email Sent Sucessfully!!")
    except Exception as x:
        print (x)

def onclose():
    try:
        session.quit()
        popup_box("You have been looged out :)")
    except Exception:
        pass
    window.destroy()



window = Tk()
window.title("Email Sending Service")
window.protocol("WM_DELETE_WINDOW", lambda:onclose())
w=960
h=600
window.geometry("960x600")
window.resizable(width=False, height=False)

#panel defenations
log_panel = PanedWindow(window)
log_panel.configure(bg="#fac3db",width=w,height=h)
log_panel.place(x=0,y=0)

writeup_panel = PanedWindow(window)
writeup_panel.configure(bg="#fac3db",width=w,height=h)
#writeup_panel.place(x=0,y=0)

#log_panel
log_title_label = Label(log_panel, text="Welcome to Email Sending Service",font=("Courier", 25),bg="#9955bb",fg="white")
log_title_label.place(x=150,y=50)

log_content_panel= Frame(log_panel, height= 200, width=646,bg="#6b6090")
log_content_panel.place(x=150,y=160)

email_entry = Entry(log_panel, width=50, font=('Arial', 15))
email_entry.place(x=200,y=200)
email_entry.insert (0,"Email")
email_entry.bind("<Button-1>", cls_email)

pass_entry = Entry(log_panel, width=50, font=('Arial', 15))
pass_entry.place(x=200,y=250)
pass_entry.insert (0,"Password")
pass_entry.bind("<Button-1>", cls_pass)

pass_checkvar = IntVar()
pass_check =  Checkbutton(log_panel, text = "Show Password", variable = pass_checkvar,bg="#6b6090",fg="white",selectcolor="gray",command=lambda:cls_pass("cb"))
pass_check.place(x=200,y=300)


login_button = Button(log_panel,text="Login",font=('Arial', 20),command = lambda:log_to_writeup(),height = 1,width=30,bg="#ff1d8e",fg="white")
login_button.place(x=240,y=410)

exit_button = Button(log_panel,text="Exit",font=('Arial', 20),command = lambda:window.destroy(),height = 1,width=30,bg="#9955bb",fg="white")
exit_button.place(x=240,y=500)

#writeup_panel
CVS_button = Button(writeup_panel,text="Select CVS for column named 'email_ids'",command = lambda:import_CVS(),height = 1,width=85,bg="#ff1d8e",fg="white")
#CVS_button.place(x=675,y=50)

recipient_entry = Entry(writeup_panel,width=100)
recipient_entry.place(x=50,y=50,height=20)
recipient_entry.insert (0,"Recipient")
recipient_entry.bind("<Button-1>", cls_recip)

recipient_checkvar = IntVar()
recipient_check =  Checkbutton(writeup_panel, text = "Get recipient list from CVS", variable = recipient_checkvar,bg="#fac3db",fg="black",font=("Times New Roman",15),command=recip_selector)
recipient_check.place(x=680,y=45)

subject_entry = Entry(writeup_panel, width=140)
subject_entry.place(x=50,y=100)
subject_entry.insert (0,"Subject")
subject_entry.bind("<Button-1>", cls_sub)

content_entry = Text(writeup_panel, width=105,height=20)
content_entry.place(x=50,y=150)
content_entry.insert(INSERT,"Your Message Here")
content_entry.bind("<Button-1>", cls_con)

send_mail_button = Button(writeup_panel,text="Send Mail",command = lambda:send_mail(),height = 3,width=30,bg="#ff1d8e",fg="white")
send_mail_button.place(x=50,y=500)

logout_button = Button(writeup_panel,text="Logout",command = lambda:writeup_to_log(),height = 3,width=30,bg="#9955bb",fg="white")
logout_button.place(x=700,y=500)

window.mainloop()
