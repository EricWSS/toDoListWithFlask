from db.conector_controller import *

class DBHelper():
    def __init__(self):
        self.connection = None

    def execute(self, sql):
        with DatabaseConnection(config) as connection: #Necessário ao criar método enter.
            cursor = connection.cursor()
            cursor.execute(sql)
            if sql.split()[0].upper() =='SELECT':
                result = list()#ok
                for row in cursor.fetchall():
                    result.append(row)
                connection.commit()
                cursor.close()
                return result
            else:
                connection.commit()
                cursor.close()
                return None