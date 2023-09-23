import os
from pyrogram import Client , filters
from pyrogram.types import Message , CallbackQuery
from func.createdFilters import *
from func.validatingFuncs import *
from classes.Handler import shopBot


@Client.on_callback_query(query_filter("getUserInfo") & is_admin & check_step(23))
async def get_value_to_search_user(client : Client , callBack : CallbackQuery):
    user = callBack.from_user
    lang = shopBot._userPocket[user.id]["lang"]
    await callBack.message.delete()
    await client.send_message(user.id , shopBot.getUserSearchValueMessage[lang] , reply_markup=shopBot.backToAdminPannelButton[lang])
    shopBot._userPocket[user.id]["step"] = 24


@Client.on_message(check_step(24) & is_admin & filters.private)
async def return_user_info(client : Client , message : Message):
    user = message.from_user
    lang = shopBot._userPocket[user.id]["lang"]
    foundPersons = []
    temp = shopBot._DB.get_user_by_telegramID(message.text)
    if temp != None:
        foundPersons.append(temp)
    temp = shopBot._DB.get_user_by_PhoneNum(message.text)
    if temp !=None: 
        foundPersons.extend(temp)
    temp = shopBot._DB.get_user_by_telegramUsername(message.text)
    if temp !=None:     
        foundPersons.extend(temp)

    if len(foundPersons) > 0:
        shopBot._userPocket[user.id]["step"] = 23
        for person in foundPersons:
            if user.id in shopBot._owners:
                if person["isAdmin"] == 2:
                    await message.reply_text(shopBot.convert_user_data_to_text(person)[lang] , reply_markup=shopBot.same_access_level_button(person["telegramID"])[lang])
                else:
                    await message.reply_text(shopBot.convert_user_data_to_text(person)[lang] , reply_markup=shopBot.owner_to_admin_button(person["telegramID"])[lang])
            
            elif (user.id in shopBot._admins) & (user.id not in shopBot._owners):
                if person["isAdmin"] == 0:
                    await message.reply_text(shopBot.convert_user_data_to_text(person)[lang] , reply_markup=shopBot.owner_to_admin_button(person["telegramID"])[lang])
                else:
                    await message.reply_text(shopBot.convert_user_data_to_text(person)[lang] , reply_markup=shopBot.same_access_level_button(person["telegramID"])[lang])
    else:
        await message.reply_text(shopBot.noUserFoundMessage[lang] , reply_markup=shopBot.backToAdminPannelButton[lang])


@Client.on_callback_query(query_filter_regex("removeUser") & is_admin & check_step(23))
async def remove_user(client : Client , callBack : CallbackQuery):
    user = callBack.from_user
    lang = shopBot._userPocket[user.id]["lang"]
    status = shopBot._DB.delete_user_by_telegramID(callBack.data[10:])
    if int(user.id) in shopBot._admins:
        shopBot._admins.remove(int(user.id))
        shopBot._DB.delete_user_by_telegramID(user.id)
    await callBack.message.delete()
    if status:
        await callBack.answer(shopBot.userDeletedSuccesfully[lang]  , show_alert=True)
    else:
        await callBack.answer(shopBot.noUserFoundMessage[lang]  , show_alert=True)


@Client.on_callback_query(query_filter_regex("showUserAds") & is_admin & check_step(23))
async def show_user_ad_to_admin(client : Client , callBack : CallbackQuery):
    user = callBack.from_user
    lang = shopBot._userPocket[user.id]["lang"]
    ads = shopBot._DB.get_all_ads_by_telegramID(callBack.data[11:])
    person = shopBot._DB.get_user_by_telegramID(callBack.data[11:])
    if ads == None:
        await callBack.answer(shopBot.noAdSubmittedByUserMessage[lang] , show_alert=True)
    else:
        await client.send_message(user.id , shopBot.convert_user_data_to_text(person)[lang] , reply_markup=shopBot.backToAdminPannelButton[lang])
        for ad in ads:
            await client.send_photo(user.id , ad["photoID"] , ad["title"], reply_markup=shopBot.admin_access_on_ad_button(ad["price"],ad["userID"],ad["adID"],ad["views"])[lang])


