from time import sleep
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import socket
import sqlite3
import ssl
import threading
import pandas
from tkinter import END, filedialog, messagebox
from configuration.ConfigParserFile import changeConfig
from configuration.encDecFile import DecryptPass


def saveLog(window):
            window.log_data = window.logText.get(1.0,END)  
            if window.log_data !='':
                filename = filedialog.asksaveasfilename(defaultextension="*.txt",title="Save File",filetypes=(("Text Files","*.txt"),))
                if filename:
                    text_file = open(filename,'w')
                    text_file.write(window.log_data)
                    text_file.close()

def clearContent(mainWindow):
    MsgBox = messagebox.askquestion('Clear content', 'Are you sure you want to clear the contents?')
    if MsgBox == 'yes':
        mainWindow.stopnum = 0
        mainWindow.subjectEntry.delete(0,END)
        mainWindow.MessageText.delete(1.0,END)
        mainWindow.logText.delete(1.0,END)
        mainWindow.saveLogButton.configure(state='disabled')
        mainWindow.logText.configure(state='disabled')
        changeConfig('mailpath','Empty')
        mainWindow.save_MailPath = 'Empty'
        changeConfig('type','Empty')
        mainWindow.save_type = 'Empty'

def execMailTransfer(mainWindow,domainFrame,MailList,type,subject,message,DomainDataDictionary):
    try:
        MessageCount = 0
        DomainCount = 1
        username = DomainDataDictionary[DomainCount][0]
        password = DomainDataDictionary[DomainCount][1]
        outgoingserver = DomainDataDictionary[DomainCount][2]
        port = DomainDataDictionary[DomainCount][3]
        smtpObj = smtplib.SMTP(host=outgoingserver,port=port)
        context=ssl.create_default_context()
        smtpObj.starttls(context=context)
        smtpObj.login(username,password)
        counter = 1
        for mail in MailList:
            # print(len(MailList))
            if (mainWindow.stopnum == 1):
                break
            MessageCount +=1
            messageBody = MIMEMultipart("alternative")
            messageBody["Subject"] = subject
            messageBody["From"] = username
            messageBody["To"] =mail
            data = MIMEText(message,type)
            messageBody.attach(data)
            smtpObj.sendmail(from_addr=username,to_addrs= mail,msg= messageBody.as_string())
            mainWindow.logText.insert(END,f"Message send from username:{username} with host: {outgoingserver} and port: {port} to {mail} successful\n")
            
            if counter==len(MailList):
                pass
            else:
                mainWindow.logText.insert(END,f"waiting for {mainWindow.waitDataVar.get()} second's\n")
                sleep(mainWindow.waitDataVar.get())
            counter+=1
            if(MessageCount == mainWindow.domainChangeDataVar.get()):
                MessageCount = 0
                DomainCount +=1
                if(DomainCount > mainWindow.domainDataVar.get()):
                    DomainCount = 1
                smtpObj.quit()
                smtpObj.close()
                username = DomainDataDictionary[DomainCount][0]
                password = DomainDataDictionary[DomainCount][1]
                outgoingserver = DomainDataDictionary[DomainCount][2]
                port = DomainDataDictionary[DomainCount][3]
                smtpObj = smtplib.SMTP(host=outgoingserver,port=port)
                context=ssl.create_default_context()
                smtpObj.starttls(context=context)
                smtpObj.login(username,password) 
        smtpObj.quit()
        smtpObj.close()
        mainWindow.stopButton.configure(state='disabled')
        mainWindow.sendButton.configure(state='normal')
        domainFrame.DomainSettingButton.configure(state='normal')
        domainFrame.EditDataButton.configure(state='normal')
        mainWindow.ChooseEmailButton.configure(state='normal')
        mainWindow.clearButton.configure(state='normal')
        if(mainWindow.stopnum == 0):
            mainWindow.logText.insert(END,"EMAIL SEND COMPLETED.")
            mainWindow.saveLogButton.configure(state='normal')
        elif(mainWindow.stopnum == 1):
            mainWindow.logText.insert(END,"USER STOPPED THE EMAIL SENDING.")
            mainWindow.saveLogButton.configure(state='normal')
            mainWindow.stopnum = 0
            
    except smtplib.SMTPAuthenticationError:
        mainWindow.logText.insert(END,f"INVALID USERNAME OR PASSWORD : username:{username} with host: {outgoingserver} and port: {port}.\n")
        mainWindow.saveLogButton.configure(state='normal')
        messagebox.showerror('ERROR', 'INVALID USERNAME OR PASSWORD')
    except smtplib.SMTPConnectError:
        mainWindow.logText.insert(END,f"CONNECTION ERROR.PLEASE TRY AGAIN LATER : username:{username} with host: {outgoingserver} and port: {port}.\n")
        mainWindow.saveLogButton.configure(state='normal')
        messagebox.showerror('ERROR', 'CONNECTION ERROR.PLEASE TRY AGAIN LATER')

