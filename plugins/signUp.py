from pyrogram import Client , filters
from pyrogram.types import Message , CallbackQuery
from classes.Handler import shopBot
from classes.Person import Person
from func.createdFilters import *
from func.validatingFuncs import *

@Client.on_callback_query(~user_started & ~(check_step(1) |check_step(2) | check_step(3)))
async def handle_unstarted_user(client : Client , callBack : CallbackQuery):
    user = callBack.from_user
    await callBack.message.delete()
    await client.send_message(user.id,shopBot.onStartMessage , reply_markup=shopBot.chooseLangButton)

@Client.on_message(check_step(0))
async def answer_banned_user(client : Client , message : Message):
    user = message.from_user
    await message.reply_text(shopBot.bannedUserMessage[shopBot._userPocket[user.id]["lang"]] 
                             ,reply_markup=shopBot.messageToAdminButton[shopBot._userPocket[user.id]["lang"]])

@Client.on_callback_query(check_step(0))
async def answer_banned_user(client : Client , callBack : CallbackQuery):
    user = callBack.from_user
    await client.send_message(chat_id=user.id,text=shopBot.bannedUserMessage[shopBot._userPocket[user.id]["lang"]] 
                             , reply_markup=shopBot.messageToAdminButton[shopBot._userPocket[user.id]["lang"]])


@Client.on_message((filters.command("start")  & filters.private) | ~user_started)
async def handle_start(client : Client , message : Message):
    user = message.from_user
    await message.reply_text(shopBot.onStartMessage , reply_markup=shopBot.chooseLangButton)
    # add new user
    newUser= Person(str(user.first_name), str(user.last_name), user.id , user.language_code , user.username , user.phone_number)

    if shopBot._DB.user_available_in_DB(user.id):
        userInfo = shopBot._DB.get_user_by_telegramID(user.id)
        if userInfo["age"] == 0:
            if userInfo["phoneNum"] == None:
                shopBot._userPocket[user.id]["step"] = 1
            elif userInfo["phoneNum"] != None:
                shopBot._userPocket[user.id]["step"] = 2
                await message.reply_text(shopBot.getAgeMessage[shopBot._userPocket[user.id]["lang"]])
        else:
            shopBot._userPocket[user.id]["step"] = 3
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
        await callBack.edit_message_text(shopBot.getPhoneNumberMessage[callBack.data])
    elif shopBot._userPocket[user.id]["step"] == 3:
        if await join_Checker(client , callBack):
           await callBack.edit_message_text(text=shopBot.userPannelMessage[shopBot._userPocket[user.id]["lang"]]
                     ,reply_markup= shopBot.userPannelButton[shopBot._userPocket[user.id]["lang"]])
        else:
            await callBack.edit_message_text(shopBot.joinCheckerMessage[shopBot._userPocket[user.id]["lang"]],
                reply_markup=shopBot.get_channels_buttons())



@Client.on_message(filters.command("lang") & filters.private)
async def change_language(client : Client , message : Message):
    user = message.from_user
    if shopBot._DB.user_available_in_DB(user.id):
        userInfo = shopBot._DB.get_user_by_telegramID(user.id)
        await message.reply_text(shopBot.changeLanguageMessage , reply_markup=shopBot.chooseLangButton)
        if userInfo["age"] == 0:
            if userInfo["phoneNum"] == None:
                shopBot._userPocket[user.id]["step"] = 1
            elif userInfo["phoneNum"] != None:
                shopBot._userPocket[user.id]["step"] = 2
                await message.reply_text(shopBot.getAgeMessage[shopBot._userPocket[user.id]["lang"]])
        else:
            shopBot._userPocket[user.id]["step"] = 3
    else:
        await handle_start(client , message)


@Client.on_message(filters.text & filters.private & check_step(1))
async def get_phone_number(client : Client , message : Message):
    user = message.from_user
    if validate_phone_number(message.text):
        shopBot._userPocket[user.id]["step"] = 2
        shopBot._DB.edit_user_PhoneNumber(user.id , message.text)
        await message.reply_text(shopBot.getAgeMessage[shopBot._userPocket[user.id]["lang"]])
    else:
        await message.reply_text(shopBot.phoneNotValidMessage[shopBot._userPocket[user.id]["lang"]])


@Client.on_message(filters.text & filters.private & check_step(2))
async def get_age(client : Client , message : Message):
    user = message.from_user
    if validate_age(message.text):
        shopBot._userPocket[user.id]["step"] = 3
        shopBot._DB.edit_user_Age(user.id , message.text)
        await message.reply_text(shopBot.signUpSuccesMessage[shopBot._userPocket[user.id]["lang"]])

        if await join_Checker(client , message):
            await message.reply_text(shopBot.userPannelMessage[shopBot._userPocket[user.id]["lang"]] 
                    , reply_markup= shopBot.userPannelButton[shopBot._userPocket[user.id]["lang"]])
        else:
            await message.reply_text(shopBot.joinCheckerMessage[shopBot._userPocket[user.id]["lang"]],
                reply_markup=shopBot.get_channels_buttons())
    else:
        await message.reply_text(shopBot.ageNotValidMessage[shopBot._userPocket[user.id]["lang"]])      


@Client.on_callback_query(join_filter & query_filter("joined"))
async def joined_button_handler(client : Client , callBack : CallbackQuery):
    user = callBack.from_user
    await callBack.edit_message_text(shopBot.joinedSuccesfullyMessage[shopBot._userPocket[user.id]["lang"]])
    await client.send_message(chat_id=user.id ,text=shopBot.userPannelMessage[shopBot._userPocket[user.id]["lang"]]
            ,reply_markup= shopBot.userPannelButton[shopBot._userPocket[user.id]["lang"]])


@Client.on_callback_query(~join_filter & query_filter("joined"))
async def notjoined_button_handler(client : Client , callBack : CallbackQuery):
    user = callBack.from_user
    await callBack.answer(shopBot.joinNotSuccesMessage[shopBot._userPocket[user.id]["lang"]])



