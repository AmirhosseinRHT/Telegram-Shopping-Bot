from pyrogram import Client , filters
from pyrogram.types import Message , ReplyKeyboardMarkup , InlineKeyboardButton , InlineKeyboardMarkup

@Client.on_message(filters.command("start"))
def handleStart(client : Client , message : Message):
    message.reply_text("""Hi
this bot can split your videos!
please upload your video""")
    # print(message.from_user.id)