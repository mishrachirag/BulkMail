

from tkinter import messagebox
from configuration.ConfigParserFile import changeConfig

def SaveEdit(window,mainWindow):
        MsgBox = messagebox.askquestion('Save Changes', 'Are you sure you want to saved the changes?')
        if MsgBox == 'yes':
            waitingdataTemp = window.waitingSpinBox.get()
            domainChangeDataTemp = window.domainChangeInput.get()

            if(domainChangeDataTemp.isdigit() == False or waitingdataTemp.isdigit() == False):
                messagebox.showerror("Check Input Field", "Only Numbers should be entered.")
            
            elif(int(waitingdataTemp) < 10 or int(waitingdataTemp) > 600):
                    messagebox.showerror("Check Limit", "The waiting sec should be between 10s to 600s.")

            else:
                changeConfig('MessageNo',domainChangeDataTemp)
                changeConfig('WaitingSec',waitingdataTemp)
                mainWindow.waitDataVar.set(waitingdataTemp)
                mainWindow.domainChangeDataVar.set(domainChangeDataTemp)
                messagebox.showinfo("Successful", "The changes has been successfully done.")