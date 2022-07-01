from unittest import result
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings


from linebot import LineBotApi, WebhookParser, WebhookHandler
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import *

from mylinebot import secret 
from .scraper import IFoodie
from .config import County

line_bot_api = LineBotApi(secret.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(secret.LINE_CHANNEL_SECRET)



flag = 0
result = None
@csrf_exempt
def callback(request):
    global flag, result
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')
 
        try:
            events = parser.parse(body, signature)  # 傳入的事件
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()
        
        for event in events:
            if isinstance(event, MessageEvent) :  # 如果有訊息事件
                if  event.message.text in County:                        
                    flag = 2
                    result = event.message.text
                    if len(event.message.text) == 2:
                        if event.message.text == '澎湖' or event.message.text == '金門':
                            result = event.message.text +'縣'
                        elif result[0] == '臺':
                            result = result.replace('臺','台')
                    
                    elif len(event.message.text) == 3:
                        if result[0] == '臺':
                            result = result.replace('臺','台')
                        
                        # else:
                        #     result = event.message.text +'市'
                    
                # if isinstance(event, MessageEvent) and len(event.message.text) == 3 and event.message.text in County:
                #     flag = 3;
                if event.message.text == "查詢":
                    print('第一階段')
                    flag = 1
                    line_bot_api.reply_message(  # 回復傳入的訊息文字
                        event.reply_token,
                        TemplateSendMessage(
                            alt_text='Buttons template',
                            template=ButtonsTemplate(
                                title='找美食',
                                text='請選擇要查詢的地區',
                                actions=[
                                    PostbackTemplateAction(
                                        label='北區',
                                        text='北區',
                                        data='A&北區',
                                    ),
                                    PostbackTemplateAction(
                                        label='中區',
                                        text='中區',
                                        data='A&中區'
                                    ),
                                    PostbackTemplateAction(
                                        label='南區',
                                        text='南區',
                                        data='A&南區'
                                    ),
                                    PostbackTemplateAction(
                                        label='東區和離島',
                                        text='東區和離島',
                                        data='A&東區和離島'
                                    )
                                ]
                            )
                        )
                    )
                    
                if isinstance(event, MessageEvent) and flag == 2 and event.message.text in County:
                    # flag = 3
                    print('成功囉')
                    print(flag)
                    line_bot_api.reply_message(  # 回復傳入的訊息文字
                        event.reply_token,
                        TemplateSendMessage(
                            alt_text='Buttons template',
                            template=ButtonsTemplate(
                                title='找美食',
                                text='請選擇想要的價格區間',
                                actions=[
                                    PostbackTemplateAction(
                                        label='150以內',
                                        text='150以內',
                                        data='B&&1',
                                    ),
                                    PostbackTemplateAction(
                                        label='150-600',
                                        text='150-600',
                                        data='B&&2'
                                    ),
                                    PostbackTemplateAction(
                                        label='600-1200',
                                        text='600-1200',
                                        data='B&&3'
                                    ),
                                    PostbackTemplateAction(
                                        label='1200以上',
                                        text='1200以上',
                                        data='B&&4'
                                    )
                                ]
                            )
                        )
                    )
                    
            elif isinstance(event, PostbackEvent):  # 如果有回傳值事件
                if event.postback.data[0:1] == "A":  # 如果回傳值為「選擇地區」
                    if event.postback.data[2:] == "北區":
                        flag = 2
                        
                        flex_message = TextSendMessage(text='請選擇要查詢的縣市',
                                    quick_reply=QuickReply(items=[
                                        QuickReplyButton(action=MessageAction(label="台北市", text="台北市")),
                                        QuickReplyButton(action=MessageAction(label="新北市", text="新北市")),
                                        QuickReplyButton(action=MessageAction(label="基隆市", text="基隆市")),
                                        QuickReplyButton(action=MessageAction(label="桃園市", text="桃園市")),
                                        QuickReplyButton(action=MessageAction(label="新竹市", text="新竹市")),
                                        QuickReplyButton(action=MessageAction(label="新竹縣", text="新竹縣")),
                                        QuickReplyButton(action=MessageAction(label="宜蘭縣", text="宜蘭縣"))
                                    ]))
                        
                        line_bot_api.reply_message(event.reply_token, flex_message)
                        
                    elif event.postback.data[2:] == "中區":
                        flag = 2
                    
                        flex_message = TextSendMessage(text='請選擇要查詢的縣市',
                                    quick_reply=QuickReply(items=[
                                        QuickReplyButton(action=MessageAction(label="苗栗縣", text="苗栗縣")),
                                        QuickReplyButton(action=MessageAction(label="台中市", text="台中市")),
                                        QuickReplyButton(action=MessageAction(label="彰化縣", text="彰化縣")),
                                        QuickReplyButton(action=MessageAction(label="南投縣", text="南投縣")),
                                        QuickReplyButton(action=MessageAction(label="雲林縣", text="雲林縣"))
                                    ]))
                        
                        line_bot_api.reply_message(event.reply_token, flex_message)
                    # else:
                    #     line_bot_api.reply_message(event.reply_token, TextSendMessage(message))
                        
                        
                
                    elif event.postback.data[2:] == "南區":
                        flag = 2
                    
                        flex_message = TextSendMessage(text='請選擇要查詢的縣市',
                                    quick_reply=QuickReply(items=[
                                        QuickReplyButton(action=MessageAction(label="嘉義市", text="嘉義市")),
                                        QuickReplyButton(action=MessageAction(label="嘉義縣", text="嘉義縣")),
                                        QuickReplyButton(action=MessageAction(label="台南市", text="台南市")),
                                        QuickReplyButton(action=MessageAction(label="高雄市", text="高雄市")),
                                        QuickReplyButton(action=MessageAction(label="屏東縣", text="屏東縣")),
                                        QuickReplyButton(action=MessageAction(label="澎湖縣", text="澎湖縣"))
                                    ]))
                        
                        line_bot_api.reply_message(event.reply_token, flex_message)
                    # else:
                    #     line_bot_api.reply_message(event.reply_token, TextSendMessage(message))
                    
                    
                    elif event.postback.data[2:] == "東區和離島":
                        flag = 2
                    
                        flex_message = TextSendMessage(text='請選擇要查詢的縣市',
                                    quick_reply=QuickReply(items=[
                                        QuickReplyButton(action=MessageAction(label="花蓮縣", text="花蓮縣")),
                                        QuickReplyButton(action=MessageAction(label="台東縣", text="台東縣")),
                                        QuickReplyButton(action=MessageAction(label="金門縣", text="金門縣"))
                                    ]))
                        
                        line_bot_api.reply_message(event.reply_token, flex_message) # 把按鈕呈現給使用者看
                        
                if event.postback.data[0:1] == "B": 
                    if event.postback.data[2:] == "&1":
                        
                        food = IFoodie(
                            result,
                            '1'
                        )
                        
                        line_bot_api.reply_message(  # 爬取該地區正在營業，且符合所選擇的消費價格的前五大最高人氣餐廳
                        event.reply_token,
                        TextSendMessage(text=food.scrape())
                        )
                    
                    
                    if event.postback.data[2:] == "&2":
                        
                        food = IFoodie(
                            result,
                            '2'
                        )
                        
                        line_bot_api.reply_message(  # 爬取該地區正在營業，且符合所選擇的消費價格的前五大最高人氣餐廳
                        event.reply_token,
                        TextSendMessage(text=food.scrape())
                        )    
                    
                    if event.postback.data[2:] == "&3":
                        
                        food = IFoodie(
                            result,
                            '3'
                        )
                        
                        line_bot_api.reply_message(  # 爬取該地區正在營業，且符合所選擇的消費價格的前五大最高人氣餐廳
                        event.reply_token,                       
                        TextSendMessage(text=food.scrape())
                        )    
                    
                    if event.postback.data[2:] == "&4":
                        
                        food = IFoodie(
                            result,
                            '4'
                        )
                        
                        line_bot_api.reply_message(  # 爬取該地區正在營業，且符合所選擇的消費價格的前五大最高人氣餐廳
                        event.reply_token,                        
                        TextSendMessage(text=food.scrape())
                        )        
                
                    # else:
                    #     line_bot_api.reply_message(event.reply_token, TextSendMessage(message))
                    
                      
        return HttpResponse()
    else:
        return HttpResponseBadRequest()
