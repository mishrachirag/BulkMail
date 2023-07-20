from classFile.MailAppClass import BulkMail
from classFile.DomainDesignClass import DomainFrame

if __name__ == "__main__":
    app = BulkMail()
    app.LabelData()
    app.EntryData()
    app.RadioButtonData()
    app.TextBoxData()
    domainFrame = DomainFrame(app)
    domainFrame.LabelData(app)
    domainFrame.ButtonData(app)
    app.ButtonData(domainFrame)
    app.StartFunctions()
    app.mainloop()
