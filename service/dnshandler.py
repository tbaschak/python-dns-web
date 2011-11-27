
from base import app, log
from dbhandler import DBHandler

class DNSHandler:
    
    def __init__(self):
        self.zonefile = open(app.config["ZONEFILE"],"r")
        
    def __del__(self):
        self.zonefile.close()
    
    def getAllEntries(self):
        # return all entries found in the zone file
        return data
        
    def getEntryByName(self):
        return data
    
    def updateZoneFile(self):
        db = DBHandler(app.config["DBFILE"])
        del(db)
        zonefile = open(app.config["ZONEFILE"],"w")
        zonefile.close()
        