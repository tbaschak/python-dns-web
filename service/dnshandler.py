
from base import app, log
from model.zoneentry import ZoneEntry
from service.dbhandler import DBHandler
import traceback
import fileinput
import sys

class DNSHandler:
    
    def __init__(self):
        self.zonefile = None
        self.tempfile = None
        self.serial = [";Serial", "; Serial"]
        
    def __del__(self):
        if self.zonefile is not None:
            self.zonefile.close()
        if self.tempfile is not None:
            self.tempfile.close()
        
    def readZonefile(self):
        self.zonefile = open(app.config["ZONEFILE"],"r")
        self.lines = self.zonefile.readlines()
        
    def createTempFile(self):
        self.tempfile = open("tempzonefile","w")
        
    def add(self, name, ip):
        data = {}
        # Check if name exists
        db = DBHandler(app.config["DBFILE"])
        c = db.getCursor()
        if db.exists("zones", "name", name):
            data["error"] = u"Duplicate name entry in db"
            data["success"] = False
        else:
            try:
                c.execute("""
                    INSERT INTO zones(name,ip,updated,update_type)
                    VALUES(?,?,1,'CREATE')
                           """,[name,ip])
                db.commit()
                data["success"] = True
                data["message"] = u"Entry %s inserted"%(name)
            except Exception, e:
                errormsg = u"Unsuccessful database insert transaction:" + e
                log.exception(errormsg, self.__class__.__name__)
                data["success"] = False
                data["error"] = errormsg
        return data
    
    def editName(self, fromName, toName):
        data = {}
        if fromName == toName:
            data["error"] = u"Name entry is the same as existing name"
            data["success"] = False
            return data
        db = DBHandler(app.config["DBFILE"])
        c = db.getCursor()
        if db.exists("zones", "name", toName):
            data["error"] = u"Duplicate name entry in db"
            data["success"] = False
            return data
        if not db.exists("zones", "name", fromName):
            data["error"] = u"No old name entry in db"
            data["success"] = False
            return data
        try:
            c.execute("""
                UPDATE zones
                SET name = ?, updated = 1, update_type = 'MODIFIED NAME'
                WHERE name LIKE ?
                """,[toName, fromName])
            db.commit()
            data["success"] = True
            data["message"] = u"Entry %s updated from %s"%(toName, fromName)
        except Exception, e:
            errormsg = u"Unsuccessful database update transaction:" + e
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
            data["success"] = False
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
            errormsg = u"Unsuccessful database update transaction:" + e
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
            """,[name]))
        if len(zone) > 0 and zone[0][0] == name:
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
                errormsg = u"Unsuccessful database delete transaction:" + e
                log.exception(errormsg, self.__class__.__name__)
                data["success"] = False
                data["error"] = errormsg
        else:
            data["success"] = False
            data["error"] = u"Entry %s not found"%(name)
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
    
    def convertResults(self,results):
        data = []
        for row in results:
            data.append(ZoneEntry(row[0],row[1],row[2]))
        return data
        
    def getEntryByName(self, name):
        return data
    
    def zonefileJob(self):
        db = DBHandler(app.config["DBFILE"])
        c = db.getCursor()
        results = list(c.execute("""
            SELECT name, ip, update_type FROM zones
            WHERE updated = 1
            """,[]))
        if len(results) > 0:
            self.updateZonefile(self.convertResults(results))
        pass
    
    def updateZonefile(self, zones):
        self.readZonefile()
        self.createTempFile()
        zoneEntries = self.getAllEntries()
        for zone in zones:
            if zone.updateType == "CREATE":
                self.addZone(zone)
            elif "MODIFIED" in zone.updateType:
                self.editZone(zone)
            elif zone.updateType == "DELETE":
                self.deleteZone(zone)
                
    def addZone(self, zone):
        for line in self.lines:
            if app.config["ZONES_END_POINT"] in line:
                newline = "%s\t\tIN\tA\t\t%s\n"%(zone.name,zone.ip)
                self.tempfile.write(newline)
            self.tempfile.write(line)
        
    def updateZone(self):
        for line in self.lines:
            if zone.updateType == "MODIFIED NAME":
                if zone.name in line:
                    newline = "%s\t\tIN\tA\t\t%s\n"%(zone.name,zone.ip)
                    self.tempfile.write(newline)
            self.tempfile.write(line)
    
    def deleteZone(self):
        pass

    def getSerial(self):
        for line in self.lines:
            for s in self.serial:
                if line.find(s) or line.find(s.lower) or line.find(s.upper):
                    print line
                    return line
                
                