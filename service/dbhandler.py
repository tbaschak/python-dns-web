
from pysqlite2 import dbapi2 as sqlite3
from base import app, log

class DBHandler:
    
    def __init__(self, dbname):
        self.connection = sqlite3.connect(dbname)
        self.cursor = self.connection.cursor()
        self.connection.row_factory = sqlite3.Row
        self.execute("""
            create table if not exists
            zones(name varchar, ip varchar, updated boolean)
        """)
            
    def __del__(self):
        self.connection.close()
        
    def getConnection(self):
        return self.connection
    
    def commit(self):
        self.connection.commit()
    
    def getCursor(self):
        return self.cursor
    
    def execute(self, query):
        try:
            self.cursor.execute(query)
            self.connection.commit()
            return True
        except:
            return False
        
    def exists(self, table, column, value):
        self.execute("""
            SELECT 1 FROM %s WHERE %s LIKE '%s'
        """%(table,column,value))
        for row in self.cursor:
            if row[0] == 1:
                return True
        return False