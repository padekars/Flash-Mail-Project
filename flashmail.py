import smtplib
import tkinter as tk
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import sqlite3
from tkinter import messagebox
from tkinter import filedialog as fd                                            # Browse
import csv
import time
import math
import matplotlib.pyplot as plt

conn = sqlite3.connect('smtp.db')
print ("Opened database successfully");

conn.execute('''CREATE TABLE IF NOT EXISTS text_db(SENDER TEXT, RECEIVER TEXT, TIME TEXT, DATE TEXT);''')
print ("Table text_db created successfully")

conn.execute('''CREATE TABLE IF NOT EXISTS image_db(SENDER TEXT, RECEIVER TEXT, TIME TEXT, DATE TEXT);''')
print ("Table image_db created successfully")

conn.execute('''CREATE TABLE IF NOT EXISTS msg_db(SENDER TEXT, RECEIVER TEXT, TIME TEXT, DATE TEXT);''')
print ("Table msg_db created successfully")

conn.execute('''CREATE TRIGGER IF NOT EXISTS validate_email_before_insert_text BEFORE INSERT ON text_db
                    BEGIN
                        SELECT CASE
                        WHEN NEW.SENDER NOT LIKE '%_@__%.__%' THEN
                        RAISE (ABORT, 'Invalid email address')
                    END;
                END;
            ''')

conn.execute('''CREATE TRIGGER IF NOT EXISTS validate_email_before_insert_image BEFORE INSERT ON image_db
                    BEGIN
                        SELECT CASE
                        WHEN NEW.SENDER NOT LIKE '%_@__%.__%' THEN
                        RAISE (ABORT, 'Invalid email address')
                    END;
                END;
            ''')

conn.execute('''CREATE TRIGGER IF NOT EXISTS validate_email_before_insert_msg BEFORE INSERT ON msg_db
                    BEGIN
                        SELECT CASE
                        WHEN NEW.SENDER NOT LIKE '%_@__%.__%' THEN
                        RAISE (ABORT, 'Invalid email address')
                    END;
                END;
            ''')

def empty(m, s1, p1, r):
    if len(s1.get())==0 or len(p1.get())==0 or len(r.get())==0:
        # hide main window
        top = tk.Toplevel()
        top.withdraw()
        # message box display
        messagebox.showerror("Error", "Make sure to enter all details!!!")

    else:
        menu(m, s1, p1, r)

def quit_(master):
    q = messagebox.askyesno("QUIT", "Do you want to exit the application???")
    if q > 0:
        master.destroy()
        return

def menu(m, s1, p1, r):
    top = tk.Toplevel()
    top.title("SMTP")
    top.configure(background="lightcyan")

    l1 = tk.Label(top, bg="lightcyan", text="FLASH MAIL", font = ("Cooper Black", 50), pady = 40)
    l1.pack(anchor = tk.CENTER)

    var = tk.IntVar()
    R1 = tk.Radiobutton(top, text = "ATTACHMENT",font=("Georgia",20),bg="lightcyan", variable = var, value = 1, command = lambda: sel(m, top, var, s1, p1, r))
    R1.pack(anchor = tk.W)
    R1.place(x=310,y=170)

    R3 = tk.Radiobutton(top, text = "MESSAGE",font=("Georgia",20), bg="lightcyan", variable = var, value = 2, command = lambda: sel(m, top, var, s1, p1, r))
    R3.pack(anchor = tk.W)
    R3.place(x=1100,y=170)

    b = tk.Button(top, bg="cyan", text='SEND',font=("Georgia", 15), command = lambda: unsel(m), padx = 30)
    b.place(x=700, y=650)
    top.mainloop()

def unsel(m):
    top = tk.Toplevel()
    top.withdraw()
    #m.withdraw()
    messagebox.showerror("Error", "ERROR: \n 1. Make sure to select an option!!! \n 2. Make sure you enter all the details!!!")

