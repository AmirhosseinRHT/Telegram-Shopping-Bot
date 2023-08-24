from pyrogram import Client 
import logging
logging.basicConfig(level=logging.INFO)

proxyV2ray = {
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

app = Client(name= "ShoppingBot" , api_hash= "b45cfb43312e5172db8e2de986403e63", 
                      api_id=21424519 , proxy= proxyV2ray,
                      bot_token="6305005735:AAEQRW6aMHGfRL8qNK6YfWe1jM0YRG8KyQM" , plugins=myPlugs)
app.run()
