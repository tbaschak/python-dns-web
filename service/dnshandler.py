
from base import app, log
from dbhandler import DBHandler
from model.zoneentry import ZoneEntry

import traceback

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
            data["success"] = False
        else:
            if db.execute("""
                INSERT INTO zones(name,ip,updated)
                VALUES('%s','%s',1)
                       """%(name,ip)):
                data["success"] = True
                data["message"] = u"Entry %s inserted"%(name)
            else:
                data["success"] = False
                data["error"] = u"Unsuccessful database insert transaction"
        return data
    
    def editName(self, name, ip):
        data = {}
        db = DBHandler(app.config["DBFILE"])
        c = db.getCursor()
        zone = list(c.execute("""
            SELECT name FROM zones
            WHERE ip LIKE ?
            """,[ip]))[0]
        if zone[0] == name:
            data["error"] = u"Name entry is the same as existing name"
            return data
        if db.exists("zones", "name", name):
            data["error"] = u"Duplicate name entry in db"
            data["success"] = False
            return data
        try:
            c.execute("""
                UPDATE zones SET name = ?, updated = 1 WHERE ip LIKE ?
                """,[name, ip])
            db.commit()
            data["success"] = True
            data["message"] = u"Entry %s updated from %s"%(name, zone[0])
        except Exception, e:
            errormsg = u"Unsuccessful database update transaction"
            log.exception(errormsg, self.__class__.__name__)
            data["success"] = False
            data["error"] = errormsg
        return data
    
    def editIp(self, name, ip):
        data = {}
        db = DBHandler(app.config["DBFILE"])
        c = db.getCursor()
        zone = list(c.execute("""
            SELECT ip FROM zones
            WHERE name LIKE ?
            """,[name]))[0]
        if zone[0] == ip:
            data["error"] = u"Ip entry is the same as existing name"
            return data
        try:
            c.execute("""
                UPDATE zones SET ip = ?, updated = 1 WHERE name LIKE ?
                """,[ip,name])
            db.commit()
            data["success"] = True
            data["message"] = u"Entry %s updated from %s"%(ip, zone[0])
        except Exception, e:
            errormsg = u"Unsuccessful database update transaction"
            log.exception(errormsg, self.__class__.__name__)
            data["success"] = False
            data["error"] = errormsg
        return data
    
    def delete(self, name):
        data = {}
        db = DBHandler(app.config["DBFILE"])
        c = db.getCursor()
        zone = list(c.execute("""
            SELECT name FROM zones
            WHERE name LIKE ?
            """,[name]))[0]
        if zone[0] == name:
            try:
                c.execute("""
                    DELETE FROM zones WHERE name LIKE ?
                    """,[name])
                db.commit()
                data["success"] = True
                data["message"] = u"Entry %s deleted"%(name)
            except Exception, e:
                errormsg = u"Unsuccessful database delete transaction"
                log.exception(errormsg, self.__class__.__name__)
                data["success"] = False
                data["error"] = errormsg
        else:
            data["success"] = False
            data["message"] = u"Entry %s not found"%(name)
        return data

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
        
    def getEntryByName(self, name):
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