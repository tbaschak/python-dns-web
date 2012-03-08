
from base import app, log
from model.zoneentry import ZoneEntry
from service.dbhandler import DBHandler
from service.dnsfilehandler import DNSFileHandler
import traceback
import fileinput
import sys
import os

class DNSHandler:
    
    def __init__(self):
        pass
        
    def add(self, name, host):
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
                    INSERT INTO zones(name,host,updated,update_type)
                    VALUES(?,?,1,'CREATE')
                           """,[name,host])
                db.commit()
                data["success"] = True
                data["message"] = u"Entry %s inserted"%(name)
            except Exception, e:
                errormsg = u"Unsuccessful database insert transaction:" + str(e)
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
                SET old_value = name, name = ?,
                updated = 1, update_type = 'MODIFIED NAME'
                WHERE name LIKE ?
                """,[toName, fromName])
            db.commit()
            data["success"] = True
            data["message"] = u"Entry %s updated from %s"%(toName, fromName)
        except Exception, e:
            errormsg = u"Unsuccessful database update transaction:" + str(e)
            log.exception(errormsg, self.__class__.__name__)
            data["success"] = False
            data["error"] = errormsg
        return data
    
    def editHost(self, name, host):
        data = {}
        db = DBHandler(app.config["DBFILE"])
        c = db.getCursor()
        dbdata = list(c.execute("""
            SELECT host FROM zones
            WHERE name LIKE ?
            """,[name]))
        if len(dbdata) == 0:
            data["error"] = u"Zone doesn't exist"
            data["success"] = False
            return data
        else:
            zone = dbdata[0]
        if zone[0] == host:
            data["error"] = u"Host entry is the same as existing name"
            data["success"] = False
            return data
        try:
            c.execute("""
                UPDATE zones
                SET host = ?, updated = 1, update_type = 'MODIFIED HOST'
                WHERE name LIKE ?
                """,[host,name])
            db.commit()
            data["success"] = True
            data["message"] = u"Entry %s updated from %s"%(host, zone[0])
        except Exception, e:
            errormsg = u"Unsuccessful database update transaction:" + str(e)
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
                    SET updated = 1, update_type = 'DELETE'
                    WHERE name LIKE ?
                    """,[name])
                db.commit()
                data["success"] = True
                data["message"] = u"Entry %s deleted"%(name)
            except Exception, e:
                errormsg = u"Unsuccessful database delete transaction:" + str(e)
                log.exception(errormsg, self.__class__.__name__)
                data["success"] = False
                data["error"] = errormsg
        else:
            data["success"] = False
            data["error"] = u"Entry %s not found"%(name)
        return data
    