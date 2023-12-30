import mysql.connector

class DatabaseConnection:
    def __init__(self, config):
        self.config = config
        self.connection = None

    def __enter__(self):
        self.connection = mysql.connector.connect(**self.config)
        return self.connection

    def __exit__(self, exc_type, exc_value, traceback):
        if self.connection:
            self.connection.close()
            
config = {
    'user': 'u274908554_713A',#ok
    'password': 'INbd713A',#ok
    'host': 'sql812.main-hosting.eu', #ok
    'database': 'u274908554_713A',#ok
    'port': 3306
}