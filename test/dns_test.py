
import os
import unittest
import tempfile
from base import app

class DNSTest(unittest.TestCase):
    
    def setUp(self):
        print "setup"

    def tearDown(self):
        print "teardown"
        
    def test_empty_db(self):
        rv = app.get('/')
        print rv
        assert 'No entries here so far' in rv.data