def sel1(m,top,var,s1,p1,r):
    if (var.get()==1):
        l = tk.Label(top, bg="lightcyan", text="Enter Subject", font = ("Georgia", 15))
        l.place(x=70, y=340)
        e1 = tk.Entry(top, width = 35)
        e1.place(x=270, y=345)

        l2 = tk.Label(top, bg="lightcyan", text="Enter body of mail", font = ("Georgia", 15))
        l2.place(x=70, y=400)
        e2 = tk.Entry(top, width =35)
        e2.place(x=270, y=405)

        l1 = tk.Label(top, bg="lightcyan", text="Enter file name", font = ("Georgia", 15))
        l1.place(x=70, y=460)
        e3 = tk.Entry(top, width =35)
        e3.place(x=270, y=465)

        l2 = tk.Label(top, bg="lightcyan", text="Enter file location", font = ("Georgia", 15))
        l2.place(x=70, y=520)
        e4 = tk.Entry(top, width =35)
        e4.place(x=270, y=525)

        def selectfile(m, top, s1, p1, r, e3):
            name = tk.StringVar(None)
            fileName = fd.askopenfilename(parent=top, title="Enter the file location")
            name.set(fileName)                                                  # Populate the text field with the selected file

            e4 = tk.Entry(top, width =35, textvariable=name)
            e4.place(x=270, y=525)

            b = tk.Button(top, bg="cyan", text='SEND',font=("Georgia", 15), command=lambda: file(m, top, s1, p1, r, e1, e2, e3, e4), padx = 30)
            b.place(x=700, y=650)


        bb = tk.Button(top, bg="cyan", text='BROWSE',font=("Georgia", 10), command = lambda: selectfile(m, top, s1, p1, r, e3))
        bb.place(x=270, y=570)

    else:                                                                       # IMAGE
        l = tk.Label(top, bg="lightcyan", text="Enter Subject", font = ("Georgia", 15))
        l.place(x=535, y=340)
        e1 = tk.Entry(top, width = 35)
        e1.place(x=785, y=345)

        l2 = tk.Label(top, bg="lightcyan", text="Enter body of mail", font = ("Georgia", 15))
        l2.place(x=535, y=400)
        e2 = tk.Entry(top, width =35)
        e2.place(x=785, y=405)

        l = tk.Label(top, bg="lightcyan", text="Enter image location", font = ("Georgia", 15))
        l.place(x=535, y=460)                                                   # Enter the image location
        e3 = tk.Entry(top, width = 35)
        e3.place(x=785, y=465)

        def selectfile(m, top, s1, p1, r):
            name = tk.StringVar(None)
            fileName = fd.askopenfilename(parent=top, title="Enter the image location")
            name.set(fileName)                                                  # Populate the text field with the selected file

            e3 = tk.Entry(top, width =35, textvariable=name)
            e3.place(x=785, y=465)

            b = tk.Button(top, bg="cyan", text='SEND',font=("Georgia", 15), command=lambda: image(m, top, s1, p1, r, e1, e2, e3), padx = 30)
            b.place(x=700, y=650)

        bb = tk.Button(top, bg="cyan", text='BROWSE',font=("Georgia", 10), command=lambda: selectfile(m, top, s1, p1, r))
        bb.place(x=785, y=510)


def sel(m, top, var, s1, p1, r):
    if (var.get() == 1):                                                        #ATTACHMENT

        var = tk.IntVar()
        R1 = tk.Radiobutton(top, text = "TEXTFILE",font=("Georgia",20),bg="lightcyan", variable = var, value = 1, command = lambda: sel1(m,top,var,s1,p1,r))
        R1.pack(anchor = tk.W)
        R1.place(x=100,y=250)

        R2 = tk.Radiobutton(top, text = "IMAGE",font=("Georgia",20), bg="lightcyan", variable = var, value = 2, command = lambda: sel1(m,top,var,s1,p1,r))
        R2.pack(anchor = tk.W )
        R2.place(x=555,y=250)

    elif (var.get() == 2):                                                      #MESSAGE

        l = tk.Label(top, bg="lightcyan", text="Enter Subject", font = ("Georgia", 15))
        l.place(x=1070, y=340)
        e1 = tk.Entry(top, width = 35)
        e1.place(x=1270, y=345)

        l1 = tk.Label(top, bg="lightcyan", text="Enter message", font = ("Georgia", 15))
        l1.place(x=1070, y=400)
        t = tk.Text(top, height=8, width=45)
        t.place(x=1070, y=465)

        b = tk.Button(top, bg="cyan", text='SEND',font=("Georgia", 15), command=lambda: message(m, top, s1, p1, r, e1, t), padx = 30)
        b.place(x=700, y=650)

