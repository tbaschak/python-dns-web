
from pysqlite2 import dbapi2 as sqlite3
from base import app, log

class DBHandler:
    
    def __init__(self, dbname):
        self.connection = sqlite3.connect(dbname)
        self.cursor = self.connection.cursor()
        self.execute("""
            create table if not exists
            zones(name varchar, ip varchar, updated boolean)
        """)
            
    def __del__(self):
        self.connection.close()
        log.debug("HEY DELETED",__name__)
        
    def getConnection(self):
        return self.connection
    
    def getCursor(self):
        return self.cursor
    
    def execute(self, query):
        self.cursor.execute(query)
        self.connection.commit()
        
    def exists(self, table, column, value):
        self.execute("""
            SELECT 1 FROM %s WHERE %s LIKE '%s'
        """%(table,column,value))
        for row in self.cursor:
            if row[0] == 1:
                return True
        return False