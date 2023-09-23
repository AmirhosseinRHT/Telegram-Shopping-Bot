import os
from pyrogram import Client , filters
from pyrogram.types import Message , CallbackQuery ,InputMediaPhoto
from classes.Ad import Ad
from func.createdFilters import *
from func.validatingFuncs import *
from classes.Handler import shopBot


@Client.on_callback_query(query_filter("editName") & check_step(3))
async def handle_change_name_button(client : Client , callBack : CallbackQuery):
    user = callBack.from_user
    lang = shopBot._userPocket[user.id]["lang"]
    shopBot._userPocket[user.id]["step"] = 4
    await callBack.message.delete()
    await client.send_message(user.id , shopBot.getNameMessage[lang] ,reply_markup=shopBot.backToUserPannelButton[lang])


@Client.on_message(filters.text & filters.private & check_step(4))
async def rename_user(client : Client , message : Message):
    user = message.from_user
    lang = shopBot._userPocket[user.id]["lang"]
    shopBot._userPocket[user.id]["step"] = 3
    shopBot._DB.edit_user_name(user.id , message.text)
    await message.reply_text(shopBot.nameChangedSuccesfullyMessage[lang])
    await message.reply_text(text=shopBot.userPannelMessage[lang],reply_markup= shopBot.userPannelButton[lang])


@Client.on_callback_query(query_filter("editPhone") & check_step(3))
async def handle_change_PhoneNum_button(client : Client , callBack : CallbackQuery):
    user = callBack.from_user
    lang = shopBot._userPocket[user.id]["lang"]
    shopBot._userPocket[user.id]["step"] = 5
    await callBack.message.delete()
    await client.send_message(user.id , shopBot.getPhoneNumberMessage[lang],reply_markup=shopBot.backToUserPannelButton[lang])


@Client.on_message(filters.text & filters.private & check_step(5))
async def change_PhoneNum(client : Client , message : Message):
    user = message.from_user
    lang = shopBot._userPocket[user.id]["lang"]
    if validate_phone_number(message.text):
        shopBot._userPocket[user.id]["step"] = 3
        shopBot._DB.edit_user_PhoneNumber(user.id , message.text)
        await message.reply_text(shopBot.PhoneChangedSuccesfullyMessage[lang])
        await message.reply_text(text=shopBot.userPannelMessage[lang],reply_markup= shopBot.userPannelButton[lang])
    else:
        await message.reply_text(shopBot.phoneNotValidMessage[lang])


@Client.on_callback_query(query_filter("sendMessageToAdmin"))
async def handle_send_message_to_admins(client : Client , callBack : CallbackQuery):
    user = callBack.from_user
    lang = shopBot._userPocket[user.id]["lang"]
    if shopBot._userPocket[user.id]["step"] >= 23:
        shopBot._userPocket[user.id]["step"] = 32
    elif shopBot._userPocket[user.id]["step"] == -1:
        shopBot._userPocket[user.id]["step"] = -11
    else:
        shopBot._userPocket[user.id]["step"] = 33
    await callBack.message.delete()
    await client.send_message(user.id , shopBot.sendMessageToUserMessage[lang] ,reply_markup=shopBot.backToUserPannelButton[lang])


@Client.on_message(filters.private & (check_step(32) | check_step(33) | check_step(-11)))
async def forward_message_to_admins(client : Client , message : Message):
    user = message.from_user
    lang = shopBot._userPocket[user.id]["lang"]
    userInfo = shopBot._DB.get_user_by_telegramID(user.id)
    for id in shopBot._admins:
        await client.send_message(chat_id = id , text = shopBot.convert_user_data_to_text(userInfo)[lang])
        await message.copy(id , reply_markup=shopBot.message_answer_button(user.id)[lang])
    await message.reply_text(shopBot.messageSentSuccesMessage[lang])
    if shopBot._userPocket[user.id]["step"] == 32:
        shopBot._userPocket[user.id]["step"] = 23
    elif shopBot._userPocket[user.id]["step"] == -11:
        shopBot._userPocket[user.id]["step"] = -1
    else:
        shopBot._userPocket[user.id]["step"] = 3
        await message.reply_text(text=shopBot.userPannelMessage[lang],reply_markup= shopBot.userPannelButton[lang])

