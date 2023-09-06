import datetime

class Ad():
    def __init__(self , telegramID , adID , photoID ,Title , Price ):
        self._telegramID = telegramID
        self._adID = adID
        self._title = Title
        self._price = Price
        self._photoID = photoID

    
    def set_title(self , newTitle):
        self._title = newTitle

    def get_submitDate(self):
        return str(datetime.datetime.now())[:19]
    
    def set_price(self , newPrice):
        self._price = newPrice

    def change_photoID(self , photoID):
        self._photoID = photoID