def SendMail(MainWindow,domainFrame):
    try:
        socket.create_connection(("www.google.com", 80),)
        MainWindow.save_MailPath
        MailList = [] 
        if(MainWindow.save_MailPath != 'Empty'):
            df = pandas.read_csv(MainWindow.save_MailPath)
            if(len(df['mails']) == 0):
                messagebox.showerror("ERROR","The text file does not contain emails. Check the Text file.")
            elif(MainWindow.domainDataVar.get() == 0):
                messagebox.showerror("ERROR","Domain Messaging server is not set.Please set the Domain Messaging Server in Domain Setting.")
            elif(MainWindow.subjectEntry.get()==''):
                messagebox.showerror("ERROR","Empty Subject field is not allowed.")
            elif(MainWindow.MessageText.get(1.0,END) == ''):
                messagebox.showerror("ERROR","Empty Message field is not allowed.")
            else:
                MsgBox = messagebox.askquestion('Send Mail', 'Are you sure you want to send the Mails?')
                if MsgBox == 'yes':
                    MainWindow.logText.delete(1.0,END)
                    MainWindow.stopButton.configure(state='normal')
                    MainWindow.logText.configure(state='normal')
                    MainWindow.sendButton.configure(state='disabled')
                    domainFrame.DomainSettingButton.configure(state='disabled')
                    domainFrame.EditDataButton.configure(state='disabled')
                    MainWindow.ChooseEmailButton.configure(state='disabled')
                    MainWindow.clearButton.configure(state='disabled')
                    for mail in df['mails']:
                        MailList.append(mail)
                    type = MainWindow.radioData.get()
                    subject = MainWindow.subjectEntry.get()
                    message = MainWindow.MessageText.get(1.0,END)
                    con=sqlite3.connect('Database/system.db')
                    cur=con.cursor()
                    cur.execute("select rowid,* from DomainDetails")
                    records = cur.fetchall()
                    con.commit()
                    con.close()
                    global countNum
                    countNum = 0
                    DomainDataDictionary = {}
                    for record in records:
                        DomainDataDictionary[record[0]] = [record[1], DecryptPass(record[2]), record[3], record[4]]
                        countNum += 1
                    #here code changes to be made
                    threading.Thread(target=execMailTransfer,args=[MainWindow,domainFrame,MailList,type,subject,message,DomainDataDictionary]).start()
        else:
            MainWindow.stopButton.configure(state='disabled')
            MainWindow.sendButton.configure(state='normal')
            domainFrame.DomainSettingButton.configure(state='normal')
            domainFrame.EditDataButton.configure(state='normal')
            MainWindow.ChooseEmailButton.configure(state='normal')
            MainWindow.clearButton.configure(state='normal')
            messagebox.showerror("ERROR","Please select emails file.")
    except OSError:
        MainWindow.stopButton.configure(state='disabled')
        MainWindow.sendButton.configure(state='normal')
        domainFrame.DomainSettingButton.configure(state='normal')
        domainFrame.EditDataButton.configure(state='normal')
        MainWindow.ChooseEmailButton.configure(state='normal')
        MainWindow.clearButton.configure(state='normal')
        messagebox.showerror("ERROR","Internet Required.Internet Not Connected")

def stopMailExec(className):
    className.stopnum = 1


def closeWindow(window):
    stopMailExec(window)
    window.destroy()
    