@Client.on_callback_query(query_filter("userPannel") & join_filter)
async def return_user_pannel(client : Client , callBack : CallbackQuery):
    user = callBack.from_user
    lang = shopBot._userPocket[user.id]["lang"]
    shopBot._userPocket[user.id]["step"] = 3
    await callBack.message.delete()
    await client.send_message(chat_id = user.id ,text=shopBot.userPannelMessage[lang],reply_markup= shopBot.userPannelButton[lang])


@Client.on_callback_query(query_filter("userPannel") & ~join_filter)
async def handle_not_joined_to_pannel(client : Client , callBack : CallbackQuery):
    user = callBack.from_user
    lang = shopBot._userPocket[user.id]["lang"]
    await callBack.message.delete()
    await client.send_message(user.id , shopBot.joinCheckerMessage[lang],reply_markup=shopBot.get_channels_buttons())


@Client.on_callback_query(query_filter("adminPannel"))
async def return_admin_pannel(client : Client , callBack : CallbackQuery):
    user = callBack.from_user
    lang = shopBot._userPocket[user.id]["lang"]
    if user.id in shopBot._admins:
        shopBot._userPocket[user.id]["step"] = 23
        await callBack.message.delete()
        await client.send_message(user.id ,shopBot.userPannelMessage[lang],reply_markup= shopBot.adminPannelButton[lang])
    else:
        await callBack.answer(shopBot.futureNotAvailableMessage[lang] , show_alert=True)
    

@Client.on_callback_query(query_filter("submitNewAd") & check_step(3))
async def get_title(client : Client , callBack : CallbackQuery):
    user = callBack.from_user
    lang = shopBot._userPocket[user.id]["lang"]
    if await join_Checker(client , callBack):
        shopBot._userPocket[user.id]["step"] = 7
        await callBack.message.delete()
        await client.send_message(chat_id = user.id ,text=shopBot.getAdTitleMessage[lang],reply_markup= shopBot.backToUserPannelButton[lang])
    else:
        await client.send_message(user.id , shopBot.joinCheckerMessage[lang],reply_markup=shopBot.get_channels_buttons())


@Client.on_message(filters.private & ~(filters.text) & (check_step(7) | check_step(11)))
async def wrong_ad_title(client : Client , message : Message):
    user = message.from_user
    lang = shopBot._userPocket[user.id]["lang"]
    await client.send_message(chat_id = user.id ,text=shopBot.getAdTitleMessage[lang],reply_markup= shopBot.backToUserPannelButton[lang])


@Client.on_message(filters.private & filters.text & check_step(7))
async def set_ad_title(client : Client , message : Message):
    user = message.from_user
    lang = shopBot._userPocket[user.id]["lang"]
    shopBot._userPocket[user.id]["step"] = 8
    numOfAds = shopBot._DB.get_num_of_user_ads(user.id)
    shopBot._userPocket[user.id]["ad"] = Ad(user.id , str(user.id)+"-"+str(numOfAds+1),None , message.text , None )
    await client.send_message(chat_id = user.id ,text=shopBot.getPriceMessage[lang],reply_markup= shopBot.backToUserPannelButton[lang])  

    
@Client.on_message(filters.private & filters.text & check_step(8))
async def get_ad_price(client : Client , message : Message):
    user = message.from_user
    lang = shopBot._userPocket[user.id]["lang"]
    if str(message.text).isdigit():
        shopBot._userPocket[user.id]["step"] = 9
        shopBot._userPocket[user.id]["ad"].set_price(int(message.text))
        await client.send_message(chat_id = user.id ,text=shopBot.getImageMessage[lang],reply_markup= shopBot.backToUserPannelButton[lang])  
    else:
        await client.send_message(chat_id = user.id ,text=shopBot.getPriceMessage[lang],reply_markup= shopBot.backToUserPannelButton[lang]) 


