import smtplib
import sqlite3
import ssl
from tkinter import END, messagebox

from Database.DomainCountFunction import countDomain
from configuration.encDecFile import EncryptPass


def checkPasswordShow(window):
            if window.check_pass_var.get() == "Show":
                window.PasswordInput.configure(show="")
            else:
                window.PasswordInput.configure(show="*")

def displayquery(window):
        con=sqlite3.connect('Database/system.db')
        cur=con.cursor()
        cur.execute("select rowid,* from DomainDetails")
        records = cur.fetchall()
        con.commit()
        con.close()
        global count
        count = 0

        for record in records:
            window.my_tree.insert(parent='', index='end', iid=count, text='', values=(record[0],record[1], record[3], record[4]), tags=('row',))
            count += 1

def addRecord(window,mainWindow):
        if len(window.my_tree.selection()) == 0:
            username = window.UsernameInput.get()
            password = window.PasswordInput.get()
            outgoingServer = window.OutgoingServerInput.get()
            port = window.PortInput.get()

            global counter
            counter = 0
            con=sqlite3.connect('Database/system.db')
            cur=con.cursor()
            cur.execute("select username from DomainDetails")
            records = cur.fetchall()
            for record in records:
                if record[0] == username:
                    print(record[0])
                    counter=1
                else:
                    pass
            con.commit()
            con.close()
            if counter == 0:
                if(username!='' and password!='' and outgoingServer!='' and port != ""):
                    MsgBox = messagebox.askquestion('Add Record', 'Are you sure you want to Add the record?')
                    if MsgBox == 'yes':
                        try:
                            smtpObj = smtplib.SMTP(host=outgoingServer,port=port)
                            context=ssl.create_default_context()
                            smtpObj.connect(outgoingServer,port)
                            smtpObj.starttls(context=context)
                            smtpObj.login(username,password)
                            con=sqlite3.connect('Database/system.db')
                            cur=con.cursor()
                            cur.execute("INSERT INTO DomainDetails VALUES(:user,:pass,:server,:port)",
                                {
                                    'user':username,
                                    'pass':EncryptPass(password),
                                    'server':outgoingServer,
                                    'port':port,
                                }
                            )
                            con.commit()
                            con.close()
                            window.UsernameInput.delete(0,END)
                            window.PasswordInput.delete(0,END)
                            window.OutgoingServerInput.delete(0,END)
                            window.PortInput.delete(0,END)

                            window.my_tree.delete(*window.my_tree.get_children())
                            displayquery(window)
                            countDomain(mainWindow)
                        except smtplib.SMTPAuthenticationError:
                            messagebox.showerror('ERROR', 'INVALID USERNAME OR PASSWORD\nCheck the Details and try again.')
                        except smtplib.SMTPConnectError:
                            messagebox.showerror('ERROR', 'CONNECTION ERROR.PLEASE TRY AGAIN LATER')
                        except Exception:
                            messagebox.showerror('ERROR', 'PLEASE ENTER VALID DETAILS.')
                else:
                    messagebox.showerror('ERROR', 'PLEASE FILL ALL THE FEILDS AND TRY AGAIN.')
            else:
                messagebox.showerror('ERROR', 'DUPLICATE RECORDS NOT ALLOWED')
        else:
            messagebox.showerror('ERROR', 'DUPLICATE RECORDS NOT ALLOWED')

def deleteRecord(window,mainWindow):
        selected = window.my_tree.focus()
        if(selected != ''):
            MsgBox = messagebox.askquestion('Delete Record', 'Are you sure you want to Delete the record?')
            if MsgBox == 'yes':
                values = window.my_tree.item(selected,'values')
                id = int(values[0])
                x = window.my_tree.selection()[0]
                con=sqlite3.connect('Database/system.db')
                cur=con.cursor()
                cur.execute("DELETE from DomainDetails where oid=:oid",{'oid':id})
                con.commit()
                con.close()
                countDomain(mainWindow)
                window.UsernameInput.delete(0,END)
                window.PasswordInput.delete(0,END)
                window.OutgoingServerInput.delete(0,END)
                window.PortInput.delete(0,END)
                window.my_tree.delete(x)


def updateRecord(window):
        selected = window.my_tree.focus()
        if(selected != ''):
            MsgBox = messagebox.askquestion('Save Update', 'Are you sure you want to Update the changes?')
            if MsgBox == 'yes':
                values = window.my_tree.item(selected,'values')
                id = values[0]
                username = window.UsernameInput.get()
                password = window.PasswordInput.get()
                outgoingServer = window.OutgoingServerInput.get()
                port = window.PortInput.get()
                if(username!='' and password!='' and outgoingServer!='' and port != ""):
                    try:
                        smtpObj = smtplib.SMTP(host=outgoingServer,port=port)
                        context=ssl.create_default_context()
                        smtpObj.starttls(context=context)
                        smtpObj.login(username,password)
                        con=sqlite3.connect('Database/system.db')
                        cur=con.cursor()
                        cur.execute("""UPDATE DomainDetails SET 
                            username = :user,
                            password = :pass,
                            outgoingServer = :server,
                            port = :port
                            WHERE oid = :oid""",
                            {
                                'user':username,
                                'pass':EncryptPass(password),
                                'server':outgoingServer,
                                'port':port,
                                'oid':id
                            }
                        )
                        con.commit()
                        con.close()
                        window.my_tree.item(selected,text='',values=(id,username,outgoingServer,port))
                        if len(window.my_tree.selection()) > 0:
                            window.my_tree.selection_remove(window.my_tree.selection()[0])
                        window.UsernameInput.delete(0,END)
                        window.PasswordInput.delete(0,END)
                        window.OutgoingServerInput.delete(0,END)
                        window.PortInput.delete(0,END)
                    except smtplib.SMTPAuthenticationError:
                        messagebox.showerror('ERROR', 'INVALID USERNAME OR PASSWORD\nCheck the Details and try again.')
                    except smtplib.SMTPConnectError:
                        messagebox.showerror('ERROR', 'CONNECTION ERROR.PLEASE TRY AGAIN LATER')
                    except Exception:
                        messagebox.showerror('ERROR', 'PLEASE ENTER VALID DETAILS.')

def clearField(window):
        window.UsernameInput.delete(0,END)
        window.PasswordInput.delete(0,END)
        window.OutgoingServerInput.delete(0,END)
        window.PortInput.delete(0,END)
        if len(window.my_tree.selection()) > 0:
            window.my_tree.selection_remove(window.my_tree.selection()[0])