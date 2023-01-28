from __future__ import unicode_literals
import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler 
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import datetime
import configparser
import bisect
import random

app = Flask(__name__)


config = configparser.ConfigParser()
config.read('config.ini')
GROUP_ID = config.get('line-bot', 'group_id')
line_bot_api = LineBotApi(config.get('line-bot', 'channel_access_token'))
handler = WebhookHandler(config.get('line-bot', 'channel_secret'))
collection_day = [datetime.datetime(2023,1,25), datetime.datetime(2023,2,1), datetime.datetime(2023,2,8), datetime.datetime(2023,2,5), 
                  datetime.datetime(2023,2,22), datetime.datetime(2023,3,1), datetime.datetime(2023,3,8), datetime.datetime(2023,3,15), 
                  datetime.datetime(2023,3,22), datetime.datetime(2023,3,29), datetime.datetime(2023,4,5), datetime.datetime(2023,4,12),
                  datetime.datetime(2023,4,19), datetime.datetime(2023,4,26), datetime.datetime(2023,5,3), datetime.datetime(2023,5,10), 
                  datetime.datetime(2023,5,17), datetime.datetime(2023,5,24), datetime.datetime(2023,5,31), datetime.datetime(2023,6,7),
                  datetime.datetime(2023,6,14), datetime.datetime(2023,6,21), datetime.datetime(2023,6,28)]
collections_type = {}
for i, day in enumerate(collection_day):
    if i % 2 != 0:
        collections_type[day] = 3
    else:
        collections_type[day] = 2


# @app.route("/callback", methods=['POST'])
# def callback():
#     print('trigger')
#     signature = request.headers['X-Line-Signature']
#     pushmsg()
#     body = request.get_data(as_text=True)
#     app.logger.info("Request body: " + body)
#     app.logger.info("test")
#     try:
#         print(body, signature)
#         handler.handle(body, signature)
        
#     except InvalidSignatureError:
#         print("error")
#         abort(400)

#     return 'OK'

# #學你說話
# @handler.add(MessageEvent, message=TextMessage)
# def pretty_echo(event):
#     print(event.source)
#     if event.source.user_id != "Udeadbeefdeadbeefdeadbeefdeadbeef":
        
#         # Phoebe 愛唱歌
#         pretty_note = '♫♪♬'
#         pretty_text = ''
        
#         for i in event.message.text:
        
#             pretty_text += i
#             pretty_text += random.choice(pretty_note)
    
#         line_bot_api.reply_message(
#             event.reply_token,
#             TextSendMessage(text=pretty_text)
#         )

@app.route("/test", methods=['POST'])        
def pushmsg():
    date = request.args.get('day')
    if date != None:
        try:
            print(date)
            current_date = datetime.datetime.strptime(date, '%Y-%m-%d')
        except:
            print('exception occur')
            current_date = datetime.datetime.today()
    else:
        current_date = datetime.datetime.today()
    print(current_date)
    next_collection_day = bisect.bisect_left(collection_day, current_date)
    msg = ""
    if next_collection_day >= len(collection_day):
        msg = "we left"
    else:
        try:
            print(str(collection_day[next_collection_day].strftime("%m%d")))
            msg = str(collection_day[next_collection_day].strftime("%m%d")) + "\n記得丟 \n recycle \n garbage \n compost" if collections_type[collection_day[next_collection_day]] ==3 else str(collection_day[next_collection_day].strftime("%m%d")) + "\n記得丟 \n garbage \n compost"
        except:
            msg = "Error"
    line_bot_api.push_message(GROUP_ID, TextSendMessage(text = msg))
        
    return 'Ok'
if __name__ == "__main__":
    print("start")
    app.run(host = '0.0.0.0')