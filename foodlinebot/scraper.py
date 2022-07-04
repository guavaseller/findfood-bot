from unicodedata import category
from bs4 import BeautifulSoup
from abc import ABC, abstractmethod
import requests
from fake_useragent import UserAgent

# 美食抽象類別
class Food(ABC):
 
    def __init__(self, area, price):
        self.area = area  # 地區
        self.price = price  # 消費價格
 
    @abstractmethod
    def scrape(self):
        pass

class Place(ABC):
    
    def __init__(self,area):
        self.area = area  # 地址
        
    
name = [None,None,None,None,None,None,None,None,None,None]

score = [None,None,None,None,None,None,None,None,None,None]

address2 = [None,None,None,None,None,None,None,None,None,None]

price = [None,None,None,None,None,None,None,None,None,None]

link = [None,None,None,None,None,None,None,None,None,None]

picture = [None,None,None,None,None,None,None,None,None,None]

google = [None,None,None,None,None,None,None,None,None,None]

test = [None]

# 爬出經緯度
class GetPlace(Place):
        
    def scrape1(self):
        user_agent = UserAgent()
        user_agent.google
        
        response = requests.get(url=
            "https://www.google.com.tw/maps/place/" + self.area , headers={ 'user-agent': user_agent.random })

        soup = BeautifulSoup(response.content, "html.parser")
        
        text = soup.prettify() #text 包含了html的內容
        initial_pos = text.find(";window.APP_INITIALIZATION_STATE")#尋找;window.APP_INITIALIZATION_STATE所在位置
        data = text[initial_pos+36:initial_pos+83] #將其後的參數進行存取
        # print('下面那行是data')
        # print(data)
        line = tuple(data.split(','))
        num1 = float(line[1]) #這格是經度
        num2 = float(line[2]) #這格是緯度
        line = [num1, num2]
        # print(line)
        
        
        return line

# 愛食記爬蟲
class IFoodie(Food):
       
    def scrape(self):
        response = requests.get(
            "https://ifoodie.tw/explore/" + self.area +
            "/list?sortby=rating&opening=true&priceLevel=" + self.price)
        
        test[0] = str("https://ifoodie.tw/explore/" + self.area +
            "/list?sortby=rating&opening=true&priceLevel=" + self.price)
        
        soup = BeautifulSoup(response.content, "html.parser")
        
        
        cards = soup.find_all(          # 爬取前X筆餐廳卡片資料
            'div', {'class': 'jsx-3292609844 restaurant-info'}, limit=10)
 
        content = ""
              
        cnt = 0
        for card in cards:
            
            title = card.find(  # 餐廳名稱
                "a", {"class": "jsx-3292609844 title-text"}).getText()
            name[cnt] = title[0:40]
            
            google[cnt] = "https://www.google.com.tw/maps/" + title
            
            stars = card.find(  # 餐廳評價
                "div", {"class": "jsx-1207467136 text"}).getText()
            
            score[cnt] = stars
 
            address = card.find(  # 餐廳地址
                "div", {"class": "jsx-3292609844 address-row"}).getText()
            address2[cnt] = address
            
            avgprice = card.find(  # 餐聽均消
                "div", {"class": "jsx-3292609844 avg-price"}).getText()
            avgprice = avgprice.replace('·','')
            price[cnt] = avgprice
                       
            url = card.find(  # 餐聽網址
                class_='jsx-3292609844 title-text', href=True)['href'] # output出來的是url這個物件中，把它當作成dict來處理後，href這個key的value
            link[cnt] = 'https://ifoodie.tw' + url
            
            
            if cnt == 0 or cnt == 1:
                img = card.find(  # 餐聽圖片
                    'img',src = True)['src'] # output出來的是img這個物件中，把它當作成dict來處理後，src這個key的value
                picture[cnt] = img
                content += f"{title}\n{stars}顆星{avgprice}\n地址:{address} \n網址:https://ifoodie.tw{url} \n\n"
                cnt += 1
            else :
                img = card.find(  # 餐聽圖片
                    'img' ,{"class": "jsx-3292609844"})['data-src']# output出來的是img這個物件中，把它當作成dict來處理後，data-src這個key的value
                picture[cnt] = img
                
                # content += f"{title}\n{stars}顆星{avgprice}\n地址:{address} \n網址:https://ifoodie.tw{url} \n\n"#將取得的餐廳名稱、評價及地址連結一起，並且指派給content變數
           
                cnt += 1
                
        return cnt