def file(m, top, s1, p1, r, e1, e2, e3, e4):
    if len(e3.get())==0 or len(e4.get())==0:
        top1 = tk.Toplevel()
        top1.withdraw()
        
        messagebox.showerror("Error", "Make sure you enter all the details!!!")
    else:
        me = s1.get()
        pw = p1.get()
        you = r.get()

        td = time.strftime('%d-%m-%Y')
        dt = time.strftime('%H:%M:%S')

        conn.execute("INSERT INTO text_db (SENDER,RECEIVER, TIME, DATE) VALUES (?,?,?,?)",(s1.get(), r.get(), dt, td))
        conn.commit()

        row = [[me,you,dt,td]]
        with open(r'F:\SMTP_database.csv', 'a', newline='\n') as writeFile:
            writing = csv.writer(writeFile)
            writing.writerows(row)
        writeFile.close()

        msg = MIMEMultipart()                                                   # instance of MIMEMultipart

        msg['From'] = me                                                        # storing the senders email address
        msg['To'] = you                                                         # storing the receivers email address

        msg['Subject'] = e1.get()                                               # storing the subject
        body = e2.get()                                                         # string to store the body of the mail

        msg.attach(MIMEText(body, 'plain'))                                     # attach the body with the msg instance
        filename = e3.get()
        attachment = open(e4.get(), "rb")                                       # open the file to be sent

        p = MIMEBase('application', 'octet-stream')                             # instance of MIMEBase and named as p
        p.set_payload((attachment).read())                                      # To change the payload into encoded form
        encoders.encode_base64(p)                                               # encode into base64
        p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
        msg.attach(p)                                                           # attach the instance 'p' to instance 'msg'

        s = smtplib.SMTP('smtp.gmail.com', 587)                                 # creates SMTP session
        s.starttls()                                                            # start TLS for security
        s.login(me, pw)                                                         # Authentication
        s.sendmail(me, [you], msg.as_string())
        s.quit()                                                                # terminating the session

        top1 = tk.Toplevel()
        top1.withdraw()
        m.withdraw()
        messagebox.showinfo("SUCCESSFULL", "Mail has been successfully sent!!!")

def image(m, top, s1, p1, r, e1, e2, e3):
    if len(e3.get())==0:
        top1 = tk.Toplevel()
        top1.withdraw()
        m.withdraw()
        messagebox.showerror("Error", "Make sure you enter all the details!!!")
    else:
        me = s1.get()
        pw = p1.get()
        you = r.get()

        msg = MIMEMultipart()                                                   # instance of MIMEMultipart

        msg['From'] = me                                                        # storing the senders email address
        msg['To'] = you

        msg['Subject'] = e1.get()                                               # storing the subject
        body = e2.get()

        msg.attach(MIMEText(body, 'plain'))                                     # string to store the body of the mail

        td = time.strftime('%d-%m-%Y')
        dt = time.strftime('%H:%M:%S')

        conn.execute('''CREATE TABLE IF NOT EXISTS image_db(SENDER TEXT, RECEIVER TEXT, TIME NUMERIC, DATE);''')
        print ("Table image_db created successfully")

        conn.execute("INSERT INTO image_db (SENDER,RECEIVER, TIME, DATE)VALUES (?,?,?,?)",(s1.get(), r.get(), dt, td))
        conn.commit()

        row = [[me,you,dt,td]]
        with open(r'F:\SMTP_database.csv', 'a', newline='\n') as writeFile:
            writing = csv.writer(writeFile)
            writing.writerows(row)
        writeFile.close()

        conn.execute("INSERT INTO image_db (SENDER,RECEIVER, TIME, DATE)VALUES (?,?,?,?)",(s1.get(), r.get(), dt, td))
        conn.commit()
        conn.close()

        msg = MIMEMultipart()                                                   # Create the container (outer) email message.
        # Assume we know that the image files are all in PNG format
        fp = open(e3.get(), 'rb')
        img = MIMEImage(fp.read())
        fp.close()
        msg.attach(img)

        msg['Subject'] = e1.get()
        msg['From'] = me
        msg['To'] = you

        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login(me, pw)
        s.sendmail(me, [you], msg.as_string())
        s.quit()

        top1 = tk.Toplevel()
        top1.withdraw()
        m.withdraw()
        messagebox.showinfo("SUCCESSFULL", "Mail has been successfully sent!!!")

