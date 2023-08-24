from collections import defaultdict
from .Database import DataBase
from .Person import Person
from .Ad import Ad
from pyrogram.types import  InlineKeyboardButton , InlineKeyboardMarkup


def my_tree():
    return defaultdict(my_tree)

class Handler():
    _DB = DataBase()
    _userPocket = my_tree()
    _channels = ["test_robot_ch"]

    onStartMSG = """Hello ! welcome to our Advertising Bot.
    please choose your language     

    
    سلام! به ربات فروشگاهی ما خوش آمدید.
    لطفا زبان خود را انتخاب کنید
    """

    chooseLangButton = InlineKeyboardMarkup(
        [[InlineKeyboardButton(text = "فارسی" , callback_data="Fa"),
        InlineKeyboardButton(text = "English" , callback_data="En")]])

    choosedLangAnswer = {"Fa" : "زبان فارسی به عنوان زبان پیشفرض انتخاب شد" ,
                    "En" : "English choosed as your default language"}
    
    joinCheckerMessage ={"Fa" : " برای فعال شدن همه امکانات ربات لطفا در کانال های زیر عضو شوید سپس روی گزینه عضو شدم کلیک کنید" ,
                    "En" : "for more futures , please join to below channels . then click on joined button"}
    
    def get_phoneNumber_message(self , name):

        return {"Fa" : f"{name} عزیز لطفا شماره تلفن همراه خود را وارد نمایید " ,
                    "En" : f"dear {name} , please enter your phone number"}
    
    userPannelButton = {
        "Fa" : InlineKeyboardMarkup(
        [
        [InlineKeyboardButton(text = "ویرایش سن" , callback_data="editAge"),
        InlineKeyboardButton(text = "ویرایش شماره موبایل" , callback_data="editPhone")],
        [InlineKeyboardButton(text = "نمایش آگهی های ثبت شده شما" , callback_data="showUserAds")],
        [InlineKeyboardButton(text = "ثبت آگهی جدید" , callback_data="submitNewAd")],
        [InlineKeyboardButton(text = "جستجوی آگهی" , callback_data="searchAd")],
        [InlineKeyboardButton(text = "ارسال پیام به ادمین" , callback_data="sendMessageToAdmin")]
        ]
        ),
        "En" : InlineKeyboardMarkup(
        [
        [InlineKeyboardButton(text = "edit age" , callback_data="editAge"),
        InlineKeyboardButton(text = "edit Phone number" , callback_data="editPhone")],
        [InlineKeyboardButton(text = "show your submited ads" , callback_data="showUserAds")],
        [InlineKeyboardButton(text = "submit new ad" , callback_data="submitNewAd")],
        [InlineKeyboardButton(text = "search in all ads" , callback_data="searchAd")],
        [InlineKeyboardButton(text = "send message to admin" , callback_data="sendMessageToAdmin")]
        ]
        )
    }
    
    userPannelMessage = {"Fa" : "لطفا یکی از دکمه های زیر را انتخاب نمایید" ,
                    "En" : "please choose on of the below buttons"}

    phoneNotValidMessage = {"Fa" : "فرمت شماره موبایل وارد شده صحیح نمی باشد. لطفا مجددا تلاش کنید" ,
                    "En" : "phone number format is not valid. please try again"}

    getAgeMessage = {"Fa" : "لطفا سن خود را به صورت عدد در پیام بعدی وارد کنید" ,
                    "En" : "please enter your age just as a number"}
    
    ageNotValidMessage = {"Fa" : "سن وارد شده معتبر نمی باشد لطفا مجددا تلاش کنید" ,
                    "En" : "age not valid ! pelase try again"}

    signUpSuccesMessage = {"Fa" : "ثبت نام شما با موفقیت انجام شد" ,
                    "En" : "signup finnished succesfully !"}
    
    joinedSuccesfullyMessage = {"Fa" : "عضویت شما تایید شد" ,
                    "En" : "Your membership has been accepted"}
    
    joinNotSuccesMessage = {"Fa" : "!شما هنوز در کانال های ما عضو نشده اید" ,
                    "En" : "you are not joined in all channels"}

    userPannelMessage = {"Fa" : "برای استفاده از هرکدام از امکانات زیر بر روی دکمه مورد نظر کلیک کنید" ,
                    "En" : "for any future , please click on it's button"}

    def add_channel(self , newChannel):
        if newChannel not in self._channels:
            self._channels.append(newChannel)

    
    def get_channels_buttons(self):
        buttons = []
        for i in range(len(self._channels)):
            buttons.append([InlineKeyboardButton(f"Channel {i+1}",url = f"https://t.me/{self._channels[i]}")])
        buttons.append([InlineKeyboardButton("عضو شدم | joined" , "joined")])
        return InlineKeyboardMarkup(buttons)


shopBot = Handler()