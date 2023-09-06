from pyrogram import Client , filters
from pyrogram.types import Message , CallbackQuery ,InputMediaPhoto
from classes.Handler import shopBot
from classes.Ad import Ad
import os
from func.createdFilters import *
from func.validatingFuncs import *


@Client.on_callback_query(query_filter("editName") & check_step(3))
async def handle_change_name_button(client : Client , callBack : CallbackQuery):
    user = callBack.from_user
    shopBot._userPocket[user.id]["step"] = 4
    await callBack.message.delete()
    await client.send_message(user.id , shopBot.getNameMessage[shopBot._userPocket[user.id]["lang"]] ,
             reply_markup=shopBot.backToPannelButton[shopBot._userPocket[user.id]["lang"]])


@Client.on_message(filters.text & filters.private & check_step(4))
async def rename_user(client : Client , message : Message):
    user = message.from_user
    shopBot._userPocket[user.id]["step"] = 3
    shopBot._DB.edit_user_name(user.id , message.text)
    await message.reply_text(shopBot.nameChangedSuccesfullyMessage[shopBot._userPocket[user.id]["lang"]])
    await message.reply_text(text=shopBot.userPannelMessage[shopBot._userPocket[user.id]["lang"]]
                ,reply_markup= shopBot.userPannelButton[shopBot._userPocket[user.id]["lang"]])


@Client.on_callback_query(query_filter("editPhone") & check_step(3))
async def handle_change_PhoneNum_button(client : Client , callBack : CallbackQuery):
    user = callBack.from_user
    shopBot._userPocket[user.id]["step"] = 5
    await callBack.message.delete()
    await client.send_message(user.id , shopBot.getPhoneNumberMessage[shopBot._userPocket[user.id]["lang"]]
            , reply_markup=shopBot.backToPannelButton[shopBot._userPocket[user.id]["lang"]])


@Client.on_message(filters.text & filters.private & check_step(5))
async def change_PhoneNum(client : Client , message : Message):
    user = message.from_user
    if validate_phone_number(message.text):
        shopBot._userPocket[user.id]["step"] = 3
        shopBot._DB.edit_user_PhoneNumber(user.id , message.text)
        await message.reply_text(shopBot.PhoneChangedSuccesfullyMessage[shopBot._userPocket[user.id]["lang"]])
        await message.reply_text(text=shopBot.userPannelMessage[shopBot._userPocket[user.id]["lang"]]
                ,reply_markup= shopBot.userPannelButton[shopBot._userPocket[user.id]["lang"]])
    else:
        await message.reply_text(shopBot.phoneNotValidMessage[shopBot._userPocket[user.id]["lang"]])



@Client.on_callback_query(query_filter("sendMessageToAdmin") & check_step(3))
async def handle_send_message_to_admins(client : Client , callBack : CallbackQuery):
    user = callBack.from_user
    shopBot._userPocket[user.id]["step"] = 6
    await callBack.message.delete()
    await client.send_message(user.id , shopBot.sendMessageToAdminMessage[shopBot._userPocket[user.id]["lang"]] ,
            reply_markup=shopBot.backToPannelButton[shopBot._userPocket[user.id]["lang"]])


@Client.on_message(filters.private & check_step(6))
async def forward_message_to_admins(client : Client , message : Message):
    user = message.from_user
    shopBot._userPocket[user.id]["step"] = 3
    userInfo = shopBot._DB.get_user_by_telegramID(user.id)
    for id in shopBot._admins:
        await client.send_message(chat_id = id , text = shopBot.convert_user_data_to_text(userInfo)[shopBot._userPocket[id]["lang"]])
        await message.copy(id , reply_markup=shopBot.message_answer_button(user.id)[shopBot._userPocket[id]["lang"]])


    await message.reply_text(shopBot.messageSentSuccesMessage[shopBot._userPocket[user.id]["lang"]])
    await message.reply_text(text=shopBot.userPannelMessage[shopBot._userPocket[user.id]["lang"]]
                ,reply_markup= shopBot.userPannelButton[shopBot._userPocket[user.id]["lang"]])


