from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, StickerSendMessage
)

app = Flask(__name__)

line_bot_api = LineBotApi('zf1j3LnXiHHxpG8xMUal5EASlxDwc4WeDMxVzJSv01RvZYbwweg5qwUMf53JpNENAlAJwccwwMo7xsJaNEqZodIKRmhdREUlynnb9JSHfTe1yxniVWSKc6Xv+Gz+0O9WFXsma7r5HoTqpyb81wH2DAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('d2b24e856b96cc4a4c741236dfe73d2b')


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
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.txt
    if '給我貼圖' in msg:
        sticker_message = StickerSendMessage(
            package_id='1',
            sticker_id='1'
        ) 

        line_bot_api.reply_message(
        event.reply_token, sticker_message)
        return

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))



if __name__ == "__main__":
    app.run()