@Client.on_callback_query(query_filter_regex("seeAd") & is_admin)
async def show_reported_ad_to_admin(client : Client , callBack : CallbackQuery):
    user = callBack.from_user
    lang = shopBot._userPocket[user.id]["lang"]
    ad = shopBot._DB.get_ad_by_adID(callBack.data[5:])
    userID , temp = callBack.data[5:].split("-")
    person = shopBot._DB.get_user_by_telegramID(userID)
    if (ad == None) | (person == None):
        await callBack.answer(shopBot.noAdSubmittedByUserMessage[lang] , show_alert=True)
    else:
        if user.id in shopBot._owners:
            if userID not in shopBot._owners:
                await client.send_message(user.id , shopBot.convert_user_data_to_text(person)[lang] , reply_markup=shopBot.owner_to_admin_button(userID)[lang])
            else:
                await client.send_message(user.id , shopBot.convert_user_data_to_text(person)[lang] , reply_markup=shopBot.same_access_level_button(userID)[lang])
        elif (user.id in shopBot._admins) & (user.id not in shopBot._owners):
            if userID not in shopBot._admins:
                await client.send_message(user.id , shopBot.convert_user_data_to_text(person)[lang] , reply_markup=shopBot.owner_to_admin_button(userID)[lang])
            else:
                await client.send_message(user.id , shopBot.convert_user_data_to_text(person)[lang] , reply_markup=shopBot.same_access_level_button(userID)[lang])
        await client.send_photo(user.id , ad["photoID"] , ad["title"], reply_markup=shopBot.admin_access_on_ad_button(ad["price"],ad["userID"],ad["adID"],ad["views"])[lang])


@Client.on_callback_query(query_filter_regex("seeUserInfo") & is_admin & check_step(23)) 
async def show_user_info_to_admin(client : Client , callBack : CallbackQuery):
    user = callBack.from_user
    lang = shopBot._userPocket[user.id]["lang"]
    person = shopBot._DB.get_user_by_telegramID(callBack.data[11:])
    if person != None:
        if user.id in shopBot._owners:
            if int(person["isAdmin"]) == 2:
                await client.send_message(user.id,shopBot.convert_user_data_to_text(person)[lang] , reply_markup=shopBot.same_access_level_button(callBack.data[11:])[lang])
            else:
                await client.send_message(user.id,shopBot.convert_user_data_to_text(person)[lang] , reply_markup=shopBot.owner_to_admin_button(callBack.data[11:])[lang])
            
        elif (user.id in shopBot._admins) & (user.id not in shopBot._owners):
            if int(person["isAdmin"]) == 0:
                await client.send_message(user.id,shopBot.convert_user_data_to_text(person)[lang] , reply_markup=shopBot.owner_to_admin_button(callBack.data[11:])[lang])
            else:
                await client.send_message(user.id,shopBot.convert_user_data_to_text(person)[lang] , reply_markup=shopBot.same_access_level_button(callBack.data[11:])[lang])
    else:
        await client.send_message(user.id, shopBot.noUserFoundMessage[lang] , reply_markup=shopBot.backToAdminPannelButton[lang])


@Client.on_callback_query((query_filter_regex("banUser") | query_filter_regex("unbanUser")) & is_admin & check_step(23))
async def change_blockage_status(client : Client , callBack : CallbackQuery):
    user = callBack.from_user
    lang = shopBot._userPocket[user.id]["lang"]
    status = True
    if callBack.data[:7] == "banUser":
        status = shopBot._DB.change_user_ban_status_by_telegramID(callBack.data[7:] , 1)
        if status:
            shopBot._userPocket[int(callBack.data[7:])]["step"] = -1
            await callBack.answer(shopBot.userBannedSuccessfullyMessage[lang] , show_alert=True)
        else:
             await callBack.answer(shopBot.errorOccuredMessage[lang] , show_alert=True)
    else:
        status = shopBot._DB.change_user_ban_status_by_telegramID(callBack.data[9:] , 0)
        if status:
            if int(callBack.data[9:]) in shopBot._admins:
                shopBot._userPocket[int(callBack.data[9:])]["step"] = 23
            else:
                shopBot._userPocket[int(callBack.data[9:])]["step"] = 3
            await callBack.answer(shopBot.userUnBannedSuccessfullyMessage[lang])
        else:
             await callBack.answer(shopBot.errorOccuredMessage[lang] , show_alert=True)


@Client.on_callback_query(query_filter("sendDatabase") & is_admin & check_step(23)) 
async def upload_database_file(client : Client , callBack : CallbackQuery):
    user = callBack.from_user
    lang = shopBot._userPocket[user.id]["lang"]
    await client.send_document(user.id , shopBot._DB._DataBasePATH ,protect_content=True , 
         file_name = "ShopDatabase.db" , reply_markup=shopBot.backToAdminPannelButton[lang])
    

@Client.on_callback_query(query_filter("getDatabase") & is_admin & check_step(23)) 
async def get_database_file(client : Client , callBack : CallbackQuery):
    user = callBack.from_user
    lang = shopBot._userPocket[user.id]["lang"]
    shopBot._userPocket[user.id]["step"] = 30
    await client.send_message(user.id , shopBot.getDatabaseMessage[lang] , reply_markup = shopBot.backToAdminPannelButton[lang])


