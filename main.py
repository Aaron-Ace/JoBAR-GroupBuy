from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from flask import Flask, request, abort
import os

app = Flask(__name__)

# 填入你的 Channel Access Token
line_bot_api = LineBotApi('YOUR_CHANNEL_ACCESS_TOKEN')
# 填入你的 Channel Secret
handler = WebhookHandler('YOUR_CHANNEL_SECRET')

# 當 Line Bot 收到訊息時，將會觸發此 function
@app.route("/callback", methods=['POST'])
def callback():
    # 取得 Line Server 傳來的資料
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

# 處理收到的文字訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    # 取得使用者傳來的文字訊息
    user_message = event.message.text
    # 回覆使用者傳來的文字訊息
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=user_message)
    )

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
