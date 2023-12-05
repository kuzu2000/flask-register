from model.DatabasePool import DatabasePool

class User:
    @classmethod
    def register(cls, email, username, password, dob, phone_number):
        try:
            dbConn=DatabasePool.getConnection()
            db_Info = dbConn.connection_id
            print(f"Connected to {db_Info}");


            cursor = dbConn.cursor(dictionary=True)
            sql="INSERT INTO users (email, username, password, dob, phone_number) VALUES (%s, %s, %s, %s, %s)"

            cursor.execute(sql,(email, username, password, dob, phone_number))
            dbConn.commit() 

            userID = cursor.lastrowid
            return userID

        finally:
            dbConn.close()
            print("release connection")