def message(m, top, s1, p1, r, e1, t):
    if len(t.get("1.0",'end-1c'))==0:
        top1 = tk.Toplevel()
        top1.withdraw()
        m.withdraw()
        messagebox.showerror("Error", "Make sure to enter all details!!!")
    else:
        msg = MIMEMultipart()
        body = t.get("1.0",'end-1c')                                            # string to store the body of the mail
        msg.attach(MIMEText(body, 'plain'))                                     # Create a text/plain message

        me = s1.get()                                                           # me == the sender's email address
        pw = p1.get()
        you = r.get()

        td = time.strftime('%d-%m-%Y')
        dt = time.strftime('%H:%M:%S')

        conn.execute('''CREATE TABLE IF NOT EXISTS msg_db(SENDER TEXT, RECEIVER TEXT, TIME NUMERIC, DATE);''')
        print ("Table msg_db created successfully")

        conn.execute("INSERT INTO msg_db (SENDER,RECEIVER, TIME, DATE)VALUES (?,?,?,?)",(s1.get(), r.get(), dt, td))
        conn.commit()

        row = [[me,you,dt,td]]
        with open(r'F:\SMTP_database.csv', 'a', newline='\n') as writeFile:
            writing = csv.writer(writeFile)
            writing.writerows(row)
        writeFile.close()

        msg['Subject'] = e1.get()
        msg['From'] = me
        msg['To'] = you

        s = smtplib.SMTP('smtp.gmail.com', 587)                                 # Send the message via our own SMTP server, but don't include the envelope header.
        s.starttls()
        s.login(me, pw)                                                         #smtp.login('fu@gmail.com', 'fu')
        s.sendmail(me, [you], msg.as_string())                                  #s.sendmail(me, 'dishashinde17@gmail.com', msg.as_string())
        s.quit()

        top1 = tk.Toplevel()
        top1.withdraw()
        m.withdraw()
        messagebox.showinfo("SUCCESSFULL", "Mail has been successfully sent!!!")

def monthly(top):

    l = tk.Label(top, bg="lightcyan", text="Enter the year (yyyy) : ", font = ("Georgia", 15))
    l.place(x=100, y=400)
    e = tk.Entry(top, width = 25)
    e.place(x=350, y=405)

    b = tk.Button(top, bg="cyan", text='ENTER', font = ("Georgia", 10), command = lambda: _pie())
    b.pack(side = "left", anchor = tk.CENTER)
    b.place(x=530, y=400)

    def _pie():
        f = e.get()
        if len(f) == 0 :
            top = tk.Toplevel()
            top.withdraw()
            messagebox.showerror("Error", "Make sure to enter the year!!!")

        else:
            data = []
            data1 = []
            w = []
            w1 = []
            count = 0
            flag = 0
            fh = open('F:\SMTP_database.csv', 'r')
            csv_reader = csv.reader(fh)

            for row in csv_reader:
                if flag == 0:
                    flag = 1
                    continue
                replacements = ('-', '/')
                for r in replacements:
                    row[3] = row[3].replace(r, ' ')
                    w = row[3].split()
                if w[2] == f:
                    w1.append(w[1])

            if w1 == []:
                top = tk.Toplevel()
                top.withdraw()
                messagebox.showerror("Error", "1. No mails sent in year" + str(f) + "!!!\nOR\n2. Check the entry format i.e. yyyy")

            else:
                test = w1[0]
                data.append(test)
                for v in w1:
                    if v == test:
                        count = count + 1
                    else:
                        test = v
                        data.append(v)
                        data1.append(count)
                        count = 1

                data1.append(count)
                
                fh.close()

                fig1,ax1 = plt.subplots()

                first_try={'01':"JAN",'02':"FEB",'03':"MAR",'04':"APR",'05':"MAY",'06':"JUN",'07':"JUL",'08':"AUG",'09':"SEP",'10':"OCT",'11':"NOV",'12':"DEC"}
                labels =[]

                for trial,value in first_try.items():
                    for i in data:
                        if i==trial:
                            labels.append(first_try[trial])

                ax1.pie(data1,explode=None,autopct='%1.1f%%', startangle=0)
                ax1.axis('equal')
                plt.legend(labels)
                plt.show()


