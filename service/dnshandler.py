
from base import app, log
from dbhandler import DBHandler
from model.zoneentry import ZoneEntry

class DNSHandler:
    
    def __init__(self):
        self.zonefile = open(app.config["ZONEFILE"],"r")
        self.lines = self.zonefile.readlines()
        
    def __del__(self):
        self.zonefile.close()
        
    def add(self, ip, name):
        data = {}
        # Check if name exists
        db = DBHandler(app.config["DBFILE"])
        if db.exists("zones", "name", name):
            data["error"] = u"Duplicate name entry in db"
        else:
            db.execute("""
                INSERT INTO zones(name,ip,updated)
                VALUES('%s','%s',1)
                       """%(name,ip))
        return data
    #def edit(self):
    
    def getAllEntries(self):
        # return all entries found in the zone file
        data = []
        printLines = False
        for line in self.lines:
            if line.find(";Aliases") >= 0:
                printLines = False
            if printLines:
                zsplit = line.split()
                if len(zsplit) == 4:
                    data.append(ZoneEntry(zsplit[0],zsplit[3]))
            if line.find(";Machine Names") >= 0:
                printLines = True
        return data
        
    def getEntryByName(self):
        return data
    
    def updateZoneFile(self):
        #db = DBHandler(app.config["DBFILE"])
        #del(db)
        pass
        
    def getSerial(self):
        serial = [";Serial", "; Serial"]
        for line in self.lines:
            for s in serial:
                if line.find(s) or line.find(s.lower) or line.find(s.upper):
                    print line
                    return line