@Client.on_callback_query(query_filter("userPannel") & join_filter)
async def return_user_pannel(client : Client , callBack : CallbackQuery):
    user = callBack.from_user
    shopBot._userPocket[user.id]["step"] = 3
    await callBack.message.delete()
    await client.send_message(chat_id = user.id ,text=shopBot.userPannelMessage[shopBot._userPocket[user.id]["lang"]]
                ,reply_markup= shopBot.userPannelButton[shopBot._userPocket[user.id]["lang"]])

@Client.on_callback_query(query_filter("userPannel") & ~join_filter)
async def handle_not_joined_to_pannel(client : Client , callBack : CallbackQuery):
    user = callBack.from_user
    await callBack.message.delete()
    await client.send_message(user.id , shopBot.joinCheckerMessage[shopBot._userPocket[user.id]["lang"]],
                reply_markup=shopBot.get_channels_buttons())

@Client.on_callback_query(query_filter("adminPannel"))
async def return_admin_pannel(client : Client , callBack : CallbackQuery):
    user = callBack.from_user
    shopBot._userPocket[user.id]["step"] = 23
    await callBack.message.delete()
    await client.send_message(chat_id = user.id ,text=shopBot.userPannelMessage[shopBot._userPocket[user.id]["lang"]]
                ,reply_markup= shopBot.adminPannelButton[shopBot._userPocket[user.id]["lang"]])
    

@Client.on_callback_query(query_filter("submitNewAd") & check_step(3))
async def get_title(client : Client , callBack : CallbackQuery):
    user = callBack.from_user
    if await join_Checker(client , callBack):
        shopBot._userPocket[user.id]["step"] = 7
        await callBack.message.delete()
        await client.send_message(chat_id = user.id ,text=shopBot.getAdTitleMessage[shopBot._userPocket[user.id]["lang"]]
                    ,reply_markup= shopBot.backToPannelButton[shopBot._userPocket[user.id]["lang"]])
    else:
        await client.send_message(user.id , shopBot.joinCheckerMessage[shopBot._userPocket[user.id]["lang"]],
                reply_markup=shopBot.get_channels_buttons())



@Client.on_message(filters.private & ~(filters.text) & (check_step(7) | check_step(11)))
async def wrong_ad_title(client : Client , message : Message):
    user = message.from_user
    await client.send_message(chat_id = user.id ,text=shopBot.getAdTitleMessage[shopBot._userPocket[user.id]["lang"]]
                ,reply_markup= shopBot.backToPannelButton[shopBot._userPocket[user.id]["lang"]])



@Client.on_message(filters.private & filters.text & check_step(7))
async def set_ad_title(client : Client , message : Message):
    user = message.from_user
    shopBot._userPocket[user.id]["step"] = 8
    numOfAds = shopBot._DB.get_num_of_user_ads(user.id)
    shopBot._userPocket[user.id]["ad"] = Ad(user.id , str(user.id)+"-"+str(numOfAds+1),None , message.text , None )
    await client.send_message(chat_id = user.id ,text=shopBot.getPriceMessage[shopBot._userPocket[user.id]["lang"]]
                ,reply_markup= shopBot.backToPannelButton[shopBot._userPocket[user.id]["lang"]])  

    
@Client.on_message(filters.private & filters.text & check_step(8))
async def get_ad_price(client : Client , message : Message):
    user = message.from_user
    if str(message.text).isdigit():
        shopBot._userPocket[user.id]["step"] = 9
        shopBot._userPocket[user.id]["ad"].set_price(int(message.text))
        await client.send_message(chat_id = user.id ,text=shopBot.getImageMessage[shopBot._userPocket[user.id]["lang"]]
            ,reply_markup= shopBot.backToPannelButton[shopBot._userPocket[user.id]["lang"]])  
    else:
        await client.send_message(chat_id = user.id ,text=shopBot.getPriceMessage[shopBot._userPocket[user.id]["lang"]]
                    ,reply_markup= shopBot.backToPannelButton[shopBot._userPocket[user.id]["lang"]]) 


@Client.on_message(filters.private & ~filters.text & (check_step(8) | check_step(12)))
async def wrong_ad_price(client : Client , message : Message):
    user = message.from_user
    await client.send_message(chat_id = user.id ,text=shopBot.getPriceMessage[shopBot._userPocket[user.id]["lang"]]
        ,reply_markup= shopBot.backToPannelButton[shopBot._userPocket[user.id]["lang"]])  


