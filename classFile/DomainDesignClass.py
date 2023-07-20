from tkinter import *
import customtkinter

from functionFile.DomainDesignFunction import DomainSetting, EditData
from Design.DesignFile import designButton, designLabel, designLabelDynamic

class DomainFrame(customtkinter.CTkFrame):
    def __init__(self,mainWindow):
        super().__init__(mainWindow)
        self.configure(width=320,height=220)
        self.place(x = 700, y = 50)
    
    def LabelData(self,container):

        self.domainDataLabel = customtkinter.CTkLabel(self)
        designLabel(self.domainDataLabel,"No. of Domains : ")
        self.domainDataLabel.place(x=10,y=10)

        # textvariable=container.variables.domainDataVar
        self.domainData = customtkinter.CTkLabel(self)
        designLabelDynamic(self.domainData,container.domainDataVar)
        self.domainData.place(x=230,y=10)

        self.waitingDataLabel = customtkinter.CTkLabel(self)
        designLabel(self.waitingDataLabel,"Waiting(sec's) :\n (10s to 600s) ")
        self.waitingDataLabel.place(x=10,y=40)

        # textvariable=waitDataVar
        self.waitingData = customtkinter.CTkLabel(self)
        designLabelDynamic(self.waitingData,container.waitDataVar)
        self.waitingData.place(x=230,y=40)

        self.DomainChangeDataLabel = customtkinter.CTkLabel(self)
        designLabel(self.DomainChangeDataLabel,"No. of Message :\n After which\ndomain change ")
        self.DomainChangeDataLabel.place(x=10,y=90)

        # textvariable=domainChangeDataVar
        self.domainChangeData = customtkinter.CTkLabel(self)
        designLabelDynamic(self.domainChangeData,container.domainChangeDataVar)
        self.domainChangeData.place(x=230,y=90)

    def ButtonData(self,mainwindow):

        self.DomainSettingButton= customtkinter.CTkButton(self,command=lambda:DomainSetting(mainwindow))
        designButton(self.DomainSettingButton,"Domain Setting")
        self.DomainSettingButton.place(x=30,y=170)

        self.EditDataButton= customtkinter.CTkButton(self,command=lambda:EditData(mainwindow))
        designButton(self.EditDataButton,"Edit")
        self.EditDataButton.place(x=180,y=170)
