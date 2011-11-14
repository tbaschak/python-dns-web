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
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import os, sys
from base import app
import logging
from service.kronos import ThreadedScheduler
from service.kronos import method
from service.dnshandler import DNSHandler

for controller in os.listdir(os.getcwd()+"/controllers"):
    module_name, ext = os.path.splitext(controller)
    if module_name.endswith('_controller') and ext == '.py':
        module = __import__("controllers.%s" % (module_name))

class MainApplication:
    @staticmethod
    def run():
        if len(sys.argv) > 1:
            if sys.argv[1] == ("dev"):
                app.config.from_object('base.config.DevelopmentConfig')
            elif sys.argv[1] == "test":
                app.config.from_object('base.config.TestingConfig')
        if len(sys.argv) == 1 or sys.argv[1] == "prod" or None:
            app.config.from_object('base.config.ProductionConfig')
        logging.basicConfig(filename=app.config["LOGFILE"],level=logging.DEBUG)
        MainApplication.initJob1()
        app.run(
            app.config["HOST"],
            app.config["PORT"]
        )
        
    @staticmethod
    def initJob1():
        dnshandler = DNSHandler()
        job = ThreadedScheduler()
        job.add_interval_task(
            dnshandler.updateZoneFile, "job1",
            0, 30, method.threaded, None, None)
        job.start()

if __name__ == "__main__":
    MainApplication.run()


