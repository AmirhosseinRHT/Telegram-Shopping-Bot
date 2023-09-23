from collections import defaultdict
from .Database import DataBase
from pyrogram.types import  InlineKeyboardButton , InlineKeyboardMarkup

def my_tree():
    return defaultdict(my_tree)

class Handler():
    _DB = DataBase()
    _userPocket = my_tree()
    _joinChannels = []
    _owners = []
    _admins = []
    saveChannel = ""     #channel which ads will be saved here

    def __init__(self):
        self.read_data_from_DB()

    def read_data_from_DB(self):
        users = self._DB.get_all_users_age_and_phone()
        for user in users:
            if (str(user["lang"]) == "Fa") | (str(user["lang"]) == "En"):
                self._userPocket[user["telegramID"]]["lang"] = user["lang"]
                if user["isBanned"] == 1:
                    self._userPocket[user["telegramID"]]["step"] = -1
                elif user["age"] == 0:
                    if user["phoneNum"] == None:
                        self._userPocket[user["telegramID"]]["step"] = 1
                    elif user["phoneNum"] != None:
                        self._userPocket[user["telegramID"]]["step"] = 2
                elif user["isAdmin"] == 1 or user["isAdmin"] == 2:
                    self._userPocket[user["telegramID"]]["step"] = 23
                else:
                    self._userPocket[user["telegramID"]]["step"] = 3
            else:
                self._userPocket[user["telegramID"]]["step"] = 0

        temp , self._admins = self._DB.get_all_admins()
        self._owners = temp
        for id in self._owners:
            if id not in self._admins:
                self._admins.append(id)


    def add_channel(self , newChannel):
        if newChannel not in self._joinChannels:
            self._joinChannels.append(newChannel)


    def promote_user(self , adminID , idToPromote):
        try:
            if adminID in self._owners: 
                if idToPromote in self._owners:
                    return False
                elif idToPromote in self._admins:
                    self._DB.edit_user_level(idToPromote , 2)
                    if idToPromote not in self._owners:
                        self._owners.append(idToPromote)
                    return 1
                else:
                    self._DB.edit_user_level(idToPromote , 1)
                    if idToPromote not in self._admins:
                        self._admins.append(idToPromote)
                    return 2
            elif adminID not in self._owners & adminID in self._admins:
                if idToPromote in self._owners | idToPromote in self._admins:
                    return False
                else:
                    self._DB.edit_user_level(idToPromote , 1)
                    if idToPromote not in self._admins:
                        self._admins.append(idToPromote)
                    return 1
            else:
                return False
        except:
            return False
    
    
    def demote_user(self , adminID , idToDemote):
        try:
            if adminID in self._owners:
                self._DB.edit_user_level(idToDemote , 0)
                if idToDemote in self._admins:
                    self._admins.remove(idToDemote)
                return True
            else:
                return False
        except:
            return False
        

    def procces_price(self, price):
        newPrice = str(price)
        count = 0
        for i in range((len(newPrice)) , 0 , -1):
            count +=1
            if count%3 == 0:
                newPrice = newPrice[:i-1] + "," +newPrice[i-1:]
        newPrice = newPrice.removeprefix(",")
        return newPrice
    

    def get_channels_buttons(self):
        buttons = []
        for i in range(len(self._joinChannels)):
            if self._joinChannels[i][:13].lower != "https://t.me/":
                buttons.append([InlineKeyboardButton(f"Channel {i+1}",url = f"https://t.me/{self._joinChannels[i]}")])
            else:
                buttons.append([InlineKeyboardButton(f"Channel {i+1}",url = self._joinChannels[i])])
        buttons.append([InlineKeyboardButton("عضو شدم | joined" , "joined")])
        return InlineKeyboardMarkup(buttons)


    chooseLangButton = InlineKeyboardMarkup(
        [[InlineKeyboardButton(text = "فارسی" , callback_data="Fa"),
        InlineKeyboardButton(text = "English" , callback_data="En")]])
    
    
    def delete_channel_button(self , channelID):
        return {
        "Fa" : InlineKeyboardMarkup([[InlineKeyboardButton(text = f"حذف کانال" , callback_data=f"deleteChannel{str(channelID)}")]]),
        "En" : InlineKeyboardMarkup([[InlineKeyboardButton(text = f"delete channel" , callback_data=f"deleteChannel{str(channelID)}")]])
    }
    
    sendMessageToAllButton = {
        "Fa" : InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(text = "ارسال" , callback_data="sendToAll")],
            [InlineKeyboardButton(text = "برگشتن به پنل ادمین", callback_data="adminPannel")],
        ]),
        "En" : InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(text = "send " , callback_data="sendToAll")],
            [InlineKeyboardButton(text = "back to admin pannel" , callback_data="adminPannel")],
        ]),
    }


    backToUserPannelButton = {
        "Fa" : InlineKeyboardMarkup(
        [[InlineKeyboardButton(text = "برگشتن به پنل" , callback_data="userPannel"),]]),
        "En" : InlineKeyboardMarkup(
        [[InlineKeyboardButton(text = "back to pannel" , callback_data="userPannel"),]])
    }

    backToAdminPannelButton = {
        "Fa" : InlineKeyboardMarkup(
        [[InlineKeyboardButton(text = "برگشتن به پنل" , callback_data="adminPannel"),]]),
        "En" : InlineKeyboardMarkup(
        [[InlineKeyboardButton(text = "back to pannel" , callback_data="adminPannel"),]])
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
        [InlineKeyboardButton(text = "دریافت اطلاعات کاربر" , callback_data="getUserInfo")],
        [InlineKeyboardButton(text = "ارسال پیام به همه کاربران" , callback_data="messageToAllUsers")],
        [InlineKeyboardButton(text ="کانال ها", callback_data="channels")],
        [InlineKeyboardButton(text = "دریافت فایل دیتابیس" , callback_data="sendDatabase"),
        InlineKeyboardButton(text = "ارسال دیتابیس جدید" , callback_data="getDatabase")],
        [InlineKeyboardButton(text = "پنل عادی" , callback_data="userPannel")],
        ]
        ),
        "En" : InlineKeyboardMarkup(
        [
        [InlineKeyboardButton(text = "search in all ads" , callback_data="searchAd")],
        [InlineKeyboardButton(text = "get user info" , callback_data="getUserInfo")],
        [InlineKeyboardButton(text ="channels", callback_data="channels")],
        [InlineKeyboardButton(text = "message to all users" , callback_data="messageToAllUsers")],
        [InlineKeyboardButton(text = "get DataBase File" , callback_data="sendDatabase"),
        InlineKeyboardButton(text = "upload new DataBase" , callback_data="getDatabase")],
        [InlineKeyboardButton(text = "switch to user pannel" , callback_data="userPannel")],
        ]
        )
    }
    

    def admin_access_on_ad_button(self , price ,userID, adID , view):
        tempPirce = self.procces_price(price)
        return {
        "Fa" : InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(text = f"{tempPirce} Tomans" , callback_data="price")],
            [InlineKeyboardButton(text = "تغییر عکس" , callback_data=f"editPhoto{adID}"),
            InlineKeyboardButton(text = "تغییر عنوان" , callback_data=f"editTitle{adID}"),
            InlineKeyboardButton(text = "تغییر قیمت" , callback_data=f"editPrice{adID}")],
            [InlineKeyboardButton(text = "حذف آگهی" , callback_data=f"deleteAd{adID}")],
            [InlineKeyboardButton(text = "مشاهده صاحب تبلیغ", callback_data=f"seeUserInfo{userID}")],
            [InlineKeyboardButton(text = f"{view} بازدید" , callback_data="view")],
            [InlineKeyboardButton(text = "برگشت به پنل" , callback_data="adminPannel")]
        ]),
        "En" : InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(text = f"{tempPirce} Tomans" , callback_data="price")],
            [InlineKeyboardButton(text = "edit Photo" , callback_data=f"editPhoto{id}"),
            InlineKeyboardButton(text = "edit Title" , callback_data=f"editTitle{id}"),
            InlineKeyboardButton(text = "edit Price" , callback_data=f"editPrice{id}")],
            [InlineKeyboardButton(text = "delete ad" , callback_data=f"deleteAd{id}")],
            [InlineKeyboardButton(text = "see user info", callback_data=f"seeUserInfo{id}")],
            [InlineKeyboardButton(text = f"{view} views" , callback_data="view")],
            [InlineKeyboardButton(text = "back to pannel" , callback_data="adminPannel")]
        ])
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


    def same_access_level_button(self , id):
        return {
        "Fa" : InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(text = "مشاهده آگهی های کاربر" , callback_data=f"showUserAds{id}")],
            [InlineKeyboardButton(text = "ارسال پیام" , callback_data=f"messageToOneUser{id}")],
            [InlineKeyboardButton(text = "برگشت به پنل ادمین", callback_data="adminPannel")]
        ]),
        "En" : InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(text = "show user ads" , callback_data=f"showUserAds{id}")],
            [InlineKeyboardButton(text = "send message" , callback_data=f"messageToOneUser{id}")],
            [InlineKeyboardButton(text = "back to admin pannel" , callback_data="adminPannel")]
        ])
    }

    def owner_to_admin_button(self , id):
        return {
        "Fa" : InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(text = "حذف کاربر" , callback_data=f"removeUser{id}")],
            [InlineKeyboardButton(text = "مشاهده آگهی های کاربر" , callback_data=f"showUserAds{id}")],
            [InlineKeyboardButton(text = "تنزل" , callback_data=f"demoteAdmin{id}"),
            InlineKeyboardButton(text = "ارتقا" , callback_data=f"promoteAdmin{id}")],
            [InlineKeyboardButton(text = "ارسال پیام" , callback_data=f"messageToOneUser{id}")],
            [InlineKeyboardButton(text = "مسدود سازی کاربر" , callback_data=f"banUser{id}"),
            InlineKeyboardButton(text = "رفع مسدودیت کاربر" , callback_data=f"unbanUser{id}")],
            [InlineKeyboardButton(text = "برگشت به پنل ادمین", callback_data="adminPannel")]
        ]),
        "En" : InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(text = "remove user" , callback_data=f"removeUser{id}")],
            [InlineKeyboardButton(text = "show user ads" , callback_data=f"showUserAds{id}")],
            [InlineKeyboardButton(text = "demote" , callback_data=f"demoteAdmin{id}"),
            InlineKeyboardButton(text = "promote" , callback_data=f"promoteAdmin{id}")],
            [InlineKeyboardButton(text = "send message" , callback_data=f"messageToOneUser{id}")],
            [InlineKeyboardButton(text = "ban user" , callback_data=f"banUser{id}"),
            InlineKeyboardButton(text = "unban user" , callback_data=f"unbanUser{id}")],
            [InlineKeyboardButton(text = "back to admin pannel" , callback_data="adminPannel")]
        ])
    }

    def price_button(self , price):
        return InlineKeyboardMarkup([[InlineKeyboardButton(text = f"{self.procces_price(price)} Tomans" , callback_data="price")]])
    
    def link_to_bot_button(self , price):
        return InlineKeyboardMarkup([[InlineKeyboardButton(text = f"{self.procces_price(price)} Tomans" , url="https://t.me/amirrahasbot")]])

    onStartMessage = """Hello ! welcome to our Advertising & Shopping Bot.
please choose your language     

    
سلام! به ربات تبلیغاتی و فروشگاهی ما خوش آمدید.
لطفا زبان مورد نظر خود را انتخاب کنید
    """

    changeLanguageMessage = """ please choose you language

لطفا زبان مورد نظر خود را انتخاب کنید
    """

    choosedLangAnswer = {"Fa" : "زبان فارسی به عنوان زبان پیش فرض انتخاب شد" ,"En" : "English choosed as your default language"}
    
    joinCheckerMessage ={"Fa" : " برای فعال شدن همه امکانات ربات لطفا در کانال های زیر عضو شوید سپس روی گزینه عضو شدم کلیک کنید" ,
                    "En" : "for more futures , please join to below channels . then click on joined button"}

    getPhoneNumberMessage = {"Fa" : "لطفا شماره تلفن همراه خود را وارد نمایید " ,"En" : "please enter your phone number"}

    userPannelMessage = {"Fa" : "لطفا یکی از دکمه های زیر را انتخاب نمایید" ,"En" : "please choose on of the below buttons"}

    phoneNotValidMessage = {"Fa" : "فرمت شماره موبایل وارد شده صحیح نمی باشد. لطفا مجددا تلاش کنید" ,"En" : "phone number format is not valid. please try again"}

    getAgeMessage = {"Fa" : "لطفا سن خود را به صورت عدد در پیام بعدی وارد کنید" ,"En" : "please enter your age just as a number"}
    
    ageNotValidMessage = {"Fa" : "سن وارد شده معتبر نمی باشد لطفا مجددا تلاش کنید" ,"En" : "age not valid ! pelase try again"}

    signUpSuccesMessage = {"Fa" : "ثبت نام شما با موفقیت انجام شد" ,"En" : "signup finnished succesfully!"}
    
    joinedSuccesfullyMessage = {"Fa" : "عضویت شما تایید شد" ,"En" : "Your membership has been accepted"}
    
    joinNotSuccesMessage = {"Fa" : "!شما هنوز در همه کانال های ما عضو نشده اید" ,"En" : "you are not joined in all of channels"}

    userPannelMessage = {"Fa" : "برای استفاده از هرکدام از امکانات زیر روی دکمه مورد نظر کلیک کنید. برای تغییر زبان دستور /lang را ارسال کنید" ,
                    "En" : "for any future , please click on it's button . for change language send /lang "}

    getNameMessage = {"Fa" : "لطفا نام جدید خود را وارد نمایید" , "En" : "please send your new name"}
    
    getNewChannelMessage = {"Fa" : "برای افزودن کانال جدید آیدی یا لینک آن را وارد کنید .در غیر اینصورت روی دکمه برگشت به پنل کلیک کنید" , 
                            "En" : "send link or id of new channel here. \n for cancel ,back to pannel"}
    
    channelAddedSuccesfullyMessage = {"Fa" : "کانال با موفقیت اضافه شد.برای افزودن کانال دیگر لینک آن را وارد کنید" , 
                            "En" : "channel added succesfully . to add another channel , enter the link"}

    nameChangedSuccesfullyMessage = {"Fa" :"نام شما با موفقیت تغیر یافت" , "En" : "your name changed succefully"}

    PhoneChangedSuccesfullyMessage = {"Fa" :"شماره موبایل شما با موفقیت تغیر یافت" , "En" : "your phone number changed succefully"}
    
    sendMessageToUserMessage = {"Fa" :"لطفا پیام مورد نظر خود را وارد کنید", "En" : "please send your message"}
    
    messageSentSuccesMessage = {"Fa" :"پیام شما با موفقیت ارسال شد","En" : "your message sent succesfully"}

    bannedUserMessage = {"Fa" :"شما توسط ادمین مسدود شده اید","En" : "you are banned by admin !"}

    getAdTitleMessage = {"Fa" :"لطفا <<فقط>> متن تبلیغ خود را تایپ کنید و توجه کنید که حتما نوع کالای شما در متن موجود باشد",
                         "En" : "please just send your ad description . note that your description must includes your ad article name"}
    
    getPriceMessage = {"Fa" :"لطفا قیمت مورد نظر خود را به صورت عددی و به تومان وارد کنید","En" : "enter your price as a number in Toman "}
    
    taskSuccesFullyMessage = {"Fa" :"عملیات با موفقیت انجام شد","En" : "task finnished succesfully"}
        
    getImageMessage = {"Fa" :"لطفا تصویر کالای خود را ارسال کنید","En" : "please send your article image"}
    
    getDatabaseMessage = {"Fa" :"فایل دیتابیس را ارسال کنید","En" : "send databse file"}
    
    databaseChangedMessage = {"Fa" :"دیتابیس با موفقیت آپدیت شد","En" : "database updated successfully"}

    unusableCallBackMessage = {"Fa" : "این دکمه صرفا برای اطلاع رسانی است" , "En" : "this button is just for noticing!"}

    adSubmittedSuccesfullyMessage = {"Fa" : "با موفقیت ثبت شد" ,"En" : "your ad submitted succesfully"}

    noAdSubmittedMessage = {"Fa" : "شما هنوز آگهی ای ثبت نکرده اید" ,"En" : "you didn't submitted any ad yet"}
    
    noAdSubmittedByUserMessage = {"Fa" : "کاربر هنوز آگهی ای ثبت نکرده است" ,"En" : "user not submitted any ad yet"}
    
    editSuccesfullMessage = {"Fa" : "تغییرات با موفقیت انجام شد" ,"En" : "changed succefully"}
    
    adDeletedSuccesfullyMessage = {"Fa" : "تبلیغ مورد نظر با موفقیت پاک شد" ,"En" : "ad deleted succesfully"}
    
    noAdFoundMessage = {"Fa" : "هیچ تبلیغی با عنوان جستجو شده یافت نشد. مجددا تلاش کنید" ,"En" : "no ad found with requested title . try again"}
    
    errorOccuredMessage = {"Fa" : "مشکلی رخ داده است" ,"En" : "an error occured"}
    
    reportSentSuccesfullyMessage = {"Fa" : "گزارش ارسال شد" ,"En" : "report sent"}
    
    userBannedSuccessfullyMessage = {"Fa" : "کاربر مسدود شد" ,"En" : "user banned"}
    
    userUnBannedSuccessfullyMessage = {"Fa" : "کاربر رفع مسدودیت شد" ,"En" : "user unbanned"}
    
    futureNotAvailableMessage = {"Fa" : "این قابلیت برای شما فعال نیست" ,"En" : "this future is not available for you"}
    
    noUserFoundMessage = {"Fa" : "هیچ کاربری یافت نشد" ,"En" : "no user found"}
    
    noAdFoundMessage = {"Fa" : "هیچ تبلیغی یافت نشد" ,"En" : "no ad found"}
    
    getUserSearchValueMessage = {"Fa" : "لطفا شماره موبایل یا یوزرنیم یا ایدی عددی کاربر را وارد کنید" ,
                       "En" : "please enter phone number or user ID or telegram ID of the user"}
    
    getAdSearchValueMessage = {"Fa" : "لطفا ایدی یا عنوان تبلیغ را وارد کنید" ,"En" : "please enter adID or title of ad"}
    
    getSearchTitleMessage = {"Fa" : "لطفا عنوان مورد جستجوی خود را وارد کنید.تمام آگهی های دارای این عنوان نمایش داده میشوند" 
                             ,"En" : "please enter your wanted title. all ads include this title will be shown"}
    
    channelRemovedSuccesfullyMessage = {"Fa" : "کانال با موفقیت حذف شد" ,"En" : "channel removed succesfully"}
    
    userDeletedSuccesfully = {"Fa" : "کاربر با موفقیت پاک شد" ,"En" : "user deleted succesfully"}

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
آی دی :@{data["telegramUsername"]}
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
