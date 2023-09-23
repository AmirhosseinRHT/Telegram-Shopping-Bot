import sqlite3

class DataBase(object):
    _DataBasePATH = "Database/ShopDatabase.db"

    def __init__(self) :
        connection = sqlite3.connect(self._DataBasePATH)
        cur = connection.cursor()

        cur.execute('''CREATE TABLE IF NOT EXISTS users
                    (telegramID TEXT PRIMARY KEY,
                     telegramUsername TEXT,
                     name TEXT,
                     phoneNum TEXT,
                     age INTEGER,
                     joinDate TEXT ,
                     isAdmin INT,
                     isBanned INT,
                     lang TEXT,
                     numOfActiveAds INT
                    )''')
        
        cur.execute('''CREATE TABLE IF NOT EXISTS ads
                    (userID TEXT,
                     adID TEXT,
                     saveID TEXT,
                     title TEXT,
                     photoID TEXT,
                     submitDate TEXT,
                     price INT,
                    views INT
                    )''')
        
        connection.commit()
        connection.close()

    def __repr__(self):
        info = """A simple Database class based on SQLite3 with users & ads table
        some functions are initiaized to add ,remove and edit data from database!"""
        return info
    

    def edit_user_name(self , telegramID , newName):
        try:
            connection = sqlite3.connect(self._DataBasePATH)
            cur = connection.cursor()
            cur.execute("UPDATE users SET name = ? WHERE telegramID = ?" , (newName, telegramID))
            connection.commit()
            connection.close()
            return True
        except sqlite3.Error as error:
                print("Error while editing name:", error)
                return False


    def edit_user_Age(self , telegramID , newAge):
        try:
            connection = sqlite3.connect(self._DataBasePATH)
            cur = connection.cursor()
            cur.execute("UPDATE users SET age = ? WHERE telegramID = ?" , (newAge, telegramID))
            connection.commit()
            connection.close()
            return True
        except sqlite3.Error as error:
                print("Error while editing age:", error)
                return False


    def edit_user_lang(self , telegramID , newLang):
        try:
            connection = sqlite3.connect(self._DataBasePATH)
            cur = connection.cursor()
            cur.execute("UPDATE users SET lang = ? WHERE telegramID = ?" , (newLang, telegramID))
            connection.commit()
            connection.close()
            return True
        except sqlite3.Error as error:
            print("Error while editing language:", error)
            return False
        

    def edit_user_PhoneNumber(self , telegramID , newNumber):
        try:
            connection = sqlite3.connect(self._DataBasePATH)
            cur = connection.cursor()
            cur.execute("UPDATE users SET phoneNum = ? WHERE telegramID = ?" , (newNumber, telegramID))
            connection.commit()
            connection.close()
            return True
        except sqlite3.Error as error:
            print("Error while editing Phone number:", error)
            return False


    def edit_user_level(self , adminTelegramID , level):
        try:
            connection = sqlite3.connect(self._DataBasePATH)
            cur = connection.cursor()
            cur.execute("UPDATE users SET isAdmin = ? WHERE telegramID = ?" , (level, adminTelegramID))
            connection.commit()
            connection.close()
            return True
        except sqlite3.Error as error:
            print("Error while user level:", error)
            return False


    def get_all_admins(self):
        try: 
            connection = sqlite3.connect(self._DataBasePATH)
            cur = connection.cursor()
            cur.execute('''SELECT * FROM users WHERE isAdmin = ?''', (1,))
            data = cur.fetchall()
            admins = [int(admin[0]) for admin in data]
            cur.execute('''SELECT * FROM users WHERE isAdmin = ?''', (2,))
            data = cur.fetchall()
            owners = [int(owner[0]) for owner in data]
            connection.close()
            return owners , admins
        except sqlite3.Error as error:
            print("Failed to load admins:", error)
            return None


    def add_new_user(self , telID  , name , isAdmin,joinDate,lang ,telUsername = None , phone = None , age = None ):
        try:
            connection = sqlite3.connect(self._DataBasePATH)
            cur = connection.cursor()
            cur.execute("SELECT COUNT(*) FROM users WHERE telegramID = ?", (telID,))
            result = cur.fetchone()

            if result[0] == 0:
                cur.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 
                        (telID, telUsername, name, phone, age,joinDate, isAdmin, 0 ,lang, 0))
                connection.commit()
                return True
            else:
                connection.close()
                return False
        except sqlite3.Error as error:
            print("Failed to add user:", error)
            return False


    def add_new_ad(self ,telegramID, adID ,messageID,title ,photoID,submitDate ,price):
        try:
            connection = sqlite3.connect(self._DataBasePATH)
            cur = connection.cursor()
            cur.execute("SELECT COUNT(*) FROM ads WHERE adID = ?", (adID,))
            result = cur.fetchone()
            if result[0] == 0:
                cur.execute("INSERT INTO ads VALUES (?, ?, ?, ?, ? , ?, ? , ?)", 
                        (telegramID, adID , messageID ,title,photoID, submitDate,price , 0))
                cur.execute("SELECT numOfActiveAds FROM users WHERE telegramID = ?", (telegramID,))
                result = cur.fetchone()
                if result is None:
                    connection.close()
                    return False
                else:
                    current_count = int(result[0])
                    new_count = current_count + 1
                    cur.execute("UPDATE users SET numOfActiveAds = ? WHERE telegramID = ?", (str(new_count), telegramID))
                    connection.commit()
                return True
            else:
                connection.close()
                raise sqlite3.Error
        except sqlite3.Error as error:
            print("Failed to add ad:", error)
            return False


    def get_num_of_user_ads(self , telegramID):
        try:
            connection = sqlite3.connect(self._DataBasePATH)
            cur = connection.cursor()
            cur.execute("SELECT COUNT(*) FROM ads WHERE userID = ?", (telegramID,))
            result = cur.fetchone()
            return int(result[0])
        except sqlite3.Error as error:
            print("Failed to retrun count of user ad:", error)
            return None


    def get_ad_by_adID(self , adID):
        try: 
            connection = sqlite3.connect(self._DataBasePATH)
            cur = connection.cursor()
            cur.execute('''SELECT * FROM ads WHERE adID = ?''', (adID,))
            data = cur.fetchone() 
            connection.close()
            if data:
                dictionary = {
                "userID" : data[0],
                "adID": data[1],
                "saveID" : data[2],
                "title": data[3],
                "photoID" : data[4],
                "submitDate": data[5],
                "price": data[6],
                "views" : data[7]
                }
            else:
                return None
        except sqlite3.Error as error:
            print("Failed to get ad:", error)
            return None
        return dictionary
    

    def get_all_ads_by_telegramID(self , telegramID):
        try: 
            connection = sqlite3.connect(self._DataBasePATH)
            cur = connection.cursor()
            cur.execute('''SELECT * FROM ads WHERE userID = ?''', (telegramID,))
            data = cur.fetchall() 
            connection.close()
            dataList =[]
            if data:
                for i in range(len(data)):
                    dictionary = {
                    "userID" : data[i][0],
                    "adID": data[i][1],
                    "saveID" : data[i][2],
                    "title": data[i][3],
                    "photoID" : data[i][4],
                    "submitDate": data[i][5],
                    "price": data[i][6],
                    "views" : data[i][7]
                    }
                    dataList.append(dictionary)
            else:
                return None
        except sqlite3.Error as error:
            print("Failed to get ad:", error)
            return None
        return dataList


    def get_all_users_age_and_phone(self):
        try: 
            connection = sqlite3.connect(self._DataBasePATH)
            cur = connection.cursor()
            cur.execute('''SELECT * FROM users''')
            data = cur.fetchall()
            connection.close()
            dataList =[]
            if data:
                for i in range(len(data)):
                    dictionary = {
                    "telegramID" : int(data[i][0]),
                    "age": int(data[i][4]),
                    "phoneNum": data[i][3],
                    "isAdmin" : int(data[i][6]),
                    "isBanned" : int(data[i][7]),
                    "lang" : data[i][8]
                    }
                    dataList.append(dictionary)
            else:
                return {}
        except sqlite3.Error as error:
            print("Failed to get users:", error)
            return {}
        return dataList


    def get_user_by_telegramID(self , telegramID):
        try:
            connection = sqlite3.connect(self._DataBasePATH)
            cur = connection.cursor()
            cur.execute("SELECT * FROM users WHERE telegramID = ?", (telegramID,))
            row = cur.fetchone()
            connection.close()
            if row:
                user_data = {
                "telegramID": row[0],
                "telegramUsername": row[1],
                "name": row[2],
                "phoneNum": row[3],
                "age": row[4],
                "joinDate": row[5],
                "isAdmin": int(row[6]),
                "isBanned": row[7],
                "lang" : row[8],
                "numOfActiveAds": row[9]
                }
                return user_data
            else:
                return None
        except sqlite3.Error as error:
            print("Error while retrieving user data:", error)
            return None

    
    def get_user_by_PhoneNum(self , phoneNumber):
        try:
            connection = sqlite3.connect(self._DataBasePATH)
            cur = connection.cursor()
            cur.execute("SELECT * FROM users WHERE phoneNum = ?", (phoneNumber,))
            rows = cur.fetchall()
            connection.close()
            datas = []
            if rows:
                for row in rows:
                    user_data = {
                    "telegramID": row[0],
                    "telegramUsername": row[1],
                    "name": row[2],
                    "phoneNum": row[3],
                    "age": row[4],
                    "joinDate": row[5],
                    "isAdmin": int(row[6]),
                    "isBanned": row[7],
                    "lang" : row[8],
                    "numOfActiveAds": row[9]
                    }
                    datas.append(user_data)
                return datas
            else:
                return None
        except sqlite3.Error as error:
            print("Error while retrieving user data:", error)
            return None


    
    def get_user_by_telegramUsername(self , username):
        try:
            connection = sqlite3.connect(self._DataBasePATH)
            cur = connection.cursor()
            cur.execute("SELECT * FROM users WHERE telegramUsername = ?", (username,))
            rows = cur.fetchall()
            connection.close()
            datas = []
            if rows:
                for row in rows:
                    user_data = {
                    "telegramID": row[0],
                    "telegramUsername": row[1],
                    "name": row[2],
                    "phoneNum": row[3],
                    "age": row[4],
                    "joinDate": row[5],
                    "isAdmin": int(row[6]),
                    "isBanned": row[7],
                    "lang" : row[8],
                    "numOfActiveAds": row[9]
                    }
                    datas.append(user_data)
                return datas
            else:
                return None
        except sqlite3.Error as error:
            print("Error while retrieving user data:", error)
            return None


    def edit_ad_saveID(self ,adID, newID):
        try:
            connection = sqlite3.connect(self._DataBasePATH)
            cur = connection.cursor()
            cur.execute("UPDATE ads SET saveID = ? WHERE adID = ?" , (newID, adID))
            connection.commit()
            connection.close()
            return True
        except sqlite3.Error as error:
            print("Error while edit ad save id:", error)
            return False
        

    def edit_ad_price(self , adID , newPrice):
        try:
            connection = sqlite3.connect(self._DataBasePATH)
            cur = connection.cursor()
            cur.execute("UPDATE ads SET price = ? WHERE adID = ?" , (newPrice, adID))
            connection.commit()
            connection.close()
            return True
        except sqlite3.Error as error:
                print("Error while editing ad price:", error)
                return False
        

    def edit_ad_PhotoID(self , adID , newPhotoID):
        try:
            connection = sqlite3.connect(self._DataBasePATH)
            cur = connection.cursor()
            cur.execute("UPDATE ads SET photoID = ? WHERE adID = ?" , (newPhotoID, adID))
            connection.commit()
            connection.close()
            return True
        except sqlite3.Error as error:
                print("Error while editing ad Photo:", error)
                return False


    def change_user_ban_status_by_telegramID(self , telegramID , status):
        try:
            connection = sqlite3.connect(self._DataBasePATH)
            cur = connection.cursor()
            cur.execute("UPDATE users SET isBanned = ? WHERE telegramID = ?" , (status, telegramID))
            connection.commit()
            connection.close()
            return True
        except sqlite3.Error as error:
            print("Error while edit blockage status:", error)
            return False


    def edit_ad_title(self , adID , newTitle):
        try:
            connection = sqlite3.connect(self._DataBasePATH)
            cur = connection.cursor()
            cur.execute("UPDATE ads SET title = ? WHERE adID = ?" , (newTitle, adID))
            connection.commit()
            connection.close()
            return True
        except sqlite3.Error as error:
                print("Error while editing ad title:", error)
                return False
        

    def get_all_telegramIDs(self):
        try:
            conn = sqlite3.connect(self._DataBasePATH)  
            cur = conn.cursor()
            cur.execute("SELECT telegramID FROM users")
            telegram_ids = [int(row[0]) for row in cur.fetchall()]
            conn.close()
            return telegram_ids
        except sqlite3.Error as error:
            print("Error while return all telegramIDs:", error)
            return None
    

    def delete_ad_by_AdID(self , adID : str):
        try:
            conn = sqlite3.connect(self._DataBasePATH)  
            cur = conn.cursor()
            cur.execute("DELETE FROM ads WHERE adID = ?", (adID,))
            telegramID , adNum = adID.split("-")
            cur.execute("SELECT numOfActiveAds FROM users WHERE telegramID = ?", (telegramID,))
            result = cur.fetchone()
            if result is None:
                conn.close()
                return False
            current_count = int(result[0])
            new_count = current_count - 1
            cur.execute("UPDATE users SET numOfActiveAds = ? WHERE telegramID = ?", (str(new_count), telegramID))
            conn.commit()
            conn.close()
            return True
        except sqlite3.Error as error:
            print("Error while deleting ad:", error)
            return False
        

    def delete_user_by_telegramID(self , telegramID):
        try:
            conn = sqlite3.connect(self._DataBasePATH)  
            cur = conn.cursor()
            cur.execute("DELETE FROM users WHERE telegramID = ?", (telegramID,))
            cur.execute("DELETE FROM ads WHERE userID = ?", (telegramID,))
            conn.commit()
            conn.close()
            return True
        except sqlite3.Error as error:
            print("Error while deleting user:", error)
            return False

    def find_wanted_ads_by_title(self , value):
        try:
            conn = sqlite3.connect(self._DataBasePATH)  
            cur = conn.cursor()
            cur.execute(f"UPDATE ads SET views = views + 1 WHERE title LIKE '%{value}%'")
            conn.commit()
            cur.execute(f"SELECT * FROM ads WHERE title LIKE '%{value}%'")
            data = cur.fetchall()
            conn.close()
            dataList =[]
            if data:
                for i in range(len(data)):
                    dictionary = {
                    "userID" : data[i][0],
                    "adID": data[i][1],
                    "saveID" : data[i][2],
                    "title": data[i][3],
                    "photoID" : data[i][4],
                    "submitDate": data[i][5],
                    "price": data[i][6],
                    "views" : data[i][7]
                    }
                    dataList.append(dictionary)
                return dataList
            else:
                return None
        except sqlite3.Error as error:
            print("Error while returning records:", error)
            return None