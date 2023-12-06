from model.DatabasePool import DatabasePool

class User:
    @classmethod
    def register(cls, email, username, password, dob, phone_number, country, preferred_language, gender):
        try:
            dbConn=DatabasePool.getConnection()
            db_Info = dbConn.connection_id
            print(f"Connected to {db_Info}");


            cursor = dbConn.cursor(dictionary=True)
            sql="INSERT INTO users (email, username, password, dob, phone_number, country, preferred_language, gender) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"

            cursor.execute(sql,(email, username, password, dob, phone_number, country, preferred_language, gender))
            dbConn.commit() 

            userID = cursor.lastrowid
            return userID

        finally:
            dbConn.close()
            print("release connection")

    @classmethod
    def user_exists(cls, username):
        try:
            dbConn = DatabasePool.getConnection()
            cursor = dbConn.cursor(dictionary=True)

            sql = "SELECT * FROM users WHERE username = %s"
            cursor.execute(sql, (username,))

            existing_user = cursor.fetchone()

            return existing_user is not None

        finally:
            dbConn.close()
