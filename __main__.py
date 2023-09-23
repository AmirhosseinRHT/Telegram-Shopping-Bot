from pyrogram import Client 
import logging
logging.basicConfig(level=logging.INFO)
V2rayProxy = {
    "scheme": "socks5",  # "socks5" and "http" are supported
    "hostname": "127.0.0.1",
    "port": 10808,
}

lanternProxy = {
    "scheme": "http",  
    "hostname": "127.0.0.1",
    "port": 49675,
}


myPlugs = {"root": "plugins"}

app = Client(name= "ShoppingBot" , api_hash= , api_id= , proxy= lanternProxy, bot_token= , plugins=myPlugs)
app.run()
