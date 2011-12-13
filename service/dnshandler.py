
from base import app, log
from model.zoneentry import ZoneEntry
from service.dbhandler import DBHandler
import traceback

class DNSHandler:
    
    def __init__(self):
        self.zonefile = None
        
    def __del__(self):
        if self.zonefile is not None:
            self.zonefile.close()
        
    def readZonefile(self):
        self.zonefile = open(app.config["ZONEFILE"],"r")
        self.lines = self.zonefile.readlines()
        
    def add(self, ip, name):
        data = {}
        # Check if name exists
        db = DBHandler(app.config["DBFILE"])
        if db.exists("zones", "name", name):
            data["error"] = u"Duplicate name entry in db"
            data["success"] = False
        else:
            if db.execute("""
                INSERT INTO zones(name,ip,updated,update_type)
                VALUES('?','?',1,'CREATE')
                       """,[name,ip]):
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
                UPDATE zones
                SET name = ?, updated = 1, update_type = 'MODIFIED NAME'
                WHERE ip LIKE ?
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
                UPDATE zones
                SET ip = ?, updated = 1, update_type = 'MODIFIED IP'
                WHERE name LIKE ?
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
                    UPDATE zones
                    SET update_type = 'DELETE'
                    WHERE name LIKE ?
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
            if line.find(app.config["ZONES_END_POINT"]) >= 0:
                printLines = False
            if printLines:
                zsplit = line.split()
                if len(zsplit) == 4:
                    data.append(ZoneEntry(zsplit[0],zsplit[3]))
            if line.find(app.config["ZONES_START_POINT"]) >= 0:
                printLines = True
        return data
        
    def getEntryByName(self, name):
        return data
    
    def zonefileJob(self):
        db = DBHandler(app.config["DBFILE"])
        c = db.getCursor()
        results = list(c.execute("""
            SELECT name, ip FROM zones
            WHERE updated = 1
            """,[]))
        if len(results) > 0:
            self.updateZonefile(results)
        pass
    
    def updateZonefile(self, results):
        self.readZonefile()
        zones = self.getAllEntries()
        for zone in zones:
            #print zone.name
            #print zone.ip
            pass
        for row in results:
            # Check if name exists
            
            pass
            # Should ip be changed?
            
            # Add entry
        
    def getSerial(self):
        serial = [";Serial", "; Serial"]
        for line in self.lines:
            for s in serial:
                if line.find(s) or line.find(s.lower) or line.find(s.upper):
                    print line
                    return line
                
                