def daily(top):

    l = tk.Label(top, bg="lightcyan", text="Enter date (dd/mm/yyyy) : ", font = ("Georgia", 15))
    l.place(x=100, y=300)
    e = tk.Entry(top, width = 25)
    e.place(x=350, y=305)

    b = tk.Button(top, bg="cyan", text='ENTER', font = ("Georgia", 10), command = lambda: _line())
    b.pack(side = "left", anchor = tk.CENTER)
    b.place(x=530, y=300)

    def _line():
        f = e.get()
        if len(f) == 0 :
            top = tk.Toplevel()
            top.withdraw()
            messagebox.showerror("Error", "Make sure to enter date!!!")
        else:
            data = []
            data1 = []
            w = []

            fh = open('F:\SMTP_database.csv', 'r')
            csv_reader = csv.reader(fh)

            for row in csv_reader:
                if row[3]==f:
                    w=row[2].split(':')
                    data.append(w[0])
            fh.close()
            
            data.sort()
            
            if data == []:
                top = tk.Toplevel()
                top.withdraw()
                messagebox.showerror("Error", "1. No mails sent on " + str(f) + "!!!\nOR\n2. Check the date format i.e. (dd/mm/yyyy)")

            else:
                flag=0
                k=[]
                count=1
                for i in data:
                    if flag==0:
                        test=i
                        flag=1
                        k.append(i)
                        continue
                    if test==i:
                        count=count+1
                    else:
                        k.append(i)
                        test=i
                        data1.append(count)
                        count=1
                data1.append(count)

                ax=plt.subplot(111)
                ax.set_title("Daily Analysis")
                
                yint = range(0, math.ceil(20)+1)

                plt.yticks(yint)

                ax.set_xlabel(f)
                plt.plot(k,data1,'go-', label='line 1', linewidth=2)

                plt.show()

def yearly():
    fh = open('F:\SMTP_database.csv', 'r')
    csv_reader = csv.reader(fh)

    k = {}
    need_to_split = []
    flag = 0
    year_count = 1
    final_count = []
    h = 0
    for row in csv_reader:
        if flag == 0:
            flag = 1
            continue
        if flag == 1:
            flag = 2
            replacements = ('-', '/')
            for r in replacements:
                row[3] = row[3].replace(r, ' ')
                need_to_split = row[3].split()
            want = need_to_split[2]
            k[h] = want
            year_count = 1
            continue

        replacements = ('-', '/')
        for r in replacements:
            row[3] = row[3].replace(r, ' ')
            need_to_split = row[3].split()

        if want == need_to_split[2]:
            year_count = year_count + 1
        else:
            h=h+1
            want=need_to_split[2]
            final_count.append(year_count)
            k[h] = want
            year_count = 1
    final_count.append(year_count)

    fh.close()

    fig, ax = plt.subplots()
    l = []
    l = list(k.values())
    plt.bar(l, final_count, align='center', alpha=0.8)                          # final plotting

    plt.xlabel('year')                                                          # naming the x-axis
    plt.ylabel('NUMBER OF MAILS')                                               # naming the y-axis
    plt.title('MAIL ANALYSIS')                                                  # plot title
    plt.tight_layout()
    plt.show()                                                                  # function to show the plot

