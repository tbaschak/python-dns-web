#!/usr/bin/python
"""
The MIT License (MIT)

Copyright (c) <2012> <Olav Groenaas Gjerde>

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in 
the Software without restriction, including without limitation the rights to 
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER 
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THEal USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

"""
Use this to launch with uwsgi.
"""

import os, sys
import inspect
from base import app, log
import logging
from service.dnsfilehandler import DNSFileHandler
from uwsgidecorators import *


for controller in os.listdir(os.getcwd()+"/controllers"):
    module_name, ext = os.path.splitext(controller)
    if module_name.endswith('_controller') and ext == '.py':
        __import__("controllers.%s" % (module_name))
        
@timer(30, target='spooler')
def job1(signum):
    dnshandler = DNSFileHandler()
    dnshandler.zonefileJob()

app.config.from_object('base.config.ProductionConfig')
logging.basicConfig(filename=app.config["LOGFILE"],level=logging.DEBUG)




