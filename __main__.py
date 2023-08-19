from pyrogram import Client 

proxyV2ray = {
    "scheme": "http",  # "socks4", "socks5" and "http" are supported
    "hostname": "127.0.0.1",
    "port": 10809,
}

pluginTest = {"root": "plugins"}

app = Client(name= "VideoSplitterBot" , api_hash= "b45cfb43312e5172db8e2de986403e63", 
                      api_id=21424519 , proxy= proxyV2ray,
                      bot_token="6305005735:AAEQRW6aMHGfRL8qNK6YfWe1jM0YRG8KyQM" , plugins=pluginTest)

app.run()