@Client.on_message(filters.private & ~filters.text & (check_step(8) | check_step(12)))
async def wrong_ad_price(client : Client , message : Message):
    user = message.from_user
    lang = shopBot._userPocket[user.id]["lang"]
    await client.send_message(chat_id = user.id ,text=shopBot.getPriceMessage[lang],reply_markup= shopBot.backToUserPannelButton[lang])  


@Client.on_message(filters.private & ~filters.photo & (check_step(9) | check_step(13)))
async def get_ad_images(client : Client , message : Message):
    user = message.from_user
    lang = shopBot._userPocket[user.id]["lang"]
    await client.send_message(chat_id = user.id ,text=shopBot.getImageMessage[lang],reply_markup= shopBot.backToUserPannelButton[lang])  


@Client.on_message(filters.private & filters.photo & check_step(9))
async def set_ad_images(client : Client , message : Message):
    user = message.from_user
    lang = shopBot._userPocket[user.id]["lang"]
    currentAd = shopBot._userPocket[user.id]["ad"]
    shopBot._userPocket[user.id]["step"] = 10
    currentAd.change_photoID(message.photo.file_id)
    await client.send_photo(user.id ,message.photo.file_id , currentAd._title ,reply_markup=shopBot.submit_ad_button(currentAd._price , 0)[lang] )


@Client.on_callback_query(query_filter("submitAd") & check_step(10))
async def submit_ad(client : Client , callBack : CallbackQuery):
    user = callBack.from_user
    lang = shopBot._userPocket[user.id]["lang"]
    ad = shopBot._userPocket[user.id]["ad"]
    photoID = callBack.message.photo.file_id
    sentMessage = await client.send_photo(shopBot.saveChannel ,photoID,caption=ad._title , reply_markup=shopBot.link_to_bot_button(ad._price))
    shopBot._DB.add_new_ad(user.id ,ad._adID ,sentMessage.id ,ad._title,photoID, ad.get_submitDate() , ad._price)
    await client.edit_message_caption(user.id , callBack.message.id , ad._title)
    shopBot._userPocket[user.id]["step"] = 3
    await callBack.answer(shopBot.adSubmittedSuccesfullyMessage[lang] , show_alert=True)
    await client.send_message(chat_id = user.id ,text=shopBot.userPannelMessage[lang],reply_markup= shopBot.userPannelButton[lang])


@Client.on_callback_query(query_filter("price") | query_filter("view"))
async def unusable_button_answer(client : Client , callBack : CallbackQuery):
    user = callBack.from_user
    lang = shopBot._userPocket[user.id]["lang"]
    await callBack.answer(shopBot.unusableCallBackMessage[lang])
    

@Client.on_callback_query(query_filter("showUserAds") & check_step(3))
async def show_all_users_ads(client : Client , callBack : CallbackQuery):
    user = callBack.from_user
    lang = shopBot._userPocket[user.id]["lang"]
    if await join_Checker(client , callBack):
        ads = shopBot._DB.get_all_ads_by_telegramID(user.id)
        if ads == None:
            await callBack.answer(shopBot.noAdSubmittedMessage[lang] , show_alert=True)
        else:
            await callBack.message.delete()
            shopBot._userPocket[user.id]["step"] = 10
            for ad in ads:
                await client.send_photo(user.id , ad["photoID"] , ad["title"], reply_markup=shopBot.edit_ad_button(ad["price"],ad["adID"],ad["views"])[lang])
    else:
        await client.send_message(user.id , shopBot.joinCheckerMessage[lang],reply_markup=shopBot.get_channels_buttons())


