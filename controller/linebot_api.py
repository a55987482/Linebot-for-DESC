from flask import Flask, request, abort

from controller import blueprint

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

import requests
import config
import json

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('+5Se7QxI/1X2qS9YpAX4b6wbDkAk37NdO/TvT6QnleE+ZEtGQsnXmSpyM5GbSJwUJLS+75uIKdacfrCgoe6FtujQpS7VTgnZWo+qII9hQqvvuzSRLWYGg/XKguD3tJBACfISEcEBcSXZPAMjOsU0LAdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('fae5bfce57cf19d935cb2a11d71982c5')

# 監聽所有來自 /callback 的 Post Request
@blueprint.route("/callback", methods=['POST'])
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

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # 確認選單按鈕設計
    command_options_function = {
    '開啟風扇': '6',
    '關閉風扇': '5',
    '風速調整至：弱': '6',
    '風速調整至：中': '7',
    '風速調整至：強': '8',
    '風速調整至：超強': '9',
    '開啟燈具': '1',
    '關閉燈具': '0',
    '亮度調整至：弱': '1',
    '亮度調整至：中': '2',
    '亮度調整至：亮': '3',
    '亮度調整至：超亮': '4',
    }
    for key,value in command_options_function.items():
        print(key,value)
        if key == event.message.text:
            dic_data = {
                'Command':value
            }
            data = json.dumps(dic_data)
            print(data)
            response = requests.post(url=config.url, data=data, headers=config.headers)

    # find event message get dict index 
    menu_options_function = [
    {
        'menu_item': '設備控制',
        'function': Menu_template
    },
    {
        'menu_item': '風扇開關',
        'function': Fan_switch
    },
    {
        'menu_item': '燈具開關',
        'function': Light_switch
    },
    {
        'menu_item': '亮度調整',
        'function': Light_brightness
    },
    {
        'menu_item': '風速調整',
        'function': Fan_speed
    },
    {
        'menu_item': '一鍵關閉',
        'function': One_button_off
    }
    ]
    for item in menu_options_function:
        if item['menu_item'] == event.message.text:
            item['function'](event)

# 風扇開關按鈕
def Fan_switch(event):
    Confirm_template = TemplateSendMessage(
        alt_text='目錄 template',
        template=ConfirmTemplate(
            title='這是ConfirmTemplate',
            text='請選擇風扇 : 開啟 or 關閉',
            actions=[                              
                PostbackTemplateAction(
                    label='開',
                    text='開啟風扇',
                    data='action=buy&itemid=1'
                ),
                MessageTemplateAction(
                    label='關',
                    text='關閉風扇'
                )
            ]
        )
    )
    line_bot_api.reply_message(event.reply_token,Confirm_template)

#風速選擇按鈕
def Fan_speed(event):
    buttons_template = TemplateSendMessage(
        alt_text='Buttons Template',
        template=ButtonsTemplate(
            title='風速調整',
            text='Please調整至您想要的風速',
            actions=[
                PostbackTemplateAction(
                    label='弱',
                    text='風速調整至：弱',
                    data='風速調弱'
                ),
                PostbackTemplateAction(
                    label='中',
                    text='風速調整至：中',
                    data='風速調中'
                ),
                PostbackTemplateAction(
                    label='強',
                    text='風速調整至：強',
                    data='風速調強'
                ),
                PostbackTemplateAction(
                    label='超強',
                    text='風速調整至：超強',
                    data='風速超強'
                )
            ]
        )
    )
    line_bot_api.reply_message(event.reply_token, buttons_template)

# 燈具開關按鈕
def Light_switch(event):
    Confirm_template = TemplateSendMessage(
        alt_text='目錄 template',
        template=ConfirmTemplate(
            title='這是ConfirmTemplate',
            text='請選擇燈具 : 開啟 or 關閉',
            actions=[                              
                PostbackTemplateAction(
                    label='開',
                    text='開啟燈具',
                    data='action=buy&itemid=1'
                ),
                MessageTemplateAction(
                    label='關',
                    text='關閉燈具'
                )
            ]
        )
    )
    line_bot_api.reply_message(event.reply_token,Confirm_template)

#亮度選擇按鈕
def Light_brightness(event):
    buttons_template = TemplateSendMessage(
        alt_text='Buttons Template',
        template=ButtonsTemplate(
            title='亮度調整',
            text='Please調整至您想要的亮度',
            actions=[
                PostbackTemplateAction(
                    label='弱',
                    text='亮度調整至：弱',
                    data='亮度調弱'
                ),
                PostbackTemplateAction(
                    label='中',
                    text='亮度調整至：中',
                    data='亮度調適中'
                ),
                PostbackTemplateAction(
                    label='亮',
                    text='亮度調整至：亮',
                    data='亮度調亮'
                ),
                PostbackTemplateAction(
                    label='超亮',
                    text='亮度調整至：超亮',
                    data='亮度調超亮'
                )
            ]
        )
    )
    line_bot_api.reply_message(event.reply_token, buttons_template)

# 一鍵關閉設備按鈕
def One_button_off(event):
    dic_data = {
            'Command':'0'
    }
    data = json.dumps(dic_data)
    response = requests.post(url=config.url, data=data, headers=config.headers)
    dic_data = {
            'Command':'5'
    }
    data = json.dumps(dic_data)
    response = requests.post(url=config.url, data=data, headers=config.headers)

# Menu選單按鈕
def Menu_template(event):
    Carousel_template = TemplateSendMessage(
    alt_text='Carousel template',
    template=CarouselTemplate(
    columns=[
        CarouselColumn(
            thumbnail_image_url='https://pics.ettoday.net/images/2703/d2703755.jpg',
            title='設備控制',
            text='風扇控制',
            actions=[
                PostbackTemplateAction(
                    label='風扇開關',
                    text='風扇開關',
                    data='action=buy&itemid=2'
                ),
                PostbackTemplateAction(
                    label='風速調整',
                    text='風速調整',
                    data='action=buy&itemid=2'
                ),
                PostbackTemplateAction(
                    label='其他功能',
                    text='尚未完成，敬請期待',
                    data='action=buy&itemid=1'
                )
            ]
        ),
        CarouselColumn(
            thumbnail_image_url='https://images.clipartlogo.com/files/istock/previews/9388/93881751-vector-light-bulb-icon-with-concept-of-idea-brainstorming.jpg',
            title='設備控制',
            text='燈具控制',
            actions=[
                PostbackTemplateAction(
                    label='燈具開關',
                    text='燈具開關',
                    data='action=buy&itemid=2'
                ),
                PostbackTemplateAction(
                    label='亮度調整',
                    text='亮度調整',
                    data='action=buy&itemid=2'
                ),
                PostbackTemplateAction(
                    label='其他功能',
                    text='尚未完成，敬請期待',
                    data='action=buy&itemid=1'
                )
            ]
        )
    ]
    )
    )
    line_bot_api.reply_message(event.reply_token, Carousel_template)