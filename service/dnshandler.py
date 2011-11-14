
from base import app, log
from dbhandler import DBHandler

class DNSHandler:
    
    def getAllEntries(self):
        return data
        
    def getEntryByName(self):
        return data
    
    def readZoneFile(self):
        zonefile = open(app.config["ZONEFILE"],"r")
    
    def updateZoneFile(self):
        db = DBHandler(app.config["DBFILE"])
        del(db)
        zonefile = open(app.config["ZONEFILE"],"w")
        zonefile.close()
        