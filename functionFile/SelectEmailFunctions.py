from configparser import ConfigParser
from tkinter import messagebox, filedialog
import pandas
from classFile.ViewEmailDesignClass import ViewEmailClass

from configuration.ConfigParserFile import changeConfig

def ChooseEmail(Container):
    datasetDestination = filedialog.askopenfilename(initialdir = "YOUR DIRECTORY PATH")
    if (datasetDestination.lower().endswith(".txt")):
            df = pandas.read_csv(datasetDestination)
            if 'mails' in df.columns:
                if(len(df['mails']) == 0):
                    messagebox.showerror("ERROR","The text file does not contain emails. Check the Text file.")
                else:
                    changeConfig('mailpath',datasetDestination)
                    Container.save_MailPath = datasetDestination
                    changeConfig('type','Text')
                    Container.save_type = 'Text'
                    messagebox.showinfo(title="Text file Selected", message="Text File Selected.")
            else:
                changeConfig('mailpath','Empty')
                Container.save_MailPath = 'Empty'
                changeConfig('type','Empty')
                Container.save_type = 'Empty'
                messagebox.showerror(title="Decline", message="Text file  does not contain mails column.Please select proper mail column file.")
                datasetDestination = ''
        
    else:
        changeConfig('mailpath','Empty')
        Container.save_MailPath = 'Empty'
        changeConfig('type','Empty')
        Container.save_type = 'Empty'
        messagebox.showerror(title="Error", message="Please select email file.")


def ViewEmail(Container):
    parser = ConfigParser()
    parser.read("configuration/configuration.txt")
    mailpath = parser.get('Setting','mailpath')
    if (mailpath == 'Empty'):
        messagebox.showerror(title="Error", message="Select Email file.")
    else:
        view = ViewEmailClass(Container)
        view.LabelData()
        view.TreeData(mailpath)
        view.ButtonData()