from tkinter import *
from tkinter.font import BOLD

import customtkinter

import socket

from configparser import ConfigParser

import sqlite3

from functionFile.SelectEmailFunctions import ChooseEmail, ViewEmail
from functionFile.MailAppFunctions import SendMail, clearContent, closeWindow, saveLog, stopMailExec
from configuration.ConfigParserFile import changeConfig

from Design.DesignFile import *
customtkinter.set_appearance_mode(appApperanceMode)  
customtkinter.set_default_color_theme(appDefaultColorTheme)


class BulkMail(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title(appTitle)
        self.iconbitmap(appIconPath)
        windowDesign(self,height = 600,width= 1100)

        self.radioData = StringVar()
        self.radioData.set('plain')

        self.parser = ConfigParser()
        self.parser.read("configuration/configuration.txt")
        self.save_NoOfDomains = self.parser.get('Setting','NoOfDomains')
        self.save_WaitingSec = self.parser.get('Setting','WaitingSec')
        self.save_MessageNo = self.parser.get('Setting','MessageNo')
        self.save_MailPath = self.parser.get('Setting','mailpath')
        self.save_type = self.parser.get('Setting','type')

        self.stopnum = 0

        self.domainDataVar = IntVar()
        self.domainDataVar.set(self.save_NoOfDomains)

        self.waitDataVar = IntVar()
        self.waitDataVar.set(self.save_WaitingSec)

        self.domainChangeDataVar = IntVar()
        self.domainChangeDataVar.set(self.save_MessageNo)

    def StartFunctions(self):
        def is_connected():
            try:
                socket.create_connection(("www.google.com", 80),)
                state = "Internet: Online"
                color = "green"
            except OSError:
                state = "Internet: Offline"
                color = "red"
            self.InternetLabel.configure(text=state,bg_color=color)
            self.after(3000, is_connected)
        is_connected()

        def countDomain():
            con=sqlite3.connect('Database/system.db')
            cur=con.cursor()
            cur.execute("select count(*) from DomainDetails")
            rowcount = cur.fetchone()[0]
            changeConfig('noofdomains',str(rowcount))
            self.domainDataVar.set(rowcount)
            con.commit()
            con.close()
        countDomain()

        changeConfig('mailpath','Empty')
        self.save_MailPath = 'Empty'
        changeConfig('type','Empty')
        self.save_type = 'Empty'


    def LabelData(self):
        self.InternetLabel = customtkinter.CTkLabel(self,text="INTERNET",bg_color='blue',corner_radius=10)
        self.InternetLabel.place(x = 10,y = 5 )

        self.subjectLabel = customtkinter.CTkLabel(self)
        designLabel(self.subjectLabel,"Subject :")
        self.subjectLabel.place(x=10,y=50)

        self.emailsDataLabel = customtkinter.CTkLabel(self)
        designLabel(self.emailsDataLabel,"Receiver Emails :")
        self.emailsDataLabel.place(x= 10,y=100)

        self.messageDataLabel = customtkinter.CTkLabel(self)
        designLabel(self.messageDataLabel,"Enter Message :")
        self.messageDataLabel.place(x=10,y=150)

        self.logLabel = customtkinter.CTkLabel(self)
        designLabel(self.logLabel,"Log Data :")
        self.logLabel.place(x=700,y=320)

    def EntryData(self):
        self.subjectEntry = customtkinter.CTkEntry(self,width=400,height=30)
        self.subjectEntry.place(x=150,y=50)

    def ButtonData(self,domainFrame):

        self.ChooseEmailButton= customtkinter.CTkButton(self,command=lambda:ChooseEmail(self))
        designButton(self.ChooseEmailButton,'Select Email Id\'s')
        self.ChooseEmailButton.place(x=230,y=95)

        self.ViewEmailButton= customtkinter.CTkButton(self,command=lambda:ViewEmail(self))
        designButton(self.ViewEmailButton,'View Email Id\'s')
        self.ViewEmailButton.place(x=380,y=95)

        self.sendButton= customtkinter.CTkButton(self,command=lambda:SendMail(self,domainFrame))
        designButton(self.sendButton,'Send')
        self.sendButton.place(x=100,y=535)

        self.clearButton= customtkinter.CTkButton(self,text='Clear',command=lambda:clearContent(self))
        designButton(self.clearButton,"Clear")
        self.clearButton.place(x=350,y=535)

        self.stopButton= customtkinter.CTkButton(self,state="disabled",text_color_disabled="grey",command=lambda:stopMailExec(self))
        designButton(self.stopButton,"Stop")
        self.stopButton.place(x=600,y=535)

        self.closeButton= customtkinter.CTkButton(self,command=lambda:closeWindow(self),fg_color="#FF605C",hover_color="#ff7976")
        designButton(self.closeButton,"Close")
        self.closeButton.place(x=850,y=535)

        self.saveLogButton= customtkinter.CTkButton(self,state="disabled",text_color_disabled="grey",command=lambda:saveLog(self))
        designButton(self.saveLogButton,"Save Log")
        self.saveLogButton.place(x=930,y=310)



    def RadioButtonData(self):
        self.plainRadioButton = customtkinter.CTkRadioButton(self,text="plain text",variable=self.radioData,value='plain',font=("Times New Roman", 14))
        self.plainRadioButton.select()
        self.plainRadioButton.place(x=100,y=180)

        self.htmlRadioButton = customtkinter.CTkRadioButton(self,text="html",variable=self.radioData,value='html',font=("Times New Roman", 14))
        self.htmlRadioButton.place(x=300,y=180)

    def TextBoxData(self):
        
        self.MessageText = customtkinter.CTkTextbox(self, wrap=WORD,width=600, height=280,font=("Times New Roman", 12))
        self.MessageText.place(x = 10,y = 230)

        self.logText = customtkinter.CTkTextbox(self,wrap=WORD,width=350, height=160,font=("Times New Roman", 12))
        self.logText.place(x = 700,y = 350)
        self.logText.configure(state="disabled")
