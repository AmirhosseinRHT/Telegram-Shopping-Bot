from pyrogram import Client , filters
from pyrogram.types import Message , CallbackQuery
from classes.Handler import shopBot

def query_filter(data):
    async def func(flt, _, query):
        return flt.data == query.data
    return filters.create(func, data=data)

def query_filter_regex(data):
    async def func(flt, _, query):
        return flt.data == query.data[:len(flt.data)]
    return filters.create(func, data=data)

def check_step(step):
    async def func(_, __, message):
        user_id = message.from_user.id
        return shopBot._userPocket[user_id]["step"] == step
    return filters.create(func)

async def join_Checker(client : Client , message):
    try:
        for channel in shopBot._joinChannels:
            temp = await client.get_chat_member(chat_id=channel , user_id=message.from_user.id)
        return True
    except Exception as exp:
        print(exp)
        return False

async def join_Checker_filter(_,client : Client , message):
    stat = True
    try:
        for channel in shopBot._joinChannels:
            temp = await client.get_chat_member(chat_id=channel , user_id=message.from_user.id)
    except Exception as exp:
        print(exp)
        stat = False
    return stat
join_filter = filters.create(join_Checker_filter)


def check_user_started(_ , client :Client , message):
        id = message.from_user.id
        address = str(shopBot._userPocket[id]["lang"])
        return ((address == "Fa") | (address == "En"))
user_started =  filters.create(check_user_started)