@Client.on_callback_query(query_filter_regex("editTitle") & (check_step(10) | check_step(23)))
async def get_new_ad_title(client : Client , callBack : CallbackQuery):
    user = callBack.from_user
    lang = shopBot._userPocket[user.id]["lang"]
    await callBack.message.delete()
    await client.send_message(user.id , shopBot.getAdTitleMessage[lang], reply_markup=shopBot.backToUserPannelButton[lang])
    if callBack.data[9] != "0" :
        shopBot._userPocket[user.id]["ad"] = shopBot._DB.get_ad_by_adID(callBack.data[9:])
    shopBot._userPocket[user.id]["step"] = 11


@Client.on_callback_query(query_filter_regex("editPrice") & (check_step(10) | check_step(23)))
async def get_new_ad_Price(client : Client , callBack : CallbackQuery):
    user = callBack.from_user
    lang = shopBot._userPocket[user.id]["lang"]
    await callBack.message.delete()
    await client.send_message(user.id , shopBot.getPriceMessage[lang],reply_markup=shopBot.backToUserPannelButton[lang])
    if callBack.data[9] != "0" :
        shopBot._userPocket[user.id]["ad"] = shopBot._DB.get_ad_by_adID(callBack.data[9:])
    shopBot._userPocket[user.id]["step"] = 12

 
@Client.on_callback_query(query_filter_regex("editPhoto") & (check_step(10) | check_step(23)))
async def get_new_ad_Photo(client : Client , callBack : CallbackQuery):
    user = callBack.from_user
    lang = shopBot._userPocket[user.id]["lang"]
    await callBack.message.delete()
    await client.send_message(user.id , shopBot.getImageMessage[lang],reply_markup=shopBot.backToUserPannelButton[lang])
    if callBack.data[9] != "0" :
        shopBot._userPocket[user.id]["ad"] = shopBot._DB.get_ad_by_adID(callBack.data[9:])
    shopBot._userPocket[user.id]["step"] = 13


@Client.on_callback_query(query_filter_regex("deleteAd") & (check_step(10) | check_step(23)))
async def delete_ad(client : Client , callBack : CallbackQuery):
    user = callBack.from_user
    lang = shopBot._userPocket[user.id]["lang"]
    currentAd = shopBot._userPocket[user.id]["ad"]
    await callBack.message.delete()
    shopBot._DB.delete_ad_by_AdID(callBack.data[8:])
    if user.id in shopBot._admins:
        shopBot._userPocket[user.id]["step"] = 23 
        await client.send_message(user.id ,shopBot.adDeletedSuccesfullyMessage[lang] , reply_markup=shopBot.backToAdminPannelButton[lang])
    else:
        await callBack.answer(shopBot.adDeletedSuccesfullyMessage[lang] , show_alert=True)
        await client.send_message(user.id ,shopBot.userPannelMessage[lang],reply_markup= shopBot.userPannelButton[lang])


@Client.on_message(filters.private & filters.text & check_step(11))
async def edit_ad_title(client : Client , message : Message):
    user = message.from_user
    lang = shopBot._userPocket[user.id]["lang"]
    currentAd = shopBot._userPocket[user.id]["ad"]
    if type(currentAd) == dict:
        shopBot._DB.edit_ad_title(currentAd["adID"] ,message.text)
        await client.edit_message_caption(shopBot.saveChannel ,int(currentAd["saveID"] )
            , message.text , reply_markup=shopBot.price_button(currentAd["price"]))
        if user.id in shopBot._admins:
            shopBot._userPocket[user.id]["step"] = 23
            await client.send_message(user.id ,shopBot.editSuccesfullMessage[lang],reply_markup= shopBot.adminPannelButton[lang])
        else:
            shopBot._userPocket[user.id]["step"] = 3
            await message.reply_text(shopBot.editSuccesfullMessage[lang])
            await message.reply_text(shopBot.userPannelMessage[lang],reply_markup= shopBot.userPannelButton[lang])
    else:
        shopBot._userPocket[user.id]["step"] = 10
        currentAd.set_title(message.text)
        await client.send_photo(user.id ,currentAd._photoID , currentAd._title 
            ,reply_markup=shopBot.submit_ad_button(currentAd._price , 0)[lang])


