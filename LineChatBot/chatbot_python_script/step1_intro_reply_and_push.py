
# coding: utf-8

# In[ ]:

from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage
)

import findword


app = Flask(__name__,static_url_path = "/images" , static_folder = "./images/" )

# create a instance for line
# line_bot_api 用來處理消息
line_bot_api = LineBotApi('dEB48QaTDE4AMg6gC6qFagwboz8wvTjqdjN1FiA86UT1w4uIVGar+OkcmRokSPCh9pUWSZsatb/qGSDCVKLEc7rAuecn35bwxPFDEk+IyTJdNZL6jTWwVdJb3QugQCOu+0+Pins8qSdZcWE4yKpVpwdB04t89/1O/w1cDnyilFU=')

# 用來接收外部消息
handler = WebhookHandler('e8f9f9ca2a7697893704f71a43fdce6e')

@app.route("/", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body 驗證封包是否來自Line
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    inputwd = event.message.text
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text='查詢: '+ inputwd + '\n' + findword.queryword(inputwd.lower())),
        timeout=None
    )
#     line_bot_api.reply_message(
#         event.reply_token,
#         TextSendMessage(text=findword.queryword(inputwd.lower()))
#     )
    line_bot_api.push_message(
        'Udb1ec7aa72f878823b99bf6f642fb558',
        TextSendMessage(text=inputwd)
    )      
        
if __name__ == "__main__":
    app.run(host='0.0.0.0')


# In[ ]:



