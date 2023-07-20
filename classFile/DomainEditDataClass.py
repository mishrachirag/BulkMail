
from tkinter import IntVar, Spinbox
import customtkinter


from Design.DesignFile import designButton, designLabel, designLabelBold, windowDesignFrame,appTitle,appIconPath
from functionFile.DomainEditDataFunction import SaveEdit

class DomainEditDataClass(customtkinter.CTkToplevel):
    def __init__(self,mainWindow):
        super().__init__(mainWindow)
        self.grab_set()
        self.title(appTitle)
        self.iconbitmap(appIconPath)
        windowDesignFrame(self,height = 250,width= 320)
        self.temp = IntVar()
        self.temp2 = IntVar()
        self.temp2.set(mainWindow.domainChangeDataVar.get())

    def LabelData(self):
        self.domainDataLabel =customtkinter.CTkLabel(self)
        designLabelBold(self.domainDataLabel,"Edit Setting")
        self.domainDataLabel.place(x=70,y=10)

        self.waitingDataLabel = customtkinter.CTkLabel(self)
        designLabel(self.waitingDataLabel,"Waiting(sec's) :\n (10s to 600s) ")
        self.waitingDataLabel.place(x=10,y=40)

        self.DomainChangeDataLabel = customtkinter.CTkLabel(self)
        designLabel(self.DomainChangeDataLabel,"No. of Message :\n After which\ndomain change ")
        self.DomainChangeDataLabel.place(x=10,y=100)

    def SpinBoxData(self,mainwindow):
        self.temp.set(mainwindow.waitDataVar.get())
        self.waitingSpinBox = Spinbox(self,from_=10,to=600,width=5,font=("courier",12),textvariable=self.temp,background="gray20",foreground="#DCE4EE",buttonbackground="gray10")
        self.waitingSpinBox.place(x=260,y=55,height=30)

    def EntryData(self):
        self.domainChangeInput = customtkinter.CTkEntry(self,width=70,height=30,textvariable=self.temp2)
        self.domainChangeInput.place(x=205,y=100)

    def ButtonData(self,mainWindow):
        saveButton = customtkinter.CTkButton(self,command=lambda:SaveEdit(self,mainWindow))
        designButton(saveButton,"Save")
        saveButton.place(x=30,y=190)

        closeButton= customtkinter.CTkButton(self,command=lambda:self.destroy(),fg_color="#FF605C",hover_color="#ff7976")
        designButton(closeButton,"Close")
        closeButton.place(x=180,y=190)
    