@Client.on_message(filters.private & ~filters.photo & (check_step(9) | check_step(13)))
async def get_ad_images(client : Client , message : Message):
    user = message.from_user
    await client.send_message(chat_id = user.id ,text=shopBot.getImageMessage[shopBot._userPocket[user.id]["lang"]]
        ,reply_markup= shopBot.backToPannelButton[shopBot._userPocket[user.id]["lang"]])  


@Client.on_message(filters.private & filters.photo & check_step(9))
async def set_ad_images(client : Client , message : Message):
    user = message.from_user
    shopBot._userPocket[user.id]["step"] = 10
    shopBot._userPocket[user.id]["ad"].change_photoID(message.photo.file_id)
    await client.send_photo(user.id ,message.photo.file_id , shopBot._userPocket[user.id]["ad"]._title 
    ,reply_markup=shopBot.submit_ad_button(shopBot._userPocket[user.id]["ad"]._price , 0)[shopBot._userPocket[user.id]["lang"]] )


@Client.on_callback_query(query_filter("submitAd") & check_step(10))
async def submit_ad(client : Client , callBack : CallbackQuery):
    user = callBack.from_user
    photoID = callBack.message.photo.file_id
    ad = shopBot._userPocket[user.id]["ad"]
    sentMessage = await client.send_photo(shopBot.saveChannel ,photoID
            ,caption=shopBot._userPocket[user.id]["ad"]._title , reply_markup=shopBot.price_button(shopBot._userPocket[user.id]["ad"]._price))
    shopBot._DB.add_new_ad(user.id ,ad._adID ,sentMessage.id ,ad._title,photoID, ad.get_submitDate() , ad._price)
    await client.edit_message_caption(user.id , callBack.message.id , shopBot._userPocket[user.id]["ad"]._title)
    shopBot._userPocket[user.id]["step"] = 3
    await callBack.answer(shopBot.adSubmittedSuccesfullyMessage[shopBot._userPocket[user.id]["lang"]])
    await client.send_message(chat_id = user.id ,text=shopBot.userPannelMessage[shopBot._userPocket[user.id]["lang"]]
                ,reply_markup= shopBot.userPannelButton[shopBot._userPocket[user.id]["lang"]])



@Client.on_callback_query(query_filter("price") | query_filter("view"))
async def unusable_button_answer(client : Client , callBack : CallbackQuery):
    user = callBack.from_user
    await callBack.answer(shopBot.unusableCallBackMessage[shopBot._userPocket[user.id]["lang"]])
    

@Client.on_callback_query(query_filter("showUserAds") & check_step(3))
async def show_all_users_ads(client : Client , callBack : CallbackQuery):
    user = callBack.from_user
    if await join_Checker(client , callBack):
        ads = shopBot._DB.get_all_ads_by_telegramID(user.id)
        if ads == None:
            await callBack.answer(shopBot.noAdSubmittedMessage[shopBot._userPocket[user.id]["lang"]])
        else:
            await callBack.message.delete()
            shopBot._userPocket[user.id]["step"] = 10
            for ad in ads:
                await client.send_photo(user.id , ad["photoID"] , ad["title"]
                , reply_markup=shopBot.edit_ad_button(ad["price"],ad["adID"],ad["views"])[shopBot._userPocket[user.id]["lang"]])
    else:
        await client.send_message(user.id , shopBot.joinCheckerMessage[shopBot._userPocket[user.id]["lang"]],
                reply_markup=shopBot.get_channels_buttons())


@Client.on_callback_query(query_filter_regex("editTitle") & check_step(10))
async def get_new_ad_title(client : Client , callBack : CallbackQuery):
    user = callBack.from_user
    await callBack.message.delete()
    await client.send_message(user.id , shopBot.getAdTitleMessage[shopBot._userPocket[user.id]["lang"]], 
                reply_markup=shopBot.backToPannelButton[shopBot._userPocket[user.id]["lang"]])
    if callBack.data[9] != "0" :
        shopBot._userPocket[user.id]["ad"] = shopBot._DB.get_ad_by_adID(callBack.data[9:])
    shopBot._userPocket[user.id]["step"] = 11


