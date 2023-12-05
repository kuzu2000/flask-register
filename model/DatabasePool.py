from mysql.connector import pooling

class DatabasePool:
    connection_pool = pooling.MySQLConnectionPool(
                               pool_name="ws_pool",
                               pool_size=5,
                               host='localhost',
                               database='flask-register',
                               user='swanthuzaw',
                               password='swanthuzaw123@')

    @classmethod
    def getConnection(cls): 
        dbConn = cls.connection_pool.get_connection()
        return dbConn