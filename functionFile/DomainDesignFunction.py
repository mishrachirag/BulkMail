
from classFile.DomainEditDataClass import DomainEditDataClass
from classFile.DomainSettingClass import DomainSettingClass

def EditData(mainwindow):
           domainEdit =  DomainEditDataClass(mainwindow)
           domainEdit.LabelData()
           domainEdit.SpinBoxData(mainwindow)
           domainEdit.EntryData()
           domainEdit.ButtonData(mainwindow)

def DomainSetting(window):
    domainSettingClass = DomainSettingClass(window)
    domainSettingClass.LabelData()
    domainSettingClass.EntryData()
    domainSettingClass.CheckBoxData()
    domainSettingClass.TreeData()
    domainSettingClass.ButtonData(window)
    