@Client.on_callback_query(query_filter_regex("editPrice") & check_step(10))
async def get_new_ad_Price(client : Client , callBack : CallbackQuery):
    user = callBack.from_user
    await callBack.message.delete()
    await client.send_message(user.id , shopBot.getPriceMessage[shopBot._userPocket[user.id]["lang"]],
                reply_markup=shopBot.backToPannelButton[shopBot._userPocket[user.id]["lang"]])
    if callBack.data[9] != "0" :
        shopBot._userPocket[user.id]["ad"] = shopBot._DB.get_ad_by_adID(callBack.data[9:])
    shopBot._userPocket[user.id]["step"] = 12


@Client.on_callback_query(query_filter_regex("editPhoto") & check_step(10))
async def get_new_ad_Photo(client : Client , callBack : CallbackQuery):
    user = callBack.from_user
    await callBack.message.delete()
    await client.send_message(user.id , shopBot.getImageMessage[shopBot._userPocket[user.id]["lang"]],
                reply_markup=shopBot.backToPannelButton[shopBot._userPocket[user.id]["lang"]])
    if callBack.data[9] != "0" :
        shopBot._userPocket[user.id]["ad"] = shopBot._DB.get_ad_by_adID(callBack.data[9:])
    shopBot._userPocket[user.id]["step"] = 13


@Client.on_callback_query(query_filter_regex("deleteAd") & check_step(10))
async def delete_ad(client : Client , callBack : CallbackQuery):
    user = callBack.from_user
    await callBack.message.delete()
    shopBot._DB
    await client.delete_messages(shopBot.saveChannel , int(shopBot._userPocket[user.id]["ad"]["saveID"]))
    shopBot._DB.delete_ad_by_AdID(callBack.data[8:])
    callBack.answer(shopBot.adDeletedSuccesfullyMessage[shopBot._userPocket[user.id]["lang"]])
    await client.send_message(chat_id = user.id ,text=shopBot.userPannelMessage[shopBot._userPocket[user.id]["lang"]]
        ,reply_markup= shopBot.userPannelButton[shopBot._userPocket[user.id]["lang"]])


@Client.on_message(filters.private & filters.text & check_step(11))
async def edit_ad_title(client : Client , message : Message):
    user = message.from_user
    if type(shopBot._userPocket[user.id]["ad"]) == dict:
        shopBot._DB.edit_ad_title(shopBot._userPocket[user.id]["ad"]["adID"] ,message.text)
        await client.edit_message_caption(shopBot.saveChannel ,int(shopBot._userPocket[user.id]["ad"]["saveID"] )
            , message.text , reply_markup=shopBot.price_button(shopBot._userPocket[user.id]["ad"]["price"]))
        await message.reply_text(shopBot.editSuccesfullMessage[shopBot._userPocket[user.id]["lang"]])
        shopBot._userPocket[user.id]["step"] = 3
        await client.send_message(chat_id = user.id ,text=shopBot.userPannelMessage[shopBot._userPocket[user.id]["lang"]]
            ,reply_markup= shopBot.userPannelButton[shopBot._userPocket[user.id]["lang"]])
    else:
        shopBot._userPocket[user.id]["step"] = 10
        shopBot._userPocket[user.id]["ad"].set_title(message.text)
        await client.send_photo(user.id ,message.photo.file_id , shopBot._userPocket[user.id]["ad"]._title 
            ,reply_markup=shopBot.submit_ad_button(shopBot._userPocket[user.id]["ad"]._price , 0)[shopBot._userPocket[user.id]["lang"]] )


