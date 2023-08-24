import datetime

class Person():
    
    def __init__(self,Fname , Lname,telegramUserID, language, telegramUsername = None ,phoneNumber = None):
        self.set_name(Fname , Lname)
        self._telegramUserID = telegramUserID
        self._isAdmin = 0
        self._telegramUsername = telegramUsername
        self._phoneNumber = phoneNumber
        self._age = 0
        self._lang = language
        self._activeAds = 0
        self._joinDate = str(datetime.datetime.now())[:19]
        self.authStep = 0

    def set_step(self , newStep):
        self.authStep = newStep
    
    def set_age(self , newAge):
        self._age = newAge

    def set_name(self, Fname , Lname):
        if Fname == "None":
            self._name = Lname
        elif Lname == "None":
            self._name = Fname
        else:
            self._name = Fname + " " + Lname


    def set_language(self, newLang):
        self._lang = newLang

    def __repr__(self) -> str:
        return f""" name = {self._name} \n userID = {self._telegramUserID} \n phone = {self._phoneNumber}
          usernameID = {self._telegramUsername} \n  lang = {self._lang} \n"""
