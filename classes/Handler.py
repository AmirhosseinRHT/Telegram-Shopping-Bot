from collections import defaultdict
from .Database import DataBase
from pyrogram.types import  InlineKeyboardButton , InlineKeyboardMarkup

def my_tree():
    return defaultdict(my_tree)

class Handler():
    _DB = DataBase()
    _userPocket = my_tree()
    _joinChannels = ["test_robot_ch" , "texxt_musics"]
    _owners = [297411912]
    _admins = []
    saveChannel = "test_robot_ch"

    def __init__(self):
        self._admins = self._DB.get_all_admins()
        for id in self._owners:
            if id not in self._admins:
                self._admins.append(id)


    def add_channel(self , newChannel):
        if newChannel not in self._joinChannels:
            self._joinChannels.append(newChannel)


    def get_channels_buttons(self):
        buttons = []
        for i in range(len(self._joinChannels)):
            buttons.append([InlineKeyboardButton(f"Channel {i+1}",url = f"https://t.me/{self._joinChannels[i]}")])
        buttons.append([InlineKeyboardButton("عضو شدم | joined" , "joined")])
        return InlineKeyboardMarkup(buttons)

    chooseLangButton = InlineKeyboardMarkup(
        [[InlineKeyboardButton(text = "فارسی" , callback_data="Fa"),
        InlineKeyboardButton(text = "English" , callback_data="En")]])
    

    backToPannelButton = {
        "Fa" : InlineKeyboardMarkup(
        [[InlineKeyboardButton(text = "برگشتن به پنل" , callback_data="userPannel"),]]),
        "En" : InlineKeyboardMarkup(
        [[InlineKeyboardButton(text = "back to pannel" , callback_data="userPannel"),]])
    }
    

    messageToAdminButton = {
        "Fa" : InlineKeyboardMarkup(
        [[InlineKeyboardButton(text = "ارسال پیام به ادمین" , callback_data="sendMessageToAdmin"),]]),
        "En" : InlineKeyboardMarkup(
        [[InlineKeyboardButton(text = "send message to admin" , callback_data="sendMessageToAdmin"),]])
    }


    userPannelButton = {
        "Fa" : InlineKeyboardMarkup(
        [
        [InlineKeyboardButton(text = "ویرایش نام" , callback_data="editName"),
         InlineKeyboardButton(text = "ویرایش شماره موبایل" , callback_data="editPhone")],
        [InlineKeyboardButton(text = "نمایش آگهی های ثبت شده شما" , callback_data="showUserAds")],
        [InlineKeyboardButton(text = "ثبت آگهی جدید" , callback_data="submitNewAd")],
        [InlineKeyboardButton(text = "جستجوی آگهی" , callback_data="searchAd")],
        [InlineKeyboardButton(text = "ارسال پیام به ادمین" , callback_data="sendMessageToAdmin")],
        [InlineKeyboardButton(text = "پنل ادمین" , callback_data="adminPannel")]
        ]
        ),
        "En" : InlineKeyboardMarkup(
        [
        [InlineKeyboardButton(text = "edit name" , callback_data="editName"),
         InlineKeyboardButton(text = "edit Phone number" , callback_data="editPhone")],
        [InlineKeyboardButton(text = "show your submited ads" , callback_data="showUserAds")],
        [InlineKeyboardButton(text = "submit new ad" , callback_data="submitNewAd")],
        [InlineKeyboardButton(text = "search in all ads" , callback_data="searchAd")],
        [InlineKeyboardButton(text = "send message to admin" , callback_data="sendMessageToAdmin")],
        [InlineKeyboardButton(text = "admin pannel" , callback_data="adminPannel")]
        ]
        )
    }

    adminPannelButton = {
        "Fa" : InlineKeyboardMarkup(
        [
        [InlineKeyboardButton(text = "جستجوی آگهی" , callback_data="searchAd")],
        [InlineKeyboardButton(text = "دریافت اطلاعات کاربر" , callback_data="getUserInfo"),
        InlineKeyboardButton(text = "ویرایش اطلاعات کاربر" , callback_data="editUser")],
        [InlineKeyboardButton(text = "مسدود سازی کاربر" , callback_data="banUser"),
        InlineKeyboardButton(text = "رفع مسدودیت کاربر", callback_data="unbanUser")],
        [InlineKeyboardButton(text = "حذف آگهی" , callback_data="removeAd")],
        [InlineKeyboardButton(text = "ویرایش آگهی" , callback_data="editAd")],
        [InlineKeyboardButton(text = "ارتقا کاربر به ادمین" , callback_data="promoteToAdmin")],
        [InlineKeyboardButton(text = "ارسال پیام به کاربر" , callback_data="messageToOneUser")],
        [InlineKeyboardButton(text = "ارسال پیام همه کاربران" , callback_data="messageToAllUsers")],
        [InlineKeyboardButton(text = "اضافه کردن کانال جدید", callback_data="addNewChannel"),
        InlineKeyboardButton(text = "حذف کانال", callback_data="removeChannel")],
        [InlineKeyboardButton(text = "حذف همه چت های ربات" , callback_data="deleteAllChats")],
        [InlineKeyboardButton(text = "پنل کاربر" , callback_data="userPannel")],
        ]
        ),
        "En" : InlineKeyboardMarkup(
        [
        [InlineKeyboardButton(text = "search in all ads" , callback_data="searchAd")],
        [InlineKeyboardButton(text = "get user info" , callback_data="getUserInfo"),
        InlineKeyboardButton(text = "edit user info" , callback_data="editUser")],
        [InlineKeyboardButton(text = "Ban user" , callback_data="banUser"),
        InlineKeyboardButton(text = "in Ban user", callback_data="unbanUser")],
        [InlineKeyboardButton(text = "remove ad" , callback_data="removeAd")],
        [InlineKeyboardButton(text = "edit ad" , callback_data="editAd")],
        [InlineKeyboardButton(text = "promote user to admin" , callback_data="promoteToAdmin")],
        [InlineKeyboardButton(text = "message to specific user" , callback_data="messageToOneUser")],
        [InlineKeyboardButton(text = "message to all users" , callback_data="messageToAllUsers")],
        [InlineKeyboardButton(text = "add new channel" , callback_data="addNewChannel"),
         InlineKeyboardButton(text = "remove channel", callback_data="removeChannel")],
        [InlineKeyboardButton(text = "delete all chats with users" , callback_data="deleteAllChats")],
        [InlineKeyboardButton(text = "switch to user pannel" , callback_data="userPannel")],
        ]
        )
    }
    

    def edit_ad_button(self , price , id , view):
        tempPirce = self.procces_price(price)
        return {
        "Fa" : InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(text = f"{tempPirce} Tomans" , callback_data="price")],
            [InlineKeyboardButton(text = "تغییر عکس" , callback_data=f"editPhoto{id}"),
            InlineKeyboardButton(text = "تغییر عنوان" , callback_data=f"editTitle{id}"),
            InlineKeyboardButton(text = "تغییر قیمت" , callback_data=f"editPrice{id}")],
            [InlineKeyboardButton(text = "حذف آگهی" , callback_data=f"deleteAd{id}")],
            [InlineKeyboardButton(text = f"{view} بازدید" , callback_data="view")],
            [InlineKeyboardButton(text = "برگشت به پنل" , callback_data="userPannel")]
        ]),
        "En" : InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(text = f"{tempPirce} Tomans" , callback_data="price")],
            [InlineKeyboardButton(text = "edit Photo" , callback_data=f"editPhoto{id}"),
            InlineKeyboardButton(text = "edit Title" , callback_data=f"editTitle{id}"),
            InlineKeyboardButton(text = "edit Price" , callback_data=f"editPrice{id}")],
            [InlineKeyboardButton(text = "delete ad" , callback_data=f"deleteAd{id}")],
            [InlineKeyboardButton(text = f"{view} views" , callback_data="view")],
            [InlineKeyboardButton(text = "back to pannel" , callback_data="userPannel")]

        ])
    }
    

    def searched_ad_button(self , price , telegramID , adID , view):
        tempPirce = self.procces_price(price)
        return {
        "Fa" : InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(text = f"{tempPirce} Tomans" , callback_data="price")],
            [InlineKeyboardButton(text = f"{view} بازدید" , callback_data="view")],
            [InlineKeyboardButton(text = "ارسال پیام به فروشنده" , callback_data=f"messageToUser{telegramID}")],
            [InlineKeyboardButton(text = "گزارش" , callback_data=f"reportAd{adID}")],
            [InlineKeyboardButton(text = "برگشت به پنل" , callback_data="userPannel")]
        ]),
        "En" : InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(text = f"{tempPirce} Tomans" , callback_data="price")],
            [InlineKeyboardButton(text = f"{view} views" , callback_data="view")],
            [InlineKeyboardButton(text = "send message to seller" , callback_data=f"messageToUser{telegramID}")],
            [InlineKeyboardButton(text = "report this ad" , callback_data=f"reportAd{adID}")],
            [InlineKeyboardButton(text = "back to pannel" , callback_data="userPannel")]

        ])
    }


    def message_answer_button(self , telegramID):
        return {
        "Fa" : InlineKeyboardMarkup([[InlineKeyboardButton(text = "پاسخ" , callback_data=f"messageToUser{telegramID}")],]),
        "En" : InlineKeyboardMarkup([[InlineKeyboardButton(text = "answer" , callback_data=f"messageToUser{telegramID}")],])
    }


    def see_ad_button(self , adID):
        return {
        "Fa" : InlineKeyboardMarkup([[InlineKeyboardButton(text = "مشاهده تبلیغ" , callback_data=f"seeAd{adID}")],]),
        "En" : InlineKeyboardMarkup([[InlineKeyboardButton(text = "see ad" , callback_data=f"seeAd{adID}")],])
    }


    def submit_ad_button(self , price , id):
        tempPrice = self.procces_price(price)
        return {
        "Fa" : InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(text = f"{tempPrice} Tomans" , callback_data="price")],
            [InlineKeyboardButton(text = "تغییر عکس" , callback_data=f"editPhoto{id}"),
            InlineKeyboardButton(text = "تغییر عنوان" , callback_data=f"editTitle{id}"),
            InlineKeyboardButton(text = "تغییر قیمت" , callback_data=f"editPrice{id}")],
            [InlineKeyboardButton(text = "ثبت آگهی" , callback_data="submitAd")],
            [InlineKeyboardButton(text = "برگشت به پنل" , callback_data="userPannel")]
        ]),
        "En" : InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(text = f"{tempPrice} Tomans" , callback_data="price")],
            [InlineKeyboardButton(text = "edit Photo" , callback_data=f"editPhoto{id}"),
            InlineKeyboardButton(text = "edit Title" , callback_data=f"editTitle{id}"),
            InlineKeyboardButton(text = "edit Price" , callback_data=f"editPrice{id}")],
            [InlineKeyboardButton(text = "submit ad" , callback_data="submitAd")],
            [InlineKeyboardButton(text = "back to pannel" , callback_data="userPannel")]
        ])
    }

    def procces_price(self, price):
        newPrice = str(price)
        count = 0
        for i in range((len(newPrice)) , 0 , -1):
            count +=1
            if count%3 == 0:
                newPrice = newPrice[:i-1] + "," +newPrice[i-1:]
        newPrice = newPrice.removeprefix(",")
        return newPrice

    def price_button(self , price):
        return InlineKeyboardMarkup([[InlineKeyboardButton(text = f"{self.procces_price(price)} Tomans" , callback_data="price")]])

    onStartMessage = """Hello ! welcome to our Advertising & Shopping Bot.
please choose your language     

    
سلام! به ربات تبلیغاتی و فروشگاهی ما خوش آمدید.
لطفا زبان مورد نظر خود را انتخاب کنید
    """

    changeLanguageMessage = """ please choose you language

لطفا زبان مورد نظر خود را انتخاب کنید
    """

    choosedLangAnswer = {"Fa" : "زبان فارسی به عنوان زبان پیش فرض انتخاب شد" ,
                    "En" : "English choosed as your default language"}
    
    joinCheckerMessage ={"Fa" : " برای فعال شدن همه امکانات ربات لطفا در کانال های زیر عضو شوید سپس روی گزینه عضو شدم کلیک کنید" ,
                    "En" : "for more futures , please join to below channels . then click on joined button"}

    getPhoneNumberMessage = {"Fa" : "لطفا شماره تلفن همراه خود را وارد نمایید " ,"En" : "please enter your phone number"}


    userPannelMessage = {"Fa" : "لطفا یکی از دکمه های زیر را انتخاب نمایید" ,
                    "En" : "please choose on of the below buttons"}

    phoneNotValidMessage = {"Fa" : "فرمت شماره موبایل وارد شده صحیح نمی باشد. لطفا مجددا تلاش کنید" ,
                    "En" : "phone number format is not valid. please try again"}

    getAgeMessage = {"Fa" : "لطفا سن خود را به صورت عدد در پیام بعدی وارد کنید" ,
                    "En" : "please enter your age just as a number"}
    
    ageNotValidMessage = {"Fa" : "سن وارد شده معتبر نمی باشد لطفا مجددا تلاش کنید" ,
                    "En" : "age not valid ! pelase try again"}

    signUpSuccesMessage = {"Fa" : "ثبت نام شما با موفقیت انجام شد" ,
                    "En" : "signup finnished succesfully!"}
    
    joinedSuccesfullyMessage = {"Fa" : "عضویت شما تایید شد" ,
                    "En" : "Your membership has been accepted"}
    
    joinNotSuccesMessage = {"Fa" : "!شما هنوز در همه کانال های ما عضو نشده اید" ,
                    "En" : "you are not joined in all of channels"}

    userPannelMessage = {"Fa" : "برای استفاده از هرکدام از امکانات زیر روی دکمه مورد نظر کلیک کنید. برای تغییر زبان دستور /lang را ارسال کنید" ,
                    "En" : "for any future , please click on it's button . for change language send /lang "}

    getNameMessage = {"Fa" : "لطفا نام جدید خود را وارد نمایید" , "En" : "please send your new name"}

    nameChangedSuccesfullyMessage = {"Fa" :"نام شما با موفقیت تغیر یافت" , "En" : "your name changed succefully"}

    PhoneChangedSuccesfullyMessage = {"Fa" :"شماره موبایل شما با موفقیت تغیر یافت" , "En" : "your phone number changed succefully"}
    
    sendMessageToAdminMessage = {"Fa" :"لطفا پیام مورد نظر خود را وارد کنید", "En" : "please send your message"}
    
    messageSentSuccesMessage = {"Fa" :"پیام شما با موفقیت ارسال شد","En" : "your message sent succesfully"}

    bannedUserMessage = {"Fa" :"شما توسط ادمین مسدود شده اید","En" : "you are banned by admin !"}

    getAdTitleMessage = {"Fa" :"لطفا <<فقط>> متن تبلیغ خود را تایپ کنید و توجه کنید که حتما که نوع کالای شما در متن موجود باشد",
                         "En" : "please just send your ad description . note that your description must includes your ad article name"}
    
    getPriceMessage = {"Fa" :"لطفا قیمت مورد نظر خود را به صورت عددی و به تومان وارد کنید","En" : "enter your price as a number in Toman "}
    
    getImageMessage = {"Fa" :"لطفا تصویر کالای خود را ارسال کنید","En" : "please send your article image"}

    unusableCallBackMessage = {"Fa" : "این دکمه صرفا برای اطلاع رسانی است" , "En" : "this button is just for noticing!"}

    adSubmittedSuccesfullyMessage = {"Fa" : "با موفقیت ثبت شد" ,"En" : "your ad submitted succesfully"}

    noAdSubmittedMessage = {"Fa" : "شما هنوز آگهی ای ثبت نکرده اید" ,"En" : "you didn't submitted any ad yet"}
    
    editSuccesfullMessage = {"Fa" : "تغییرات با موفقیت انجام شد" ,"En" : "changed succefully"}
    
    adDeletedSuccesfullyMessage = {"Fa" : "تبلیغ مورد نظر با موفقیت پاک شد" ,"En" : "ad deleted succesfully"}
    
    noAdFoundMessage = {"Fa" : "هیچ تبلیغی با عنوان خواسته شده یافت نشد" ,"En" : "no ad found with requested title"}
    
    errorOccuredMessage = {"Fa" : "مشکلی رخ داده است" ,"En" : "an error occured"}
    
    reportSentSuccesfullyMessage = {"Fa" : "گزارش ارسال شد" ,"En" : "report sent"}
    
    getSearchTitleMessage = {"Fa" : "لطفا عنوان مورد جستجوی خود را وارد کنید.تمام آگهی های دارای این عنوان نمایش داده میشوند" 
                             ,"En" : "please enter your wanted title. all ads include this title will be shown"}
    
    largeImageMessage = {"Fa" : "حجم فایل بیشتر از 2 مگابایت است لطفا دوباره تلاش کنید" ,
                         "En" : "file size is bigger than 2MB . try again"}

    def alert_message_for_forwarding_messages(self , name):
        return {
            "Fa" : f"{name} یک پیام برای شما ارسال کرده است",
            "En" : f"{name} sent you a message"
        }
    

    def report_ad_to_admin(self , telegramID  , adID):
        return {
            "Fa" : f"کاربر {telegramID} تبلیغ {adID} را گزارش کرده است",
            "En" : f"user {telegramID} reported ad {adID}"
        }


    def convert_user_data_to_text(self , data):
        persianString = f"""اسم : {data["name"]}
آی دی تلگرام : {data["telegramID"]} 
شماره موبایل : {data["phoneNum"]}
آی دی @{data["telegramUsername"]}
سن : {data["age"]}
تاریخ عضویت : {data["joinDate"]}
تبلیغات فعال : {data["numOfActiveAds"]}
زبان : {data["lang"]}
ادمین: {data["isAdmin"]}
بن شده: {data["isBanned"]}"""
        
        englishString = f"""name : {data["name"]}
telegram ID : {data["telegramID"]}
phone : {data["phoneNum"]} 
user ID : @{data["telegramUsername"]}
age : {data["age"]}
join date : {data["joinDate"]}
number of active ads : {data["numOfActiveAds"]}
language = {data["lang"]}
is admin : {data["isAdmin"]}
is banned : {data["isBanned"]}"""
        return {"Fa" : persianString , "En" : englishString}



shopBot = Handler()
