import sqlite3

class DataBase(object):
    _adminsID = [12345678]
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
                     lang TEXT,
                     numOfActiveAds INT
                    )''')
        
        cur.execute('''CREATE TABLE IF NOT EXISTS ads
                     (userID TEXT,
                     AdID TEXT PRIMARY KEY,
                     Title TEXT,
                     submitDate TEXT,
                     Price INT,
                     NumOfPhotos INTEGER
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
            for i in range(data):
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
                cur.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?, ? , ?)", 
                        (telID, telUsername, name, phone, age,joinDate, isAdmin,lang, 0))
                connection.commit()
                return True
            else:
                connection.close()
                return False
        except sqlite3.Error as error:
            print("Failed to add user:", error)



    def add_new_ad(self ,telegramID, adID , title ,submitDate ,price , numOfPhotos):
        try:
            connection = sqlite3.connect(self._DataBasePATH)
            cur = connection.cursor()

            cur.execute("SELECT COUNT(*) FROM ads WHERE adID = ?", (adID))
            result = cur.fetchone()

            if result[0] == 0:
                cur.execute("INSERT INTO ads VALUES (?, ?, ?, ?, ?, ?)", 
                        (telegramID, adID, title, submitDate,price, numOfPhotos))
                connection.commit()
            else:
                raise sqlite3.Error
            connection.close()
        except sqlite3.Error as error:
            print("Failed to add ad:", error)



    def remove_ad(self , telegramID , adID):
        try:
            connection = sqlite3.connect(self._DataBasePATH)
            cur = connection.cursor()
            tempId = adID.split("_")
            if telegramID in self._adminsID or tempId == telegramID :
                cur.execute("DELETE FROM ads WHERE AdID = ?"  , (adID , ))               
                connection.commit()
            else:
                connection.close()
                raise sqlite3.Error("permission denied to remove!")
        except sqlite3.Error as error:
            print("Failed to remove ad:", error)



    def get_ad_by_telegramID(self , telegramID , adID):
        try: 
            connection = sqlite3.connect(self._DataBasePATH)
            cur = connection.cursor()
            # Query the database to select the ad based on the telegramID and adID
            cur.execute('''SELECT * FROM ads WHERE AdID = ?''', (adID,))
            data = cur.fetchone()  # Fetch the first row of the result
            connection.close()

            tempId  , temp2= adID.split("_")
            if telegramID in self._adminsID or tempId == telegramID :
                dictionary = {
                "userID" : data[0],
                "AdID": data[1],
                "Title": data[2],
                "submitDate": data[3],
                "Price": data[4],
                "NumOfPhotos": data[5]
                }
            else:
                raise sqlite3.Error("permission denied to get ad!")
            
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
                tempId = data[0].split("_")
                if telegramID in self._adminsID or data[0][0] == telegramID :
                    for i in range(len(data)):
                        dictionary = {
                        "userID" : data[i][0],
                        "AdID": data[i][1],
                        "Title": data[i][2],
                        "submitDate": data[i][3],
                        "Price": data[i][4],
                        "NumOfPhotos": data[i][5]
                        }
                        dataList.append[dictionary]
                else:
                    raise sqlite3.Error("permission denied to get ad!")
            else:
                raise sqlite3.Error("no ad found with given userID!")
            
        except sqlite3.Error as error:
            print("Failed to get ad:", error)
            return None
        return dictionary



    def get_user_by_telegramID(self ,requestedUserId, telegramID):
        try:
            connection = sqlite3.connect(self._DataBasePATH)
            cur = connection.cursor()
            cur.execute("SELECT * FROM users WHERE telegramID = ?", (telegramID,))
            row = cur.fetchone()
            connection.close()
            if row:
                if requestedUserId in self._adminsID:
                    user_data = {
                    "telegramID": row[0],
                    "telegramUsername": row[1],
                    "name": row[2],
                    "phoneNum": row[3],
                    "age": row[4],
                    "joinDate": row[5],
                    "isAdmin": row[6],
                    "lang" : row[7],
                    "numOfActiveAds": row[8]
                    }
                    return user_data
                else:
                    raise sqlite3.Error("permission denied!")
            else:
                return None
        except sqlite3.Error as error:
            print("Error while retrieving user data:", error)

               
def edit_ad_price(self , telegramID , adID , newPrice):
    try:
        connection = sqlite3.connect(self._DataBasePATH)
        cur = connection.cursor()
        tempID , temp= adID.split("_")
        if telegramID == tempID or telegramID in self._adminsID:
            cur.execute("UPDATE ads SET Price = ? WHERE AdID = ?" , (newPrice, adID))
            connection.commit()
        else:
            raise sqlite3.Error("permission denied!")
        connection.close()
        return True
    except sqlite3.Error as error:
            print("Error while editing ad price:", error)
            return False



def edit_ad_title(self , telegramID , adID , newTitle):
    try:
        connection = sqlite3.connect(self._DataBasePATH)
        cur = connection.cursor()
        tempID , temp= adID.split("_")
        if telegramID == tempID or telegramID in self._adminsID:
            cur.execute("UPDATE ads SET Title = ? WHERE AdID = ?" , (newTitle, adID))
            connection.commit()
        else:
            raise sqlite3.Error("permission denied!")
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



db = DataBase()