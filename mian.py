# 單個純文字
import json
import requests
import linebot

url = f'https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key=AIzaSyCXXr0iFYbN80g3ThmWZyxMn74oE0fjlF4'
bot = linebot.LineBotApi("0InbEcbLLWpYwg2aX1khDiskD/OR6u+kFg+cpQXfqxIRD7G5HdFpGRfiEpg32mpSt7d5Ofu9id7WlUB26p6UI0mFdRYjVHm0njkBAfu9id7WlUB26p6UI0mFdRYjVHm0njkBBsOT0kSFcLnii3656LbxJbx5 gdB04t89/1O/w1cDnyilFU=")
headers = {'Content-Type': 'application/json'}

@bot.event
def message(event):
    # 檢查訊息類型
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
        response = requests.post(url, headers=headers, json=ping_data)
        print(f"response status_code: {response.status_code}")
        data = response.json()
        # 提取"text"字段
        text = data["candidates"][0]["content"]["parts"][0]["text"]
        bot.reply_message(
                event,
                linebot.TextMessage(text=f"{text}")
            )

