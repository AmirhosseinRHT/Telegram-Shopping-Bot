import sqlite3

class DataBase(object):
    _adminsID = [297411912]
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
        self.load_admins()

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
        except sqlite3.Error as error:
                print("Error while editing Phone number:", error)
                return False


    def add_admin(self , adminTelegramID):
        try:
            connection = sqlite3.connect(self._DataBasePATH)
            cur = connection.cursor()
            cur.execute("UPDATE users SET isAdmin = ? WHERE telegramID = ?" , (1, adminTelegramID))
            connection.commit()
            connection.close()
            if adminTelegramID not in self._adminsID:
                self._adminsID.append(adminTelegramID)
        except sqlite3.Error as error:
            print("Error while add new admin:", error)



    def remove_admin(self , adminTelegramID):
        try:
            connection = sqlite3.connect(self._DataBasePATH)
            cur = connection.cursor()
            cur.execute("UPDATE users SET isAdmin = ? WHERE telegramID = ?" , (0, adminTelegramID))
            connection.commit()
            connection.close()
            if adminTelegramID in self._adminsID:
                self._adminsID.remove(adminTelegramID)
        except sqlite3.Error as error:
            print("Error while remove new admin:", error)
    

    def load_admins(self):
        try: 
            connection = sqlite3.connect(self._DataBasePATH)
            cur = connection.cursor()
            cur.execute('''SELECT * FROM users WHERE isAdmin = ?''', (1,))
            data = cur.fetchall() 
            connection.close()
            for i in range(len(data)):
                if data[i][0] not in self._adminsID:
                    self._adminsID.append(data[0][i])
        except sqlite3.Error as error:
            print("Failed to load admins:", error)
        else:
            print("admins loaded succesfully!")



    def user_available_in_DB(self , telegramID):
        try:
            connection = sqlite3.connect(self._DataBasePATH)
            cur = connection.cursor()
            cur.execute("SELECT COUNT(*) FROM users WHERE telegramID = ?", (telegramID,))
            result = cur.fetchone()
            connection.close()
            if result[0] == 0:
                return False
            else:
                return True
        except sqlite3.Error as error:
            print("Failed to add user:", error)


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
                raise sqlite3.Error
            connection.close()
        except sqlite3.Error as error:
            print("Failed to add ad:", error)


    def get_num_of_user_ads(self , telegramID):
        connection = sqlite3.connect(self._DataBasePATH)
        cur = connection.cursor()
        cur.execute("SELECT COUNT(*) FROM ads WHERE userID = ?", (telegramID,))
        result = cur.fetchone()
        return int(result[0])



    def remove_ad(self , telegramID , adID):
        try:
            connection = sqlite3.connect(self._DataBasePATH)
            cur = connection.cursor()
            tempId = adID.split("_")
            cur.execute("DELETE FROM ads WHERE adID = ?"  , (adID , ))               
            connection.commit()
            connection.close()
        except sqlite3.Error as error:
            print("Failed to remove ad:", error)



    def get_ad_by_adID(self , adID):
        try: 
            connection = sqlite3.connect(self._DataBasePATH)
            cur = connection.cursor()
            cur.execute('''SELECT * FROM ads WHERE adID = ?''', (adID,))
            data = cur.fetchone() 
            connection.close()
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
                "isAdmin": row[6],
                "isBanned": row[7],
                "lang" : row[8],
                "numOfActiveAds": row[9]
                }
                return user_data
            else:
                return None
        except sqlite3.Error as error:
            print("Error while retrieving user data:", error)

               
    def edit_ad_saveID(self ,adID, newID):
        connection = sqlite3.connect(self._DataBasePATH)
        cur = connection.cursor()
        cur.execute("UPDATE ads SET saveID = ? WHERE adID = ?" , (newID, adID))
        connection.commit()
        connection.close()

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


    def ban_user_by_Phone(self , number):
        connection = sqlite3.connect(self._DataBasePATH)
        cur = connection.cursor()
        cur.execute("UPDATE users SET isBanned = ? WHERE phoneNum = ?" , (1, number))
        connection.commit()
        connection.close()
        return True
    
    def ban_user_by_telegramID(self , telegramID):
        connection = sqlite3.connect(self._DataBasePATH)
        cur = connection.cursor()
        cur.execute("UPDATE users SET isBanned = ? WHERE telegramID = ?" , (1, telegramID))
        connection.commit()
        connection.close()
        return True


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
        conn = sqlite3.connect(self._DataBasePATH)  
        cur = conn.cursor()
        cur.execute("SELECT telegramID FROM users")
        telegram_ids = [row[0] for row in cur.fetchall()]
        conn.close()
        return telegram_ids


    def get_all_admins(self):
        return self._adminsID
    
    def delete_ad_by_AdID(self , adID: str):
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
