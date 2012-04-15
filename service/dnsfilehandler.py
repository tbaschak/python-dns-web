from base import app, log
from model.zoneentry import ZoneEntry
from service.dbhandler import DBHandler
import traceback
import fileinput
import sys
import os
import socket
from subprocess import call
    
class DNSFileHandler:
    
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
        return self.lines
        
    def createTempFile(self):
        self.tempfile = open(app.config["TEMPZONEFILE"],"w")
        
    def moveZoneFile(self):
        os.rename(app.config["TEMPZONEFILE"], app.config["ZONEFILE"] )
        
    def getAllEntries(self, lines):
        # return all entries found in the zone file
        data = []
        printLines = False
        for line in lines:
            if line.find(app.config["ZONES_END_POINT"]) >= 0:
                printLines = False
            if printLines:
                zsplit = line.split()
                if len(zsplit) == 4:
                    data.append(ZoneEntry(zsplit[0],zsplit[3]))
            if line.find(app.config["ZONES_START_POINT"]) >= 0:
                printLines = True
        return data
    
    def reloadBind(self):
        if call(app.config["BIND_RELOAD_CMD"], shell=True) != 0:
            errormsg = u"Couldn't reload BIND."
            log.exception(errormsg, self.__class__.__name__)
        
    def zonefileJob(self):
        self.db = DBHandler(app.config["DBFILE"])
        self.c = self.db.getCursor()
        results = list(self.c.execute("""
            SELECT name, host, update_type, old_value FROM zones
            WHERE updated = 1
            """,[]))
        if len(results) > 0:
            self.updateZonefile(self.convertResults(results))
    
    def updateZonefile(self, zones):
        self.readZonefile()
        self.createTempFile()
        for zone in zones:
            self.templines = []
            if zone.updateType == "CREATE":
                self.addZone(zone)
            elif "MODIFIED" in zone.updateType:
                self.updateZone(zone)
            elif zone.updateType == "DELETE":
                self.deleteZone(zone)
            app.logger.info(zone.updateType+" zone: "+str(zone.name))
            for item in ["CREATE", "MODIFIED", "DELETE"]:
                if item in zone.updateType:
                    self.lines = list(self.templines)
        self.updateSerial()
        for line in self.lines:
            self.tempfile.write(line)
        self.tempfile.close()
        self.moveZoneFile()
        self.reloadBind()
                
    def addZone(self, zone):
        added = False
        for i, line in enumerate(self.lines):
            if app.config["ZONES_END_POINT"] in line:
                # Check if ip address or hostname
                try:
                    socket.inet_aton(zone.host)
                    newline = "%s\tIN\tA\t%s\n"%(zone.name,zone.host)
                except:
                    if not zone.host[:-1] == ".":
                        zone.host = zone.host + "."
                    newline = "%s\tIN\tCNAME\t%s\n"%(
                        zone.name,zone.host)
                self.templines.insert(i, newline)
                added = True
            if added:
                self.templines.insert(i+1, line)
            else:
                self.templines.insert(i, line)
        if added:
            try:
                self.c.execute("""
                    UPDATE zones
                    SET updated = 0, update_type = NULL
                    WHERE name LIKE ?
                    """,[zone.name])
                self.db.commit()
            except Exception, e:
                errormsg = u"Unsuccessful database update transaction:" + str(e)
                log.exception(errormsg, self.__class__.__name__)
                        
    def updateZone(self, zone):
        checkZoneName = False
        updatedName = False
        updatedHost = False
        for line in self.lines:
            if app.config["ZONES_END_POINT"] in line:
                checkZoneName = False
            if app.config["ZONES_START_POINT"] in line:
                checkZoneName = True
            if zone.updateType == "MODIFIED NAME":
                if checkZoneName is True and zone.old_value == line.split()[0]:
                    # This will remove duplicates
                    if not updatedName:
                        # Check if ip address or hostname
                        try:
                            socket.inet_aton(zone.host)
                            newline = "%s\tIN\tA\t%s\n"%(zone.name,zone.host)
                        except:
                            if not zone.host[:-1] == ".":
                                zone.host = zone.host + "."
                            newline = "%s\tIN\tCNAME\t%s\n"%(
                                zone.name,zone.host)
                        self.templines.append(newline)
                        updatedName = True
                else:
                    self.templines.append(line)
            elif zone.updateType == "MODIFIED HOST":
                if checkZoneName is True and zone.name in line.split()[0]:
                    # This will remove duplicates
                    if not updatedHost:
                        # Check if ip address or hostname
                        try:
                            socket.inet_aton(zone.host)
                            newline = "%s\tIN\tA\t%s\n"%(zone.name,zone.host)
                        except:
                            if not zone.host[:-1] == ".":
                                zone.host = zone.host + "."
                            newline = "%s\tIN\tCNAME\t%s\n"%(
                                zone.name,zone.host)
                        self.templines.append(newline)
                        updatedHost = True
                else:
                    self.templines.append(line)
        if updatedName:
            try:
                self.c.execute("""
                    UPDATE zones
                    SET updated = 0, update_type = NULL, name = ?
                    WHERE old_value LIKE ?
                    """,[zone.name, zone.old_value])
                self.db.commit()
            except Exception, e:
                errormsg = u"Unsuccessful database update transaction:" + str(e)
                log.exception(errormsg, self.__class__.__name__)
        if updatedHost:
            try:
                self.c.execute("""
                    UPDATE zones
                    SET updated = 0, update_type = NULL, host = ?
                    WHERE name LIKE ?
                    """,[zone.host, zone.name])
                self.db.commit()
            except Exception, e:
                errormsg = u"Unsuccessful database update transaction:" + str(e)
                log.exception(errormsg, self.__class__.__name__)
    
    def deleteZone(self,zone):
        checkZoneName = False
        for line in self.lines:
            if zone.updateType == "DELETE":
                if app.config["ZONES_END_POINT"] in line:
                    checkZoneName = False
                if app.config["ZONES_START_POINT"] in line:
                    checkZoneName = True
                if checkZoneName and zone.name in line:
                    # This will remove duplicates
                    continue
                else:
                    self.templines.append(line)
        try:
            self.c.execute("""
                DELETE FROM zones
                WHERE name LIKE ?
                """,[zone.name])
            self.db.commit()
        except Exception, e:
            errormsg = u"Unsuccessful database delete transaction:" + str(e)
            log.exception(errormsg, self.__class__.__name__)
                
    def convertResults(self,results):
        data = []
        for row in results:
            data.append(ZoneEntry(row[0],row[1],row[2],row[3]))
        return data

    def getNewSerial(self):
        return str(int(self.getSerial())+1)
                    
    def getSerial(self):
        for line in self.lines:
            for s in self.serial:
                if s in line or s.upper() in line or s.lower() in line:
                    result = line.strip().split(";")[0]
                    return result
    def updateSerial(self):
        for i, line in enumerate(self.lines):
            for s in self.serial:
                if s in line or s.upper() in line or s.lower() in line:
                    result = line.strip().split(";")[0]
                    if len(result) > 1:
                        newserial = str(int(result)+1)+";Serial\n"
                        self.lines[i] = newserial