@Client.on_message(filters.private & filters.text & check_step(12))
async def edit_ad_price(client : Client , message : Message):
    user = message.from_user
    if str(message.text).isdigit():
        if type(shopBot._userPocket[user.id]["ad"]) == dict:
            shopBot._DB.edit_ad_price(shopBot._userPocket[user.id]["ad"]["adID"] ,message.text)
            await client.edit_message_reply_markup(shopBot.saveChannel ,int(shopBot._userPocket[user.id]["ad"]["saveID"]) 
            , reply_markup=shopBot.price_button(message.text))
            await message.reply_text(shopBot.editSuccesfullMessage[shopBot._userPocket[user.id]["lang"]])
            shopBot._userPocket[user.id]["step"] = 3
            await client.send_message(chat_id = user.id ,text=shopBot.userPannelMessage[shopBot._userPocket[user.id]["lang"]]
                ,reply_markup= shopBot.userPannelButton[shopBot._userPocket[user.id]["lang"]])
        else:
            shopBot._userPocket[user.id]["step"] = 10
            shopBot._userPocket[user.id]["ad"].set_price(int(message.text))
            await client.send_message(chat_id = user.id ,text=shopBot.getImageMessage[shopBot._userPocket[user.id]["lang"]]
                ,reply_markup= shopBot.backToPannelButton[shopBot._userPocket[user.id]["lang"]])
    else:
        await client.send_message(chat_id = user.id ,text=shopBot.getPriceMessage[shopBot._userPocket[user.id]["lang"]]
            ,reply_markup= shopBot.backToPannelButton[shopBot._userPocket[user.id]["lang"]]) 


@Client.on_message(filters.private & filters.photo & check_step(13))
async def edit_ad_photo(client : Client , message : Message):
    user = message.from_user
    if type(shopBot._userPocket[user.id]["ad"]) == dict:
        if message.photo.file_size > 2048000:
            await message.reply_text(shopBot.largeImageMessage[shopBot._userPocket[user.id]["lang"]]
                                     ,reply_markup=shopBot.backToPannelButton[shopBot._userPocket[user.id]["lang"]])
        else:
            shopBot._DB.edit_ad_PhotoID(shopBot._userPocket[user.id]["ad"]["adID"] ,message.photo.file_id)
            await client.download_media(message , f"cache/{user.id}.jpg")
            await client.edit_message_media(shopBot.saveChannel ,int(shopBot._userPocket[user.id]["ad"]["saveID"])
                    , InputMediaPhoto(f"cache/{user.id}.jpg"), reply_markup=shopBot.price_button(shopBot._userPocket[user.id]["ad"]["price"]))
            os.remove(f"cache/{user.id}.jpg")
            await client.edit_message_caption(shopBot.saveChannel ,int(shopBot._userPocket[user.id]["ad"]["saveID"] )
                , shopBot._userPocket[user.id]["ad"]["title"] , reply_markup=shopBot.price_button(shopBot._userPocket[user.id]["ad"]["price"]))
            await message.reply_text(shopBot.editSuccesfullMessage[shopBot._userPocket[user.id]["lang"]])
            shopBot._userPocket[user.id]["step"] = 3
            await client.send_message(chat_id = user.id ,text=shopBot.userPannelMessage[shopBot._userPocket[user.id]["lang"]]
                ,reply_markup= shopBot.userPannelButton[shopBot._userPocket[user.id]["lang"]])
    else:
        shopBot._userPocket[user.id]["step"] = 10
        shopBot._userPocket[user.id]["ad"].change_photoID(message.photo.file_id)
        await client.send_photo(user.id ,message.photo.file_id , shopBot._userPocket[user.id]["ad"]._title 
            ,reply_markup=shopBot.submit_ad_button(shopBot._userPocket[user.id]["ad"]._price , 0)[shopBot._userPocket[user.id]["lang"]] )


@Client.on_callback_query(query_filter("searchAd") & check_step(3))
async def get_search_title(client : Client , callBack : CallbackQuery):
    user = callBack.from_user
    await callBack.message.delete()
    if await join_Checker(client , callBack):
        await client.send_message(user.id , shopBot.getSearchTitleMessage[shopBot._userPocket[user.id]["lang"]],
            reply_markup=shopBot.backToPannelButton[shopBot._userPocket[user.id]["lang"]])
        shopBot._userPocket[user.id]["step"] = 14
    else:
        await client.send_message(user.id , shopBot.joinCheckerMessage[shopBot._userPocket[user.id]["lang"]],
                reply_markup=shopBot.get_channels_buttons())
        