def db(top, var, t):
    if (var.get() == 4):
        t.delete('1.0', tk.END)
        cursor = conn.execute("SELECT sender, receiver, time, date FROM text_db")
        for row in cursor:
            send = "SENDER = " + str(row[0]) + "\n"
            t.insert(tk.INSERT, send)
            recv = "RECEIVER = " + str(row[1]) + "\n"
            t.insert(tk.INSERT, recv)
            time1 = "TIME = " + str(row[2]) + "\n"
            t.insert(tk.INSERT, time1)
            date1 = "DATE = " + str(row[3]) + "\n\n"
            t.insert(tk.INSERT, date1)

    elif (var.get() == 5):
        t.delete('1.0', tk.END)
        out = conn.execute("SELECT COUNT(*) FROM image_db")
        data = out.fetchone()
        t.insert(tk.INSERT, data[0])

    elif (var.get() == 6):
        t.delete('1.0', tk.END)
        td = time.strftime('%d-%m-%Y')
        out1 = conn.execute("SELECT COUNT(*) FROM text_db WHERE DATE = ?", (td,))
        out2 = conn.execute("SELECT COUNT(*) FROM image_db WHERE DATE = ?", (td,))
        out3 = conn.execute("SELECT COUNT(*) FROM msg_db WHERE DATE = ?", (td,))
        data = out1.fetchone()
        data1 = out2.fetchone()
        data2 = out3.fetchone()
        datafinal = int(data[0])+int(data1[0])+int(data2[0])
        t.insert(tk.INSERT, datafinal)

    elif (var.get() == 7):
        t.delete('1.0', tk.END)
        td1 = time.strftime('%d-%m-%Y')
        w1 = []
        replacements = ('-', '/')
        for r in replacements:
            td1 = td1.replace(r, ' ')
            w1 = td1.split()
        td1 = w1[1]
        out1 = conn.execute("SELECT COUNT(*) FROM text_db WHERE DATE LIKE ?", ('%'+td1+'%',))
        out2 = conn.execute("SELECT COUNT(*) FROM image_db WHERE DATE LIKE ?", ('%'+td1+'%',))
        out3 = conn.execute("SELECT COUNT(*) FROM msg_db WHERE DATE LIKE ?", ('%'+td1+'%',))
        data = out1.fetchone()
        data1 = out2.fetchone()
        data2 = out3.fetchone()
        print(data,data1,data2)
        datafinal = int(data[0])+int(data1[0])+int(data2[0])
        print(datafinal)
        t.insert(tk.INSERT, datafinal)

    else:
        t.delete('1.0', tk.END)
        td2 = time.strftime('%d-%m-%Y')
        w2 = []
        replacements = ('-', '/')
        for r in replacements:
            td2 = td2.replace(r, ' ')
            w2 = td2.split()
        td2 = w2[2]
        out1 = conn.execute("SELECT COUNT(*) FROM text_db WHERE DATE LIKE ?", ('%'+td2,))
        out2 = conn.execute("SELECT COUNT(*) FROM image_db WHERE DATE LIKE ?", ('%'+td2,))
        out3 = conn.execute("SELECT COUNT(*) FROM msg_db WHERE DATE LIKE ?", ('%'+td2,))
        data = out1.fetchone()
        data1 = out2.fetchone()
        data2 = out3.fetchone()
        datafinal = int(data[0])+int(data1[0])+int(data2[0])
        t.insert(tk.INSERT, str(datafinal))


def sdl():
    top = tk.Toplevel()
    top.title("FLASH MAIL")
    top.configure(background="lightcyan")

    l = tk.Label(top, bg="lightcyan", text="FLASH MAIL", font = ("Cooper Black", 50), pady = 40)
    l.pack(anchor = tk.CENTER)

    l1 = tk.Label(top, bg="lightcyan", text="GRAPHICAL ANALYSIS", font = ("Georgia",25), pady = 40)
    l1.place(x=150, y=150)

    var = tk.IntVar()
    R1 = tk.Radiobutton(top, text = "DAILY",font=("Georgia",15),bg="lightcyan", variable = var, value = 1, command = lambda: daily(top))
    R1.pack(anchor = tk.W)
    R1.place(x=100,y=250)

    R2 = tk.Radiobutton(top, text = "MONTHLY",font=("Georgia",15), bg="lightcyan", variable = var, value = 2, command = lambda: monthly(top))
    R2.pack(anchor = tk.W )
    R2.place(x=100,y=350)

    R3 = tk.Radiobutton(top, text = "YEARLY",font=("Georgia",15), bg="lightcyan", variable = var, value = 3, command = yearly)
    R3.pack(anchor = tk.W)
    R3.place(x=100,y=450)

    l2 = tk.Label(top, bg="lightcyan", text="DATABASE ANALYSIS", font = ("Georgia",25), pady = 40)
    l2.place(x=1000, y=150)

    l2 = tk.Label(top, bg="lightcyan", text="OUTPUT", font = ("Georgia", 12))
    l2.place(x=950, y=540)
    t = tk.Text(top, height=10, width=60)
    t.place(x=950, y=580)

    R4 = tk.Radiobutton(top, text = "DETAILS OF TEXTFILE MAILS SENT",font=("Georgia",15),bg="lightcyan", variable = var, value = 4, command = lambda: db(top, var, t))
    R4.pack(anchor = tk.W)
    R4.place(x=950,y=280)

    R5 = tk.Radiobutton(top, text = "NUMBER OF IMAGE MAILS SENT",font=("Georgia",15), bg="lightcyan", variable = var, value = 5, command = lambda: db(top, var, t))
    R5.pack(anchor = tk.W )
    R5.place(x=950,y=330)

    R6 = tk.Radiobutton(top, text = "NUMBER OF MAILS SENT TODAY",font=("Georgia",15), bg="lightcyan", variable = var, value = 6, command = lambda: db(top, var, t))
    R6.pack(anchor = tk.W)
    R6.place(x=950,y=380)

    R7 = tk.Radiobutton(top, text = "NUMBER OF MAILS SENT IN THIS MONTH",font=("Georgia",15),bg="lightcyan", variable = var, value = 7, command = lambda: db(top, var, t))
    R7.pack(anchor = tk.W)
    R7.place(x=950,y=430)

    R8 = tk.Radiobutton(top, text = "NUMBER OF MAILS SENT IN THIS YEAR",font=("Georgia",15), bg="lightcyan", variable = var, value = 8, command = lambda: db(top, var, t))
    R8.pack(anchor = tk.W )
    R8.place(x=950,y=480)

    top.mainloop()