@Client.on_message(filters.private & filters.document & is_admin & check_step(30)) 
async def download_database_file(client : Client , message : Message):
    try:
        user = message.from_user
        lang = shopBot._userPocket[user.id]["lang"]
        await message.download("cache/ShopDatabase.db")
        if is_sqlite_file("cache/ShopDatabase.db"):
            shopBot.read_data_from_DB()
            os.replace("cache/ShopDatabase.db" , "Database/ShopDatabase.db")
            await message.reply_text(shopBot.databaseChangedMessage[lang])
            await message.reply_text(shopBot.userPannelMessage[lang],reply_markup= shopBot.adminPannelButton[lang])
            shopBot._userPocket[user.id]["step"] = 23
        else:
            await message.reply_text(shopBot.getDatabaseMessage[lang] , reply_markup = shopBot.backToAdminPannelButton[lang])
            os.remove("cache/ShopDatabase.db")
    except Exception as exc:
        await message.reply_text(shopBot.errorOccuredMessage[lang] + exc , shopBot.backToAdminPannelButton[lang])


@Client.on_message(filters.private & ~filters.document & is_admin & check_step(30)) 
async def wrong_database_file(client : Client , message : Message):
    user = message.from_user
    lang = shopBot._userPocket[user.id]["lang"]
    await client.send_message(user.id , shopBot.getDatabaseMessage[lang] , reply_markup = shopBot.backToAdminPannelButton[lang])


@Client.on_callback_query(query_filter("messageToAllUsers") & is_admin & check_step(23)) 
async def get_message_to_sent_to_all(client : Client , callBack : CallbackQuery):
    user = callBack.from_user
    lang = shopBot._userPocket[user.id]["lang"]
    shopBot._userPocket[user.id]["step"] = 28
    await client.send_message(user.id , shopBot.sendMessageToUserMessage[lang] , reply_markup = shopBot.backToAdminPannelButton[lang])


@Client.on_message(filters.private & is_admin & check_step(28)) 
async def submit_message_to_send_to_all(client : Client , message : Message):
    user = message.from_user
    lang = shopBot._userPocket[user.id]["lang"]
    await message.copy(user.id , reply_markup=shopBot.sendMessageToAllButton[lang])


@Client.on_callback_query(query_filter("sendToAll") & is_admin & check_step(28)) 
async def send_message_to_all_users(client : Client , callBack : CallbackQuery):
    user = callBack.from_user
    msg = callBack.message
    lang = shopBot._userPocket[user.id]["lang"]
    usersIDs = shopBot._DB.get_all_telegramIDs()
    for id in usersIDs:
        if id != user.id:
            await msg.copy(id , reply_markup=None)
    shopBot._userPocket[user.id]["step"] = 23
    await msg.edit_reply_markup(None)
    await callBack.answer(shopBot.messageSentSuccesMessage[lang] , show_alert=True)
    await client.send_message(chat_id = user.id ,text=shopBot.userPannelMessage[lang],reply_markup= shopBot.adminPannelButton[lang])


@Client.on_callback_query(query_filter_regex("messageToOneUser") & is_admin & check_step(23))
async def get_text_to_send_message(client : Client , callBack : CallbackQuery):
    user = callBack.from_user
    lang = shopBot._userPocket[user.id]["lang"]
    await client.send_message(user.id , shopBot.sendMessageToUserMessage[lang] , reply_markup= shopBot.backToAdminPannelButton[lang])
    shopBot._userPocket[user.id]["step"] = 25
    shopBot._userPocket[user.id]["forwardTo"] = int(callBack.data[16:])


@Client.on_message(filters.private & is_admin & check_step(25)) 
async def send_message_to_user(client : Client , message : Message):
    user = message.from_user
    lang = shopBot._userPocket[user.id]["lang"]
    await client.send_message(shopBot._userPocket[user.id]["forwardTo"] , shopBot.alert_message_for_forwarding_messages("admin")[lang])
    await message.copy(shopBot._userPocket[user.id]["forwardTo"] , reply_markup=shopBot.message_answer_button(user.id)[lang])
    await message.reply_text(shopBot.messageSentSuccesMessage[lang])
    await message.reply_text(shopBot.userPannelMessage[lang] , reply_markup=shopBot.adminPannelButton[lang])
    shopBot._userPocket[user.id]["step"] = 23


@Client.on_callback_query(query_filter("searchAd") & is_admin & check_step(23))
async def get_value_to_search_ad(client : Client , callBack : CallbackQuery):
    user = callBack.from_user
    lang = shopBot._userPocket[user.id]["lang"]
    await callBack.message.delete()
    await client.send_message(user.id , shopBot.getAdSearchValueMessage[lang] , reply_markup=shopBot.backToAdminPannelButton[lang])
    shopBot._userPocket[user.id]["step"] = 26


