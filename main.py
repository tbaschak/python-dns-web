import os, sys
from base import app
import logging

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
        app.run(
            app.config["HOST"],
            app.config["PORT"]
        )

if __name__ == "__main__":
    MainApplication.run()


