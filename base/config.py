class Config(object):
    DEBUG = False
    TESTING = False
    HOST = "0.0.0.0"
    PORT = 8080
    LOGFILE = 'stacktrace.log'
    JSONfile = False
    AUTHPASS = "httppassword"
    ZONEFILE = "/home/olav/example.org"
    DBFILE = "zones.db"

class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    DEBUG = True
    JSONfile = True

class TestingConfig(Config):
    TESTING = True

