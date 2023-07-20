import sqlite3
from configuration.ConfigParserFile import changeConfig

def countDomain(mainwindow):
        con=sqlite3.connect('Database/system.db')
        cur=con.cursor()
        cur.execute("select count(*) from DomainDetails")
        rowcount = cur.fetchone()[0]
        changeConfig('noofdomains',str(rowcount))
        mainwindow.domainDataVar.set(rowcount)
        con.commit()
        con.close()