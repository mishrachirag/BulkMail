import sqlite3
from tkinter import *
from tkinter import ttk
import customtkinter

from Design.DesignFile import designButton, designLabel, designLabelBold, windowDesignFrame,appIconPath,appTitle
from configuration.encDecFile import DecryptPass
from functionFile.DomainSettingFunctions import addRecord, checkPasswordShow, clearField, deleteRecord, updateRecord

class DomainSettingClass(customtkinter.CTkToplevel):
    def __init__(self,mainWindow):
        super().__init__(mainWindow)
        self.grab_set()
        self.title(appTitle)
        self.iconbitmap(appIconPath)
        windowDesignFrame(self,height = 500,width= 700)
        self.check_pass_var = StringVar()
        self.check_pass_var.set("Hide")
        
    def LabelData(self):
        self.domainSettingDataLabel =customtkinter.CTkLabel(self)
        designLabelBold(self.domainSettingDataLabel,"Edit Domain Setting")
        self.domainSettingDataLabel.place(x=210,y=10)

        self.UsernameLabel = customtkinter.CTkLabel(self)
        designLabel(self.UsernameLabel,"Username :")
        self.UsernameLabel.place(x=20,y=320)

        self.PasswordLabel = customtkinter.CTkLabel(self)
        designLabel(self.PasswordLabel,"Password :")
        self.PasswordLabel.place(x=20,y=360)

        self.OutgoingServerLabel = customtkinter.CTkLabel(self)
        designLabel(self.OutgoingServerLabel,"Server   :")
        self.OutgoingServerLabel.place(x=20,y=400)

        self.PortLabel = customtkinter.CTkLabel(self)
        designLabel(self.PortLabel,"Port :")
        self.PortLabel.place(x=380,y=400)


    def EntryData(self):
        self.UsernameInput = customtkinter.CTkEntry(self,width=200,height=25)
        self.UsernameInput.place(x=160,y=320)   

        self.PasswordInput = customtkinter.CTkEntry(self,width=200,height=25,show="*")
        self.PasswordInput.place(x=160,y=360) 

        self.OutgoingServerInput = customtkinter.CTkEntry(self,width=200,height=25)
        self.OutgoingServerInput.place(x=160,y=400)

        self.PortInput = customtkinter.CTkEntry(self,width=80,height=25)
        self.PortInput.place(x=460,y=400)

    def CheckBoxData(self):
        self.passwordCheckbox = customtkinter.CTkCheckBox(self, text="Show Password", command=lambda:checkPasswordShow(self),
                                        variable=self.check_pass_var, onvalue="Show", offvalue="Hide")
        self.passwordCheckbox.place(x=380,y=360)

    def TreeData(self):
        self.style = ttk.Style()

        self.style.theme_use('default')

        self.style.configure("Treeview",
            background="grey",
                foreground="black",
                rowheight=30,
                rowwidth=80,
                fieldbackground="light blue")

        self.style.map('Treeview',
            background=[('selected', "#347083")])

        self.tree_frame = customtkinter.CTkFrame(self)
        self.tree_frame.place(x=60,y=40)

        self.tree_scroll = customtkinter.CTkScrollbar(self.tree_frame)
        self.tree_scroll.pack(side=RIGHT, fill=Y)

        self.my_tree = ttk.Treeview(self.tree_frame, yscrollcommand=self.tree_scroll.set, selectmode="browse")
        self.my_tree.pack()

        self.tree_scroll.configure(command=self.my_tree.yview)

        self.my_tree['columns'] = ("ID","UserName", "Outgoing Server", "Port")

        self.my_tree.tag_configure('row', background="white")
        # my_tree.tag_configure('evenrow', background="white")

        self.my_tree.column("#0", width=0, stretch=NO)
        self.my_tree.column("ID", anchor=CENTER, width=50)
        self.my_tree.column("UserName", anchor=CENTER, width=270)
        # my_tree.column("Password", anchor=CENTER, width=200)
        self.my_tree.column("Outgoing Server", anchor=CENTER, width=220)
        self.my_tree.column("Port", anchor=CENTER, width=110)

        self.my_tree.heading("#0", text="", anchor=W)
        self.my_tree.heading("ID", text="ID", anchor=W)
        self.my_tree.heading("UserName", text="UserName", anchor=W)
        # my_tree.heading("Password", text="Password", anchor=W)
        self.my_tree.heading("Outgoing Server", text="Outgoing Server", anchor=CENTER)
        self.my_tree.heading("Port", text="Port", anchor=CENTER) 

        def displaytreedata():
            con=sqlite3.connect('Database/system.db')
            cur=con.cursor()
            cur.execute("select rowid,* from DomainDetails")
            records = cur.fetchall()
            con.commit()
            con.close()
            global count
            count = 0

            for record in records:
                self.my_tree.insert(parent='', index='end', iid=count, text='',
                values=(record[0],record[1], record[3], record[4]), tags=('row',))
                count += 1
        displaytreedata()

        def select_record(e):
            self.UsernameInput.delete(0,END)
            self.PasswordInput.delete(0,END)
            self.OutgoingServerInput.delete(0,END)
            self.PortInput.delete(0,END)

            selected = self.my_tree.focus()
            if(selected != ''):
                values = self.my_tree.item(selected,'values')
                username = values[1]
                
                outgoingServer = values[2]
                port = values[3]
                con=sqlite3.connect('Database/system.db')
                cur=con.cursor()
                cur.execute(f"select password from DomainDetails where username = '{username}'")
                record = cur.fetchone()
                con.commit()
                con.close()
                password = DecryptPass(record[0])
                self.UsernameInput.insert(0,username)
                self.PasswordInput.insert(0,password)
                self.OutgoingServerInput.insert(0,outgoingServer)
                self.PortInput.insert(0,port)
        self.my_tree.bind("<ButtonRelease-1>",select_record)

    def ButtonData(self,mainWindow):
        self.addButton =  customtkinter.CTkButton(self,command=lambda:addRecord(self,mainWindow))
        designButton(self.addButton,"Add Record")
        self.addButton.place(x=20,y=440)

        self.deleteButton = customtkinter.CTkButton(self,command=lambda:deleteRecord(self,mainWindow))
        designButton(self.deleteButton,"Delete Record")
        self.deleteButton.place(x=150,y=440)

        updateButton = customtkinter.CTkButton(self,command=lambda:updateRecord(self))
        designButton(updateButton,"Update Record")
        updateButton.place(x=280,y=440)
        
        self.clearButton = customtkinter.CTkButton(self,command=lambda:clearField(self))
        designButton(self.clearButton,"Clear")
        self.clearButton.place(x=410,y=440)

        self.closeButton = customtkinter.CTkButton(self,command=lambda:self.destroy(),fg_color="#FF605C",hover_color="#ff7976")
        designButton(self.closeButton,"Close")
        self.closeButton.place(x=540,y=440)
