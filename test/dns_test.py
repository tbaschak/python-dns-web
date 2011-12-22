
import os
import shutil
import unittest
import tempfile
from base import app
from service.dnshandler import DNSHandler
from service.dnsfilehandler import DNSFileHandler
from service.dbhandler import DBHandler

class DNSTest(unittest.TestCase):
    
    def setUp(self):
        self.dh = DNSHandler()
        self.dfh = DNSFileHandler()
        self.db = DBHandler(app.config["DBFILE"])
        self.c = self.db.getCursor()

    def tearDown(self):
        del(self.dh)
        del(self.dfh)
        del(self.db)
        del(self.c)
        
    def test_crud_operations(self):
        # Test add
        result = self.dh.add("olavtest", "192.168.1.1")
        assert result["message"] == u"Entry olavtest inserted"
        assert result["success"] == True
        # Test duplicate
        result = self.dh.add("olavtest", "192.168.1.1")
        assert result["error"] == u"Duplicate name entry in db"
        assert result["success"] == False
        
        # Test edit name
        # Test duplicate
        result = self.dh.editName("olavtest", "olavtest")
        assert result["error"] == u"Name entry is the same as existing name"
        assert result["success"] == False
        # Test not found
        result = self.dh.editName("testtest", "olavtest2")
        assert result["error"] == u"No old name entry in db"
        assert result["success"] == False
        # Test update
        result = self.dh.editName("olavtest", "olavtest2")
        assert result["message"] == u"Entry olavtest2 updated from olavtest"
        assert result["success"] == True
        
        # Edit ip
        # Test duplicate
        result = self.dh.editHost("olavtest2", "192.168.1.1")
        assert result["error"] == u"Host entry is the same as existing name"
        assert result["success"] == False
        # Test update
        result = self.dh.editHost("olavtest2", "192.168.1.2")
        msg = u"Entry 192.168.1.2 updated from 192.168.1.1"
        assert result["message"] == msg
        assert result["success"] == True
        
        # Test delete
        # Test not existing name
        result = self.dh.delete("olavtest")
        assert result["error"] == u"Entry olavtest not found"
        assert result["success"] == False
        # Test delete
        result = self.dh.delete("olavtest2")
        assert result["message"] == u"Entry olavtest2 deleted"
        assert result["success"] == True
        
    def test_file_operations(self):
        shutil.copy2( "example.org", app.config["ZONEFILE"] )
        # Test add
        self.dh.add("olavfiletest", "192.168.1.1")
        self.dh.add("olavfiletest2", "test.example.org")
        
        results = list(self.c.execute("""
            SELECT name, host, update_type, old_value FROM zones
            WHERE updated = 1
            """,[]))
        self.dfh.updateZonefile(self.dfh.convertResults(results))
            
        lineFound = [False,False]
        for line in self.dfh.lines:
            if u"olavfiletest\tIN\tA\t192.168.1.1\n" == line:
                lineFound[0] = True
            if u"olavfiletest2\tIN\tCNAME\ttest.example.org\n" == line:
                lineFound[1] = True
                
        for status in lineFound:
            assert status is True
            
        # Test modify name
        self.dh.editName("olavfiletest", "olavfiletest3")
        self.dh.editName("olavfiletest2", "olavfiletest4")
        
        results = list(self.c.execute("""
            SELECT name, host, update_type, old_value FROM zones
            WHERE updated = 1
            """,[]))
        self.dfh.updateZonefile(self.dfh.convertResults(results))
            
        lineFound = [False,False]
        for line in self.dfh.lines:
            if u"olavfiletest3\tIN\tA\t192.168.1.1\n" == line:
                lineFound[0] = True
            if u"olavfiletest4\tIN\tCNAME\ttest.example.org\n" == line:
                lineFound[1] = True
                
        for status in lineFound:
            assert status is True
        
        # Edit ip
        self.dh.editHost("olavfiletest3", "test.example.org")
        self.dh.editHost("olavfiletest4", "192.168.1.2")
        
        results = list(self.c.execute("""
            SELECT name, host, update_type, old_value FROM zones
            WHERE updated = 1
            """,[]))
        self.dfh.updateZonefile(self.dfh.convertResults(results))
        
        lineFound = [False,False]
        for line in self.dfh.lines:
            if u"olavfiletest3\tIN\tCNAME\ttest.example.org\n" == line:
                lineFound[0] = True
            if u"olavfiletest4\tIN\tA\t192.168.1.2\n" == line:
                lineFound[1] = True
                
        for status in lineFound:
            assert status is True
        
        # Test delete
        self.dh.delete("olavfiletest4")
        results = list(self.c.execute("""
            SELECT name, host, update_type, old_value FROM zones
            WHERE updated = 1
            """,[]))
        self.dfh.updateZonefile(self.dfh.convertResults(results))
        
        lineFound = [False]
        for line in self.dfh.lines:
            if u"olavfiletest4\tIN\tA\t192.168.1.2\n" == line:
                lineFound[0] = True
                
        for status in lineFound:
            assert status is False