@Client.on_message(filters.private & filters.text & check_step(12))
async def edit_ad_price(client : Client , message : Message):
    user = message.from_user
    lang = shopBot._userPocket[user.id]["lang"]
    currentAd = shopBot._userPocket[user.id]["ad"]
    if str(message.text).isdigit():
        if type(currentAd) == dict:
            shopBot._DB.edit_ad_price(currentAd["adID"] ,message.text)
            await client.edit_message_reply_markup(shopBot.saveChannel ,int(currentAd["saveID"]) , reply_markup=shopBot.price_button(message.text))
            if user.id in shopBot._admins:
                shopBot._userPocket[user.id]["step"] = 23
                await client.send_message(user.id ,shopBot.editSuccesfullMessage[lang],reply_markup= shopBot.adminPannelButton[lang])
            else:
                shopBot._userPocket[user.id]["step"] = 3
                await message.reply_text(shopBot.editSuccesfullMessage[lang])
                await message.reply_text(text=shopBot.userPannelMessage[lang],reply_markup= shopBot.userPannelButton[lang])
        else:
            shopBot._userPocket[user.id]["step"] = 10
            currentAd.set_price(int(message.text))
            await message.reply_text(shopBot.editSuccesfullMessage[lang])
            await client.send_photo(user.id ,currentAd._photoID ,currentAd._title ,reply_markup=shopBot.submit_ad_button(currentAd._price , 0)[lang])
    else:
        await client.send_message(chat_id = user.id ,text=shopBot.getPriceMessage[lang],reply_markup= shopBot.backToUserPannelButton[lang]) 


@Client.on_message(filters.private & filters.photo & check_step(13))
async def edit_ad_photo(client : Client , message : Message):
    user = message.from_user
    lang = shopBot._userPocket[user.id]["lang"]
    currentAd = shopBot._userPocket[user.id]["ad"]
    if type(currentAd) == dict:
        if message.photo.file_size > 2048000:
            await message.reply_text(shopBot.largeImageMessage[lang]
                    ,reply_markup=shopBot.backToUserPannelButton[lang])
        else:
            shopBot._DB.edit_ad_PhotoID(currentAd["adID"] ,message.photo.file_id)
            await client.download_media(message , f"cache/{user.id}.jpg")
            await client.edit_message_media(shopBot.saveChannel ,int(currentAd["saveID"])
                    , InputMediaPhoto(f"cache/{user.id}.jpg"), reply_markup=shopBot.price_button(currentAd["price"]))
            os.remove(f"cache/{user.id}.jpg")
            await client.edit_message_caption(shopBot.saveChannel ,int(currentAd["saveID"] )
                , currentAd["title"] , reply_markup=shopBot.price_button(currentAd["price"]))
            if user.id in shopBot._admins:
                shopBot._userPocket[user.id]["step"] = 23
                await client.send_message(user.id ,shopBot.editSuccesfullMessage[lang],reply_markup= shopBot.adminPannelButton[lang])
            else:
                shopBot._userPocket[user.id]["step"] = 3
                await message.reply_text(shopBot.editSuccesfullMessage[lang])
                await client.send_message(chat_id = user.id ,text=shopBot.userPannelMessage[lang],reply_markup= shopBot.userPannelButton[lang])
    else:
        shopBot._userPocket[user.id]["step"] = 10
        currentAd.change_photoID(message.photo.file_id)
        await client.send_photo(user.id ,message.photo.file_id , currentAd._title 
            ,reply_markup=shopBot.submit_ad_button(currentAd._price , 0)[lang] )


@Client.on_callback_query(query_filter("searchAd") & (check_step(3)))
async def get_search_title(client : Client , callBack : CallbackQuery):
    user = callBack.from_user
    lang = shopBot._userPocket[user.id]["lang"]
    await callBack.message.delete()
    if await join_Checker(client , callBack):
        await client.send_message(user.id , shopBot.getSearchTitleMessage[lang],reply_markup=shopBot.backToUserPannelButton[lang])
        shopBot._userPocket[user.id]["step"] = 14
    else:
        await client.send_message(user.id , shopBot.joinCheckerMessage[lang],reply_markup=shopBot.get_channels_buttons())
        