@Client.on_message(filters.private & filters.text & check_step(14))
async def show_wanted_ads_to_user(client : Client , message : Message):
    user = message.from_user
    ads = shopBot._DB.find_wanted_ads_by_title(message.text)
    if ads == None:
            await message.reply_text(shopBot.noAdFoundMessage[shopBot._userPocket[user.id]["lang"]] , 
                reply_markup=shopBot.backToPannelButton[shopBot._userPocket[user.id]["lang"]])
    else:
        for ad in ads:
            await client.send_photo(user.id , ad["photoID"] , ad["title"]
            , reply_markup=shopBot.searched_ad_button(ad["price"],ad["userID"] , ad["adID"],ad["views"])[shopBot._userPocket[user.id]["lang"]])


@Client.on_message(filters.private & ~(filters.text) & check_step(14))
async def wrong_search_ad_title(client : Client , message : Message):
    user = message.from_user
    await client.send_message(chat_id = user.id ,text=shopBot.getSearchTitleMessage[shopBot._userPocket[user.id]["lang"]]
                ,reply_markup= shopBot.backToPannelButton[shopBot._userPocket[user.id]["lang"]])
    


@Client.on_callback_query(query_filter_regex("messageToUser") & (check_step(14) | check_step(3)))
async def get_message_to_user(client : Client , callBack : CallbackQuery):
    user = callBack.from_user
    await client.send_message(user.id , shopBot.sendMessageToAdminMessage[shopBot._userPocket[user.id]["lang"]],
            reply_markup=shopBot.backToPannelButton[shopBot._userPocket[user.id]["lang"]])
    shopBot._userPocket[user.id]["step"] = 15
    shopBot._userPocket[user.id]["forwardTo"] = callBack.data[13:]


@Client.on_message(filters.private & check_step(15))
async def forward_message_to_user(client : Client , message : Message):
    try:
        user = message.from_user
        name = shopBot._DB.get_user_by_telegramID(user.id)['name']
        alertMessage = await client.send_message(shopBot._userPocket[user.id]["forwardTo"] , 
        shopBot.alert_message_for_forwarding_messages(name)[shopBot._userPocket[user.id]["lang"]])
        await message.copy(shopBot._userPocket[user.id]["forwardTo"] , reply_to_message_id=alertMessage.id , 
            reply_markup=shopBot.message_answer_button(user.id)[shopBot._userPocket[user.id]["lang"]])
        await message.reply_text(shopBot.messageSentSuccesMessage[shopBot._userPocket[user.id]["lang"]])
        shopBot._userPocket[user.id]["step"] = 3
    except:
        await message.reply_text(shopBot.errorOccuredMessage[shopBot._userPocket[user.id]["lang"]]
            , reply_markup=shopBot.backToPannelButton[shopBot._userPocket[user.id]["lang"]])


@Client.on_message(filters.private & check_step(15))
async def forward_message_to_user(client : Client , message : Message):
    try:
        user = message.from_user
        name = shopBot._DB.get_user_by_telegramID(user.id)['name']
        alertMessage = await client.send_message(shopBot._userPocket[user.id]["forwardTo"] , 
        shopBot.alert_message_for_forwarding_messages(name)[shopBot._userPocket[user.id]["lang"]])
        await message.copy(shopBot._userPocket[user.id]["forwardTo"] , reply_to_message_id=alertMessage.id , 
            reply_markup=shopBot.message_answer_button(user.id)[shopBot._userPocket[user.id]["lang"]])
        await message.reply_text(shopBot.messageSentSuccesMessage[shopBot._userPocket[user.id]["lang"]])
        shopBot._userPocket[user.id]["step"] = 3
    except:
        await message.reply_text(shopBot.errorOccuredMessage[shopBot._userPocket[user.id]["lang"]]
            , reply_markup=shopBot.backToPannelButton[shopBot._userPocket[user.id]["lang"]])
        

@Client.on_callback_query(query_filter_regex("reportAd"))
async def report_ad(client : Client , callBack : CallbackQuery):
    user = callBack.from_user
    for id in shopBot._admins:
        await client.send_message(chat_id = id , text = shopBot.report_ad_to_admin(user.id , callBack.data[8:])[shopBot._userPocket[id]["lang"]],
                reply_markup=shopBot.see_ad_button(callBack.data[8:])[shopBot._userPocket[id]["lang"]])

    await client.send_message(user.id , shopBot.reportSentSuccesfullyMessage[shopBot._userPocket[user.id]["lang"]],
            reply_markup=shopBot.backToPannelButton[shopBot._userPocket[user.id]["lang"]])


