from unicodedata import name
from unittest import result
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings


from linebot import LineBotApi, WebhookParser, WebhookHandler
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import *

from mylinebot import secret 
from .scraper import *
from .config import County

line_bot_api = LineBotApi(secret.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(secret.LINE_CHANNEL_SECRET)


@csrf_exempt
def callback(request):
    
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
            flag = 0                
            def create_carousel(i):
                return CarouselColumn(
                    thumbnail_image_url=picture[i],
                    title=name[i],
                    text=address2[i]+'\n'+'評價為' + str(score[i]) + '顆星 ，'+price[i] ,
                    actions=[
                        PostbackTemplateAction(
                            label='前往導航',
                            text='進去後點擊右下角可切換至google map導航喔~',
                            data = 'E&' + str(i) +'&'+str(address2[i])+'&'+ name[i]
                        ),
                        # URITemplateAction(
                        #     label='前往導航',
                        #     text= '評價為' + str(score[i]) + '顆星',
                        #     uri = 'https://www.google.com.tw/maps/place/' + address2[i]
                        # ),
                        URITemplateAction(
                            label='查看更多選擇',
                            text='',
                            uri = more[0]
                        ),                                
                        URITemplateAction(
                            label='查看店家詳細內容',
                            text ='',
                            uri= link[i],
                        )
                    ]
                )
            if isinstance(event, MessageEvent) :  # 如果傳入事件是訊息事件                 
                if event.message.text == "查詢":
                    flag = 1
                    line_bot_api.reply_message(
                        event.reply_token,
                        TemplateSendMessage(
                            alt_text='Buttons template',
                            template=ButtonsTemplate(
                                title='找美食',
                                text='請選擇要查詢的地區',
                                actions=[
                                    PostbackTemplateAction(
                                        label='北區',
                                        text='搜尋:北區',
                                        data='A&北區',
                                    ),
                                    PostbackTemplateAction(
                                        label='中區',
                                        text='搜尋:中區',
                                        data='A&中區'
                                    ),
                                    PostbackTemplateAction(
                                        label='南區',
                                        text='搜尋:南區',
                                        data='A&南區'
                                    ),
                                    PostbackTemplateAction(
                                        label='東區和離島',
                                        text='搜尋:東區和離島',
                                        data='A&東區和離島'
                                    )
                                ]
                            )
                        )
                    )
                    
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
    
                if flag == 2 and event.message.text in County:
                    line_bot_api.reply_message(  # 回復傳入的訊息文字
                        event.reply_token,
                        TextSendMessage(text='今天想吃點什麼呢?',
                            quick_reply=QuickReply(items=[
                                QuickReplyButton(image_url= 'https://i.imgur.com/6hzm4LJ.png',action=PostbackAction(label="牛排", text="搜尋牛排", data='C&'+ result + '&' + '牛排')),
                                QuickReplyButton(image_url= 'https://i.imgur.com/IWFj9Wh.png',action=PostbackAction(label="拉麵", text="搜尋拉麵", data='C&'+ result + '&' + '拉麵')),
                                QuickReplyButton(image_url= 'https://i.imgur.com/NVoTM7A.png',action=PostbackAction(label="壽司", text="搜尋壽司", data='C&'+ result + '&' + '壽司')),
                                QuickReplyButton(image_url= 'https://i.imgur.com/2eVGAgY.png',action=PostbackAction(label="早餐與早午餐", text="搜尋早餐與早午餐", data='C&'+ result + '&' + '早餐與早午餐')),
                                QuickReplyButton(image_url= 'https://i.imgur.com/i3lc2cY.png',action=PostbackAction(label="炸雞", text="搜尋炸雞", data='C&'+ result + '&' + '炸雞')),
                                QuickReplyButton(image_url= 'https://i.imgur.com/iEx9Zea.png',action=PostbackAction(label="義式料理", text="搜尋義式料理", data='C&'+ result + '&' + '義式料理')),
                                QuickReplyButton(image_url= 'https://i.imgur.com/6I2lIm4.png',action=PostbackAction(label="甜點", text="搜尋甜點", data='C&'+ result + '&' + '甜點')),
                                QuickReplyButton(image_url= 'https://i.imgur.com/dUZuiN3.png',action=PostbackAction(label="泰式", text="搜尋泰式", data='C&'+ result + '&' + '泰式')),
                                QuickReplyButton(image_url= 'https://i.imgur.com/QZKPEfs.png',action=PostbackAction(label="韓式", text="搜尋韓式", data='C&'+ result + '&' + '韓式')),
                                QuickReplyButton(image_url= 'https://i.imgur.com/5VuqG7l.png',action=PostbackAction(label="燒烤", text="搜尋燒烤", data='C&'+ result + '&' + '燒烤')),
                                QuickReplyButton(image_url= 'https://i.imgur.com/GDyKwJF.png',action=PostbackAction(label="不分類", text="不分類", data='C&'+ result + '&' + ''))
                            ])
                        )
                    )
                    
            elif isinstance(event, PostbackEvent):  # 如果傳入事件是回傳值事件
                if event.postback.data[0:1] == "A":  # 如果回傳值為「選擇地區」
                    flag = 2
                    if event.postback.data[2:] == "北區":
                        line_bot_api.reply_message(  # 回復傳入的訊息文字
                            event.reply_token,
                            TextSendMessage(text='請選擇要查詢的縣市',
                                quick_reply=QuickReply(items=[
                                    QuickReplyButton(action=PostbackAction(label="台北市", text="您所搜尋的是:台北市", data='B&台北市')),
                                    QuickReplyButton(action=PostbackAction(label="新北市", text="您所搜尋的是:新北市", data='B&新北市')),
                                    QuickReplyButton(action=PostbackAction(label="基隆市", text="您所搜尋的是:基隆市", data='B&基隆市')),
                                    QuickReplyButton(action=PostbackAction(label="桃園市", text="您所搜尋的是:桃園市", data='B&桃園市')),
                                    QuickReplyButton(action=PostbackAction(label="新竹市", text="您所搜尋的是:新竹市", data='B&新竹市')),
                                    QuickReplyButton(action=PostbackAction(label="新竹縣", text="您所搜尋的是:新竹縣", data='B&新竹縣')),
                                    QuickReplyButton(action=PostbackAction(label="宜蘭縣", text="您所搜尋的是:宜蘭縣", data='B&宜蘭縣'))
                                ])
                            )    
                        )
                        
                    elif event.postback.data[2:] == "中區":
                    
                        line_bot_api.reply_message(  # 回復傳入的訊息文字
                            event.reply_token,
                            TextSendMessage(text='請選擇要查詢的縣市',
                                quick_reply=QuickReply(items=[
                                    QuickReplyButton(action=PostbackAction(label="苗栗縣", text="您所搜尋的是:苗栗縣", data='B&苗栗縣')),
                                    QuickReplyButton(action=PostbackAction(label="台中市", text="您所搜尋的是:台中市", data='B&台中市')),
                                    QuickReplyButton(action=PostbackAction(label="彰化縣", text="您所搜尋的是:彰化縣", data='B&彰化縣')),
                                    QuickReplyButton(action=PostbackAction(label="南投縣", text="您所搜尋的是:南投縣", data='B&南投縣')),
                                    QuickReplyButton(action=PostbackAction(label="雲林縣", text="您所搜尋的是:雲林縣", data='B&雲林縣'))
                                ])
                            )
                        )
                
                    elif event.postback.data[2:] == "南區":
                    
                        line_bot_api.reply_message(  # 回復傳入的訊息文字
                            event.reply_token,
                            TextSendMessage(text='請選擇要查詢的縣市',
                                quick_reply=QuickReply(items=[
                                    QuickReplyButton(action=PostbackAction(label="嘉義市", text="您所搜尋的是:嘉義市", data='B&嘉義市')),
                                    QuickReplyButton(action=PostbackAction(label="嘉義縣", text="您所搜尋的是:嘉義縣", data='B&嘉義縣')),
                                    QuickReplyButton(action=PostbackAction(label="台南市", text="您所搜尋的是:台南市", data='B&台南市')),
                                    QuickReplyButton(action=PostbackAction(label="高雄市", text="您所搜尋的是:高雄市", data='B&高雄市')),
                                    QuickReplyButton(action=PostbackAction(label="屏東縣", text="您所搜尋的是:屏東縣", data='B&屏東縣')),
                                    QuickReplyButton(action=PostbackAction(label="澎湖縣", text="您所搜尋的是:澎湖縣", data='B&澎湖縣'))
                                ])
                            )
                        )
                        
                    
                    elif event.postback.data[2:] == "東區和離島":
                    
                        line_bot_api.reply_message(  # 回復傳入的訊息文字
                            event.reply_token,
                            TextSendMessage(text='請選擇要查詢的縣市',
                                quick_reply=QuickReply(items=[
                                    QuickReplyButton(action=PostbackAction(label="花蓮縣", text="您所搜尋的是:花蓮縣", data='B&花蓮縣')),
                                    QuickReplyButton(action=PostbackAction(label="台東縣", text="您所搜尋的是:台東縣", data='B&台東縣')),
                                    QuickReplyButton(action=PostbackAction(label="金門縣", text="您所搜尋的是:金門縣", data='B&金門縣'))
                                ])
                            )
                        )
                
                if event.postback.data[0:1] == "B":
                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text='今天想吃點什麼呢?',               
                            quick_reply=QuickReply(items=[
                                QuickReplyButton(image_url= 'https://i.imgur.com/6hzm4LJ.png',action=PostbackAction(label="牛排", text="搜尋牛排", data='C&'+ event.postback.data[2:] + '&' + '牛排')),
                                QuickReplyButton(image_url= 'https://i.imgur.com/IWFj9Wh.png',action=PostbackAction(label="拉麵", text="搜尋拉麵", data='C&'+ event.postback.data[2:] + '&' + '拉麵')),
                                QuickReplyButton(image_url= 'https://i.imgur.com/NVoTM7A.png',action=PostbackAction(label="壽司", text="搜尋壽司", data='C&'+ event.postback.data[2:] + '&' + '壽司')),
                                QuickReplyButton(image_url= 'https://i.imgur.com/2eVGAgY.png',action=PostbackAction(label="早餐與早午餐", text="搜尋早餐與早午餐", data='C&'+ event.postback.data[2:] + '&' + '早餐與早午餐')),
                                QuickReplyButton(image_url= 'https://i.imgur.com/i3lc2cY.png',action=PostbackAction(label="炸雞", text="搜尋炸雞", data='C&'+ event.postback.data[2:] + '&' + '炸雞')),
                                QuickReplyButton(image_url= 'https://i.imgur.com/iEx9Zea.png',action=PostbackAction(label="義式料理", text="搜尋義式料理", data='C&'+ event.postback.data[2:] + '&' + '義式料理')),
                                QuickReplyButton(image_url= 'https://i.imgur.com/6I2lIm4.png',action=PostbackAction(label="甜點", text="搜尋甜點", data='C&'+ event.postback.data[2:] + '&' + '甜點')),
                                QuickReplyButton(image_url= 'https://i.imgur.com/dUZuiN3.png',action=PostbackAction(label="泰式", text="搜尋泰式", data='C&'+ event.postback.data[2:] + '&' + '泰式')),
                                QuickReplyButton(image_url= 'https://i.imgur.com/QZKPEfs.png',action=PostbackAction(label="韓式", text="搜尋韓式", data='C&'+ event.postback.data[2:] + '&' + '韓式')),
                                QuickReplyButton(image_url= 'https://i.imgur.com/5VuqG7l.png',action=PostbackAction(label="燒烤", text="搜尋燒烤", data='C&'+ event.postback.data[2:] + '&' + '燒烤')),
                                QuickReplyButton(image_url= 'https://i.imgur.com/GDyKwJF.png',action=PostbackAction(label="不分類", text="不分類", data='C&'+ event.postback.data[2:] + '&' + ''))
                            ])
                        )
                    )
                      
                if event.postback.data[0:1] == "C":
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
                                        data='D&1&'+ event.postback.data[2:],
                                    ),
                                    PostbackTemplateAction(
                                        label='150-600',
                                        text='150-600',
                                        data='D&2&'+ event.postback.data[2:],
                                    ),
                                    PostbackTemplateAction(
                                        label='600-1200',
                                        text='600-1200',
                                        data='D&3&'+ event.postback.data[2:],
                                    ),
                                    PostbackTemplateAction(
                                        label='1200以上',
                                        text='1200以上',
                                        data='D&4&'+ event.postback.data[2:],
                                    )
                                ]
                            )
                        )
                    )
                            
                if event.postback.data[0:1] == "D": 
                    find = tuple(event.postback.data.split('&'))
                    if event.postback.data[2:4] == "1&":
                        
                        food = IFoodie(
                            find[2], #這是哪個縣市
                            find[3], #這是哪個分類
                            '1'
                        )
                        
                        if food.scrape()!= 0:
                            amount = food.scrape()
                            line_bot_api.reply_message( 
                                event.reply_token,
                                TemplateSendMessage(                                
                                    alt_text='Carousel template',
                                    template =CarouselTemplate(
                                        columns=[
                                            create_carousel(i) for i in range(amount)
                                        ]        
                                    )
                                )
                            )
                                                        
                        elif food.scrape() == 0:
                            line_bot_api.reply_message(event.reply_token, TextSendMessage(text= '目前這個價位沒有營業中的餐廳喔~'))
                    
                    
                    if event.postback.data[2:4] == "2&":
                        
                        food = IFoodie(
                            find[2], #這是哪個縣市
                            find[3], #這是哪個分類
                            '2'
                        )
                        
                        if food.scrape()!= 0:
                            amount = food.scrape()
                            line_bot_api.reply_message( 
                                event.reply_token,
                                TemplateSendMessage(                                
                                    alt_text='Carousel template',
                                    template =CarouselTemplate(
                                        columns=[
                                            create_carousel(i) for i in range(amount)
                                        ]        
                                    )
                                )
                            )
                        
                        elif food.scrape() == 0:
                            line_bot_api.reply_message(event.reply_token, TextSendMessage(text= '目前這個價位沒有營業中的餐廳喔~'))  
                    
                    if event.postback.data[2:4] == "3&":
                        
                        food = IFoodie(
                            find[2], #這是哪個縣市
                            find[3], #這是哪個分類
                            '3'
                        )
                        
                        if food.scrape()!= 0:
                            amount = food.scrape()
                            line_bot_api.reply_message( 
                                event.reply_token,
                                TemplateSendMessage(                                
                                    alt_text='Carousel template',
                                    template =CarouselTemplate(
                                        columns=[
                                            create_carousel(i) for i in range(amount)
                                        ]        
                                    )
                                )
                            )
                        
                        elif food.scrape() == 0:
                            line_bot_api.reply_message(event.reply_token, TextSendMessage(text= '目前這個價位沒有營業中的餐廳喔~'))   
                    
                    if event.postback.data[2:4] == "4&":
                        
                        food = IFoodie(
                            find[2], #這是哪個縣市
                            find[3], #這是哪個分類
                            '4'
                        )
                        
                        if food.scrape()!= 0:
                            amount = food.scrape()
                            line_bot_api.reply_message( 
                                event.reply_token,
                                TemplateSendMessage(                                
                                    alt_text='Carousel template',
                                    template =CarouselTemplate(
                                        columns=[
                                            create_carousel(i) for i in range(amount)
                                        ]        
                                    )
                                )
                            )
                        
                        elif food.scrape() == 0:
                            line_bot_api.reply_message(event.reply_token, TextSendMessage(text= '目前這個價位沒有營業中的餐廳喔~'))
                                  
                if event.postback.data[0:1] == "E":
                    
                    ans = tuple(event.postback.data.split('&'))
                    addressforgoogle = event.postback.data[3:]                    
                    place = GetPlace(
                        addressforgoogle
                    )

                    latitudeandlongitude = place.scrape1()
                    
                    line_bot_api.reply_message(
                    event.reply_token,                        
                    LocationSendMessage(
                        title = ans[3],
                        address = ans[2],
                        latitude=latitudeandlongitude[1],
                        longitude=latitudeandlongitude[0]
                    )
                    )
                                            
        return HttpResponse()
    else:
        return HttpResponseBadRequest()
