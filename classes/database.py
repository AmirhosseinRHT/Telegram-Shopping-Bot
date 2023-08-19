import sqlite3

class DataBase(object):
    adminsID = []
    def __init__(self) :
        connection = sqlite3.connect("ShopDatabase.db")
        cur = connection.cursor()

        cur.execute('''CREATE TABLE IF NOT EXISTS users
                    (telegramID TEXT PRIMARY KEY,
                     telegramUsername TEXT,
                     name TEXT,
                     phoneNum TEXT,
                     age INTEGER,
                     joinDate TEXT ,
                     isAdmin INT,
                     numOfActiveAds INT
                    )''')
        
        cur.execute('''CREATE TABLE IF NOT EXISTS ads
                     (userID TEXT,
                     AdID TEXT PRIMARY KEY,
                     Title TEXT,
                     sentDate TEXT,
                     Price INT,
                     NumOfPhotos INTEGER
                    )''')
        
        connection.commit()
        connection.close()



    def add_admin(self , adminTelegramID):
        if adminTelegramID not in self.adminsID:
            self.adminsID.append(adminTelegramID)



    def remove_admin(self , adminTelegramID):
        if adminTelegramID in self.adminsID:
            self.adminsID.remove(adminTelegramID)
    


    def add_new_user(self , telID  , name , isAdmin,joinDate ,telUsername = None , phone = None , age = None ):
        try:
            connection = sqlite3.connect("ShopDatabase.db")
            cur = connection.cursor()

            cur.execute("SELECT COUNT(*) FROM users WHERE telID = ?", (telID,))
            result = cur.fetchone()

            if result[0] == 0:
                cur.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?, ?)", 
                        (telID, telUsername, name, phone, age,joinDate, isAdmin, 0))
                connection.commit()
            else:
                raise sqlite3.Error
            connection.close()
        except sqlite3.Error as error:
            print("Failed to add user:", error)



    def add_new_ad(self ,telegramID, adID , title ,sentDate ,price , numOfPhotos):
        try:
            connection = sqlite3.connect("ShopDatabase.db")
            cur = connection.cursor()

            cur.execute("SELECT COUNT(*) FROM ads WHERE adID = ?", (adID))
            result = cur.fetchone()

            if result[0] == 0:
                cur.execute("INSERT INTO ads VALUES (?, ?, ?, ?, ?, ?)", 
                        (telegramID, adID, title, sentDate,price, numOfPhotos))
                connection.commit()
            else:
                raise sqlite3.Error
            connection.close()
        except sqlite3.Error as error:
            print("Failed to add ad:", error)



    def remove_ad(self , telegramID , adID):
        try:
            connection = sqlite3.connect("ShopDatabase.db")
            cur = connection.cursor()
            tempId = adID.split("_")
            if telegramID in self.adminsID or tempId == telegramID :
                cur.execute("DELETE FROM ads WHERE AdID = ?"  , (adID , ))               
                connection.commit()
            else:
                connection.close()
                raise sqlite3.Error("permission denied to remove!")
        except sqlite3.Error as error:
            print("Failed to remove ad:", error)



    def get_ad_by_telegramID(self , telegramID , adID):
        try: 
            connection = sqlite3.connect("ShopDatabase.db")
            cur = connection.cursor()
            # Query the database to select the ad based on the telegramID and adID
            cur.execute('''SELECT * FROM ads WHERE AdID = ?''', (adID,))
            data = cur.fetchone()  # Fetch the first row of the result
            connection.close()

            tempId  , temp2= adID.split("_")
            if telegramID in self.adminsID or tempId == telegramID :
                dictionary = {
                "userID" : data[0],
                "AdID": data[1],
                "Title": data[2],
                "sentDate": data[3],
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
            connection = sqlite3.connect("ShopDatabase.db")
            cur = connection.cursor()
            cur.execute('''SELECT * FROM ads WHERE userID = ?''', (telegramID,))
            data = cur.fetchall() 
            connection.close()
            dataList =[]
            if data:
                tempId = data[0].split("_")
                if telegramID in self.adminsID or data[0][0] == telegramID :
                    for i in range(len(data)):
                        dictionary = {
                        "userID" : data[i][0],
                        "AdID": data[i][1],
                        "Title": data[i][2],
                        "sentDate": data[i][3],
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
            connection = sqlite3.connect("ShopDatabase.db")
            cur = connection.cursor()
            cur.execute("SELECT * FROM users WHERE telegramID=?", (telegramID,))
            row = cur.fetchone()
            connection.close()
            if row:
                if requestedUserId in self.adminsID:
                    user_data = {
                    "telegramID": row[0],
                    "telegramUsername": row[1],
                    "name": row[2],
                    "phoneNum": row[3],
                    "age": row[4],
                    "joinDate": row[5],
                    "isAdmin": row[6],
                    "numOfActiveAds": row[7]
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
        connection = sqlite3.connect("ShopDatabase.db")
        cur = connection.cursor()
        tempID , temp= adID.split("_")
        if telegramID == tempID or telegramID in self.adminsID:
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
        connection = sqlite3.connect("ShopDatabase.db")
        cur = connection.cursor()
        tempID , temp= adID.split("_")
        if telegramID == tempID or telegramID in self.adminsID:
            cur.execute("UPDATE ads SET Title = ? WHERE AdID = ?" , (newTitle, adID))
            connection.commit()
        else:
            raise sqlite3.Error("permission denied!")
        connection.close()
        return True
    except sqlite3.Error as error:
            print("Error while editing ad title:", error)
            return False
    

db = DataBase()