def GUI():
    master = tk.Tk()
    master.title("FLASH MAIL")
    master.configure(background="lightcyan")

    l1 = tk.Label(master, bg="lightcyan", text="FLASH MAIL", font = ("Cooper Black", 50), pady = 40)
    l1.pack(anchor = tk.CENTER)

    C1 = tk.Canvas(master, bg = "black", height = 6, width = 500)
    C1.pack()
    C2 = tk.Canvas(master, bg = "black", height = 490, width = 6)
    C2.place(x=510,y=169)

    C3 = tk.Canvas(master, bg = "black", height = 490, width = 6)
    C3.place(x=1016,y=169)
    C4 = tk.Canvas(master, bg = "black", height = 6, width = 500)
    C4.place(x = 516, y = 661)

    l2 = tk.Label(master, bg="lightcyan", text="SENDER'S DETAILS", font = ("Georgia", 20))
    l2.place(x=637, y=220)
    l3 = tk.Label(master, bg="lightcyan", text="E-MAIL ID", font = ("Georgia", 10))
    l3.place(x=622, y=300)
    e1 = tk.Entry(master, width = 35)
    e1.place(x=720, y=300)

    l4 = tk.Label(master, bg="lightcyan", text="PASSWORD", font = ("Georgia", 10))
    l4.place(x=620, y=330)
    e2 = tk.Entry(master, show = '*', width = 35)
    e2.place(x=720, y=330)

    def if_admin():
        
        f = tk.Frame(master, width=350, height=150, bg="lightcyan")
        f.place(x=610, y=470)
        
        l = tk.Label(master, bg="lightcyan", text="PASSWORD", font = ("Georgia", 10))
        l.place(x=620, y=480)
        e = tk.Entry(master, show = '*', width = 35)
        e.place(x=720, y=480)

        b = tk.Button(master, bg = "cyan", text='ANALYSIS', font=("Georgia",15), command = lambda : check(e), padx = 10)
        b.place(x=820, y=560)

        b1 = tk.Button(master, bg="cyan", text='QUIT', font = "Georgia", command = lambda: quit_(master))
        b1.pack(side = "left", anchor = tk.CENTER)
        b1.place(x=610, y=560)

    def if_user():
        
        f1 = tk.Frame(master, width=350, height=150, bg="lightcyan")
        f1.place(x=610, y=470)
        
        l5 = tk.Label(master, bg="lightcyan", text="RECEIVER'S DETAILS", font = ("Georgia", 20))
        l5.pack(anchor = tk.CENTER)
        l5.place(x=637, y=475)
        l6 = tk.Label(master, bg="lightcyan", text="E-MAIL ID", font = ("Georgia", 10))
        l6.place(x=622, y=525)
        e3 = tk.Entry(master, width = 35)
        e3.place(x=720, y=525)
        b2 = tk.Button(master, bg="cyan", text='LOGIN', font = "Georgia", command = lambda: empty(master, e1, e2, e3))
        b2.pack(side = "left", anchor = tk.CENTER)
        b2.place(x=850, y=560)
        b1 = tk.Button(master, bg="cyan", text='QUIT', font = "Georgia", command = lambda: quit_(master))
        b1.pack(side = "left", anchor = tk.CENTER)
        b1.place(x=610, y=560)

    b3 = tk.Button(master, bg="cyan", text='USER', font = "Georgia", command = if_user)
    b3.pack(side = "left", anchor = tk.CENTER)
    b3.place(x=610, y=400)

    b4 = tk.Button(master, bg="cyan", text='ADMIN', font = "Georgia", command = if_admin)
    b4.pack(side = "left", anchor = tk.CENTER)
    b4.place(x=850, y=400)

    def check(e):
        if e.get() == "12345":
            sdl()
        else:
            top = tk.Toplevel()
            top.withdraw()
            messagebox.showerror("Error", "Wrong password.....Try again!!!!")

GUI()
tk.mainloop( )
