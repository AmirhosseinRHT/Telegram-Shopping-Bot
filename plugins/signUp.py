from pyrogram import Client , filters
from pyrogram.types import Message , CallbackQuery
from classes.Handler import shopBot
from classes.Person import Person


def query_filter(data):
    async def func(flt, _, query):
        return flt.data == query.data
    return filters.create(func, data=data)

def check_user_joined(client : Client , userID , channelsID):
    joinStatus = True
    for channel in channelsID:
        stat = client.get_chat_member(chat_id=channel , user_id=userID)
        print (stat)
        if stat != "member":
            joinStatus = False
    return joinStatus

def CheckStep(step):
    async def func(_, __, message : Message):
        user_id = message.from_user.id
        return shopBot._userPocket[user_id]["step"] == step
    return filters.create(func)

def validate_age(age : str):
    print(age)
    if age.isdigit():
        if 18 <= int(age) <= 99:
            return True
    return False


def validate_phone_number(number : str):
    if not number[1:].isdigit():
        return False
    if len(number) != 11:
        if len(number) != 13:
            return False
    if number[:2] != "09":
        if number[:4] != "+989":
            return False
    return True

@Client.on_message(filters.command("start") & filters.private)
async def handle_start(client : Client , message : Message):
    user = message.from_user
    await message.reply_text(shopBot.onStartMSG , reply_markup=shopBot.chooseLangButton)
    # add new user
    newUser= Person(str(user.first_name), str(user.last_name), user.id , user.language_code , user.username , user.phone_number)

    if shopBot._DB.user_available_in_DB(user.id):
        userInfo = shopBot._DB.get_user_by_telegramID(12345678,user.id)
        print(userInfo)
        if userInfo["age"] == 0:
            if userInfo["phoneNum"] == None:
                shopBot._userPocket[user.id]["step"] = 1
            elif userInfo["phoneNum"] != None:
                shopBot._userPocket[user.id]["step"] = 2
                await message.reply_text(shopBot.getAgeMessage[shopBot._userPocket[user.id]["lang"]])
            else:
                shopBot._userPocket[user.id]["step"] = 10
    else:
        shopBot._DB.add_new_user(newUser._telegramUserID , newUser._name, False ,
        newUser._joinDate , newUser._lang,newUser._telegramUsername , newUser._phoneNumber , newUser._age)
        shopBot._userPocket[user.id]["step"] = 1


@Client.on_callback_query(query_filter("Fa") | query_filter("En"))
async def set_language(client : Client , callBack : CallbackQuery):
    user = callBack.from_user
    shopBot._DB.edit_user_lang(user.id , callBack.data)
    shopBot._userPocket[user.id]["lang"] = callBack.data
    await callBack.answer(shopBot.choosedLangAnswer[callBack.data])
    if shopBot._userPocket[user.id]["step"] == 1:
        await callBack.edit_message_text(shopBot.get_phoneNumber_message(str(user.first_name))[callBack.data])
    elif shopBot._userPocket[user.id]["step"] == 10:
        if check_user_joined(client , user.id , shopBot._channels):
            await callBack.edit_message_text(shopBot.joinedSuccesfullyMessage[shopBot._userPocket[user.id]["lang"]])
            """return user panel"""
        else:
            await callBack.edit_message_text(shopBot.joinCheckerMessage[shopBot._userPocket[user.id]["lang"]],
                reply_markup=shopBot.get_channels_buttons())


@Client.on_callback_query(query_filter("joined"))
async def joined_button_handler(client : Client , callBack : CallbackQuery):
    user = callBack.from_user
    if check_user_joined(client , user.id , shopBot._channels):
        await callBack.edit_message_text(shopBot.joinedSuccesfullyMessage[shopBot._userPocket[user.id]["lang"]])
        """send user pannel"""
    else:
        await callBack.answer(shopBot.joinNotSuccesMessage[shopBot._userPocket[user.id]["lang"]])


@Client.on_message(filters.text & filters.private & CheckStep(1))
async def get_phone_number(client : Client , message : Message):
    user = message.from_user
    if shopBot._userPocket[user.id]["step"] == 1:
        if validate_phone_number(message.text):
            shopBot._userPocket[user.id]["step"] = 2
            shopBot._DB.edit_user_PhoneNumber(user.id , message.text)
            await message.reply_text(shopBot.getAgeMessage[shopBot._userPocket[user.id]["lang"]])
        else:
            await message.reply_text(shopBot.phoneNotValidMessage[shopBot._userPocket[user.id]["lang"]])


@Client.on_message(filters.text & filters.private & CheckStep(2))
async def get_age(client : Client , message : Message):
    user = message.from_user
    if shopBot._userPocket[user.id]["step"] == 2:
        if validate_age(message.text):
            shopBot._userPocket[user.id]["step"] = 10
            shopBot._DB.edit_user_Age(user.id , message.text)
            await message.reply_text(shopBot.signUpSuccesMessage[shopBot._userPocket[user.id]["lang"]])
            
            #check joined channels
            if check_user_joined(client , user.id , shopBot._channels):
                await message.edit_text(shopBot.joinedSuccesfullyMessage[shopBot._userPocket[user.id]["lang"]])
                """return user panel"""
            else:
                await message.reply_text(shopBot.joinCheckerMessage[shopBot._userPocket[user.id]["lang"]],
                        reply_markup=shopBot.get_channels_buttons())
        else:
            await message.reply_text(shopBot.ageNotValidMessage[shopBot._userPocket[user.id]["lang"]])      



