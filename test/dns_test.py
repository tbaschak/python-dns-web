
import os
import unittest
import tempfile
from base import app
from service.dnshandler import DNSHandler

class DNSTest(unittest.TestCase):
    
    def setUp(self):
        self.dh = DNSHandler()

    def tearDown(self):
        del(self.dh)
        
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