@Client.on_message(filters.private & filters.text & check_step(14))
async def show_wanted_ads_to_user(client : Client , message : Message):
    user = message.from_user
    lang = shopBot._userPocket[user.id]["lang"]
    ads = shopBot._DB.find_wanted_ads_by_title(message.text)
    if ads == None:
            await message.reply_text(shopBot.noAdFoundMessage[lang] , reply_markup=shopBot.backToUserPannelButton[lang])
    else:
        for ad in ads:
            await client.send_photo(user.id , ad["photoID"] , ad["title"],reply_markup=shopBot.searched_ad_button(ad["price"],ad["userID"] , ad["adID"],ad["views"])[lang])


@Client.on_message(filters.private & ~(filters.text) & check_step(14))
async def wrong_search_ad_title(client : Client , message : Message):
    user = message.from_user
    lang = shopBot._userPocket[user.id]["lang"]
    await client.send_message(chat_id = user.id ,text=shopBot.getSearchTitleMessage[lang],reply_markup= shopBot.backToUserPannelButton[lang])
    

@Client.on_callback_query(query_filter_regex("messageToUser"))
async def get_message_to_user(client : Client , callBack : CallbackQuery):
    user = callBack.from_user
    lang = shopBot._userPocket[user.id]["lang"]
    if shopBot._userPocket[user.id]["step"] >= 23:
        shopBot._userPocket[user.id]["step"] = 31
    elif shopBot._userPocket[user.id]["step"] == -1:
        shopBot._userPocket[user.id]["step"] = -10
    else:
        shopBot._userPocket[user.id]["step"] = 30

    shopBot._userPocket[user.id]["forwardTo"] = int(callBack.data[13:])
    await client.send_message(user.id , shopBot.sendMessageToUserMessage[lang],reply_markup=shopBot.backToUserPannelButton[lang])


@Client.on_message(filters.private & (check_step(31) | check_step(30) | check_step(-10)))
async def forward_message_to_user(client : Client , message : Message):
    user = message.from_user
    lang = shopBot._userPocket[user.id]["lang"]
    try:
        name = shopBot._DB.get_user_by_telegramID(user.id)['name']
        alertMessage = await client.send_message(shopBot._userPocket[user.id]["forwardTo"] , shopBot.alert_message_for_forwarding_messages(name)[lang])
        await message.copy(shopBot._userPocket[user.id]["forwardTo"] , reply_to_message_id=alertMessage.id , reply_markup=shopBot.message_answer_button(user.id)[lang])
        await message.reply_text(shopBot.messageSentSuccesMessage[lang] , reply_markup=shopBot.backToUserPannelButton[lang])
        if shopBot._userPocket[user.id]["step"] == 31:
            shopBot._userPocket[user.id]["step"] = 23
        elif shopBot._userPocket[user.id]["step"] == -10:
            shopBot._userPocket[user.id]["step"] = -1
        else:
            shopBot._userPocket[user.id]["step"] = 3
    except Exception as e:
        print(e)
        await message.reply_text(shopBot.errorOccuredMessage[lang] , reply_markup=shopBot.backToUserPannelButton[lang])
        

@Client.on_callback_query(query_filter_regex("reportAd"))
async def report_ad(client : Client , callBack : CallbackQuery):
    user = callBack.from_user
    lang = shopBot._userPocket[user.id]["lang"]
    for id in shopBot._admins:
        await client.send_message(chat_id = int(id) , text = shopBot.report_ad_to_admin(user.id , callBack.data[8:])[shopBot._userPocket[int(id)]["lang"]],
                reply_markup=shopBot.see_ad_button(callBack.data[8:])[shopBot._userPocket[int(id)]["lang"]])
    await client.send_message(user.id , shopBot.reportSentSuccesfullyMessage[lang],reply_markup=shopBot.backToUserPannelButton[lang])