from tkinter import CENTER, NO, RIGHT, W, Y,ttk
import customtkinter
import pandas

from Design.DesignFile import designButton, designLabelBold, windowDesignFrame,appIconPath,appTitle

class ViewEmailClass(customtkinter.CTkToplevel):
    def __init__(self,container):
        super().__init__(container)
        self.grab_set()
        self.title(appTitle)
        self.iconbitmap(appIconPath)
        windowDesignFrame(self,height = 400,width= 300)

    def LabelData(self):
        self.domainSettingDataLabel =customtkinter.CTkLabel(self)
        designLabelBold(self.domainSettingDataLabel,"View Mail")
        self.domainSettingDataLabel.place(x=80,y=10)

    def TreeData(self,mailpath):
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
        self.tree_frame.place(x=30,y=50)

        self.tree_scroll = customtkinter.CTkScrollbar(self.tree_frame)
        self.tree_scroll.pack(side=RIGHT, fill=Y)
        
        self.my_tree = ttk.Treeview(self.tree_frame, yscrollcommand=self.tree_scroll.set, selectmode="browse")
        self.my_tree.pack()

        self.tree_scroll.configure(command=self.my_tree.yview)

        self.my_tree['columns'] = ("No.","Emails")

        self.my_tree.tag_configure('row', background="white")

        self.my_tree.column("#0", width=0, stretch=NO)
        self.my_tree.column("No.", anchor=CENTER, width=50)
        self.my_tree.column("Emails", anchor=CENTER, width=240)

        self.my_tree.heading("#0", text="", anchor=W)
        self.my_tree.heading("No.", text="No.", anchor=W)
        self.my_tree.heading("Emails", text="Emails", anchor=CENTER)

        self.df = pandas.read_csv(mailpath)
        if 'mails' in self.df.columns:
            self.count = 0
            for mail in self.df['mails']:
                    self.my_tree.insert(parent='', index='end', iid=self.count, text='', values=(self.count+1, mail), tags=('row',))
                    self.count += 1

    def ButtonData(self):
        self.closeButton= customtkinter.CTkButton(self,command=lambda:self.destroy(),fg_color="#FF605C",hover_color="#ff7976")
        designButton(self.closeButton,"Close")
        self.closeButton.place(x=80,y=350)