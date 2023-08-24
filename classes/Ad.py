import datetime

class Ad():
    def __init__(self , telegramID , adID , Title , Price , numOfPhotos):
        self._telegramID = telegramID
        self._adID = adID
        self._title = Title
        self._price = Price
        self._numOfPhotos = numOfPhotos
        self._submitDate = str(datetime.datetime.now())[:19]
    
    def set_title(self , newTitle):
        self._title = newTitle

    def set_price(self , newPrice):
        self._price = newPrice
    
    def change_numOfPhotos(self , newNumber):
        self._numOfPhotos = newNumber