@Client.on_message(filters.private & is_admin & check_step(26)) 
async def return_searched_ads(client : Client , message : Message):
    user = message.from_user
    lang = shopBot._userPocket[user.id]["lang"]
    foundAds = []
    temp = shopBot._DB.get_ad_by_adID(message.text)
    if temp !=None:
        foundAds.append(shopBot._DB.get_ad_by_adID(message.text))
    temp = shopBot._DB.find_wanted_ads_by_title(message.text)
    if temp !=None: 
        foundAds.extend(temp)
    if len(foundAds) > 0:
        shopBot._userPocket[user.id]["step"] = 23
        for ad in foundAds:
            await client.send_photo(user.id , ad["photoID"] , ad["title"],reply_markup=shopBot.admin_access_on_ad_button(ad["price"],ad["userID"],ad["adID"],ad["views"])[lang])
    else:  
        await message.reply_text(shopBot.noAdFoundMessage[lang] , reply_markup=shopBot.backToAdminPannelButton[lang])


@Client.on_callback_query(query_filter("channels") & is_admin & check_step(23))
async def show_all_channels(client : Client , callBack : CallbackQuery):
    user = callBack.from_user
    lang = shopBot._userPocket[user.id]["lang"]
    await callBack.message.delete()
    for channel in shopBot._joinChannels:
        if channel[:5].lower() == "https":
            await client.send_message(user.id , channel , reply_markup=shopBot.delete_channel_button(channel)[lang])
        else:
            await client.send_message(user.id , f"{channel}" , reply_markup=shopBot.delete_channel_button(channel)[lang])
    shopBot._userPocket[user.id]["step"] = 27
    await client.send_message(user.id ,text=shopBot.getNewChannelMessage[lang], reply_markup=shopBot.backToAdminPannelButton[lang])
    

@Client.on_message(filters.private & is_admin & check_step(27) & ~filters.text) 
async def wrong_new_channel(client : Client , message : Message):
    user = message.from_user
    lang = shopBot._userPocket[user.id]["lang"]
    await client.send_message(user.id ,text=shopBot.getNewChannelMessage[lang], reply_markup=shopBot.backToAdminPannelButton[lang])


@Client.on_message(filters.private & is_admin & check_step(27) & filters.text) 
async def add_new_channel(client : Client , message : Message):
    user = message.from_user
    lang = shopBot._userPocket[user.id]["lang"]
    if check_given_link_is_valid(message.text.lower()):
        if str(message.text) not in shopBot._joinChannels:
            shopBot._joinChannels.append(str(message.text))
            await message.reply_text(shopBot.channelAddedSuccesfullyMessage[lang] , reply_markup=shopBot.backToAdminPannelButton[lang])
    else:
        await client.send_message(user.id ,text=shopBot.getNewChannelMessage[lang], reply_markup=shopBot.backToAdminPannelButton[lang])


@Client.on_callback_query(query_filter_regex("deleteChannel") & is_admin)
async def remove_channel(client : Client , callBack : CallbackQuery):
    user = callBack.from_user
    lang = shopBot._userPocket[user.id]["lang"]
    channelLink = callBack.data[13:]
    await callBack.message.delete()
    if channelLink in shopBot._joinChannels:
        shopBot._joinChannels.remove(channelLink)
    await callBack.answer(shopBot.channelRemovedSuccesfullyMessage[lang] , True)
    shopBot._userPocket[user.id]["step"] = 23


@Client.on_callback_query(query_filter_regex("demoteAdmin") & is_admin & check_step(23))
async def demote_admin_to_user(client : Client , callBack : CallbackQuery):
    user = callBack.from_user
    lang = shopBot._userPocket[user.id]["lang"]
    if shopBot.demote_user(user.id,int(callBack.data[11:])):
        shopBot._userPocket[int(callBack.data[12:])]["step"] = 3
        await callBack.answer(shopBot.taskSuccesFullyMessage[lang] ,True)
    else:
        await callBack.answer(shopBot.errorOccuredMessage[lang] , True)


@Client.on_callback_query(query_filter_regex("promoteAdmin") & is_admin & check_step(23))
async def promote_user_to_admin(client : Client , callBack : CallbackQuery):
    user = callBack.from_user
    lang = shopBot._userPocket[user.id]["lang"]
    message = callBack.message
    status = shopBot.promote_user(user.id,int(callBack.data[12:]))
    if status == 1:
        shopBot._userPocket[int(callBack.data[12:])]["step"] = 23
        await message.edit_reply_markup(shopBot.same_access_level_button(int(callBack.data[12:]))[lang])
        await callBack.answer(shopBot.taskSuccesFullyMessage[lang] ,True)
    elif status == 2:
        shopBot._userPocket[int(callBack.data[12:])]["step"] = 23
        await callBack.answer(shopBot.taskSuccesFullyMessage[lang] ,True)
    else:
        await callBack.answer(shopBot.errorOccuredMessage[lang] , True)