# coding: utf-8
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import requests

#line token
channel_access_token = '0InbEcbLLWpYwg2aX1khDiskD/OR6u+kFg+cpQXfqxIRD7G5HdFpGRfiEpg32mpSt7d5Ofu9id7WlUB26p6UI0mFdRYjVHm0njkBsOT0kSFcwV5f38GTjTRSb3wR8ocObxL6LDnGNn8kr/pJUMqQ7gdB04t89/1O/w1cDnyilFU='
channel_secret = 'a36e97467391e99809dd036b9c594e0b'
line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

app = Flask(__name__)

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
   if event.message.type == "text":
        # 取得訊息內容
        message = event.message.text
        ping_data = {
            "contents": [
                {
                    "parts": [{"text": f"{message}"}]
                }
            ]
        }
        url = f'https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key=AIzaSyCXXr0iFYbN80g3ThmWZyxMn74oE0fjlF4'
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, headers=headers, json=ping_data)
        print(f"response status_code: {response.status_code}")
        data = response.json()
        # 提取"text"字段
        text = data["candidates"][0]["content"]["parts"][0]["text"]
        msg = text
        message = TextSendMessage(text=msg)
        line_bot_api.reply_message(event.reply_token,message)

#    msg= event.message.text
 #   message = TextSendMessage(text=msg)
  #  line_bot_api.reply_message(event.reply_token,message)

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
