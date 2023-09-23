from pyrogram import Client , filters
from pyrogram.types import Message , CallbackQuery
from classes.Handler import shopBot
from classes.Person import Person
from func.createdFilters import *
from func.validatingFuncs import *
 

@Client.on_callback_query(check_step(0)& ~(query_filter("Fa") | query_filter("En")))
async def handle_unstarted_user_on_callBack(client : Client , callBack : CallbackQuery):
    user = callBack.from_user
    await callBack.message.delete()
    await client.send_message(user.id,shopBot.onStartMessage , reply_markup=shopBot.chooseLangButton)


@Client.on_message(check_step(0))
async def handle_unstarted_user_on_message(client : Client , message : Message):
    user = message.from_user
    await client.send_message(user.id,shopBot.onStartMessage , reply_markup=shopBot.chooseLangButton)


@Client.on_message(check_step(-1))
async def answer_banned_user_on_message(client : Client , message : Message):
    user = message.from_user
    lang = shopBot._userPocket[user.id]["lang"]
    await message.reply_text(shopBot.bannedUserMessage[lang],reply_markup=shopBot.messageToAdminButton[lang])


@Client.on_callback_query(check_step(-1) & ~query_filter("sendMessageToAdmin"))
async def answer_banned_user_on_query(client : Client , callBack : CallbackQuery):
    user = callBack.from_user
    lang = shopBot._userPocket[user.id]["lang"]
    await client.send_message(chat_id=user.id,text=shopBot.bannedUserMessage[lang],reply_markup=shopBot.messageToAdminButton[lang])


@Client.on_message((filters.command("start") | (check_step(3) & ~filters.command("lang")))  & filters.private)
async def handle_start(client : Client , message : Message):
    user = message.from_user
    lang = shopBot._userPocket[user.id]["lang"]
    step = shopBot._userPocket[user.id]["step"]
    if (lang == "Fa") | (lang == "En"):
        if step == 1:
            await message.reply_text(shopBot.getPhoneNumberMessage[lang])
        elif step == 2:
            await message.reply_text(shopBot.getAgeMessage[lang])
        elif step == 3:
            if await join_Checker(client , message):
                await message.reply_text(shopBot.userPannelMessage[lang] , reply_markup=shopBot.userPannelButton[lang])
            else:
                await client.send_message(user.id , shopBot.joinCheckerMessage[lang],reply_markup=shopBot.get_channels_buttons())
        elif step == 23:
            await message.reply_text(shopBot.userPannelMessage[lang],reply_markup= shopBot.adminPannelButton[lang])
        else:
            await message.reply_text(shopBot.joinCheckerMessage[lang],reply_markup=shopBot.get_channels_buttons())
    else:
        shopBot._userPocket[user.id]["step"] = 0
        newUser= Person(str(user.first_name), str(user.last_name), user.id , None , user.username , user.phone_number)
        shopBot._DB.add_new_user(newUser._telegramUserID , newUser._name, False ,newUser._joinDate , newUser._lang,newUser._telegramUsername , newUser._phoneNumber , newUser._age)
        await message.reply_text(shopBot.onStartMessage , reply_markup=shopBot.chooseLangButton)


@Client.on_callback_query(query_filter("Fa") | query_filter("En"))
async def set_language(client : Client , callBack : CallbackQuery):
    user = callBack.from_user
    await callBack.message.delete()
    shopBot._DB.edit_user_lang(user.id , callBack.data)
    shopBot._userPocket[user.id]["lang"] = callBack.data
    step = shopBot._userPocket[user.id]["step"]
    await callBack.answer(shopBot.choosedLangAnswer[callBack.data])
    if step == -1:
        await client.send_message(user.id,shopBot.bannedUserMessage[callBack.data],reply_markup=shopBot.messageToAdminButton[callBack.data])
    elif step == 0:
        shopBot._userPocket[user.id]["step"] = 1 
        await client.send_message(user.id , shopBot.getPhoneNumberMessage[callBack.data])
    elif step == 1:
        await client.send_message(user.id , shopBot.getPhoneNumberMessage[callBack.data])
    elif step == 2 :
        await client.send_message(user.id , shopBot.getAgeMessage[callBack.data])
    elif step == 23:
        await client.send_message(user.id , shopBot.userPannelMessage[callBack.data],reply_markup= shopBot.adminPannelButton[callBack.data])
    else:
        if await join_Checker(client , callBack):
            await client.send_message(user.id , shopBot.userPannelMessage[callBack.data] , reply_markup=shopBot.userPannelButton[callBack.data])
        else:
            await client.send_message(user.id , shopBot.joinCheckerMessage[callBack.data],reply_markup=shopBot.get_channels_buttons())


@Client.on_message(filters.command("lang") & filters.private)
async def change_language(client : Client , message : Message):
    user = message.from_user
    lang = shopBot._userPocket[user.id]["lang"]
    await message.reply_text(shopBot.changeLanguageMessage , reply_markup=shopBot.chooseLangButton)


@Client.on_message(filters.text & filters.private & check_step(1))
async def get_phone_number(client : Client , message : Message):
    user = message.from_user
    lang = shopBot._userPocket[user.id]["lang"]
    if validate_phone_number(message.text):
        shopBot._userPocket[user.id]["step"] = 2
        shopBot._DB.edit_user_PhoneNumber(user.id , message.text)
        await message.reply_text(shopBot.getAgeMessage[lang])
    else:
        await message.reply_text(shopBot.phoneNotValidMessage[lang])


@Client.on_message(filters.text & filters.private & check_step(2))
async def get_age(client : Client , message : Message):
    user = message.from_user
    lang = shopBot._userPocket[user.id]["lang"]
    if validate_age(message.text):
        shopBot._userPocket[user.id]["step"] = 3
        shopBot._DB.edit_user_Age(user.id , message.text)
        await message.reply_text(shopBot.signUpSuccesMessage[lang])

        if await join_Checker(client , message):
            await message.reply_text(shopBot.userPannelMessage[lang] , reply_markup= shopBot.userPannelButton[lang])
        else:
            await message.reply_text(shopBot.joinCheckerMessage[lang],reply_markup=shopBot.get_channels_buttons())
    else:
        await message.reply_text(shopBot.ageNotValidMessage[lang])      


@Client.on_callback_query(join_filter & query_filter("joined"))
async def joined_button_handler(client : Client , callBack : CallbackQuery):
    user = callBack.from_user
    lang = shopBot._userPocket[user.id]["lang"]
    await callBack.edit_message_text(shopBot.joinedSuccesfullyMessage[lang])
    await client.send_message(chat_id=user.id ,text=shopBot.userPannelMessage[lang],reply_markup= shopBot.userPannelButton[lang])


@Client.on_callback_query(~join_filter & query_filter("joined"))
async def notjoined_button_handler(client : Client , callBack : CallbackQuery):
    user = callBack.from_user
    lang = shopBot._userPocket[user.id]["lang"]
    await callBack.answer(shopBot.joinNotSuccesMessage[lang])