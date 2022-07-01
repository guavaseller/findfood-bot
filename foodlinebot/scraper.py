from unicodedata import category
from bs4 import BeautifulSoup
from abc import ABC, abstractmethod
import requests


# 美食抽象類別
class Food(ABC):
 
    def __init__(self, area, price):
        self.area = area  # 地區
        self.price = price  # 消費價格
 
    @abstractmethod
    def scrape(self):
        pass
    
    
# 愛食記爬蟲
class IFoodie(Food):
 
    def scrape(self):
        response = requests.get(
            "https://ifoodie.tw/explore/" + self.area +
            "/list?sortby=rating&opening=true&priceLevel=" + self.price)
        
        soup = BeautifulSoup(response.content, "html.parser")
        
         # 爬取前五筆餐廳卡片資料
        cards = soup.find_all(
            'div', {'class': 'jsx-3292609844 restaurant-info'}, limit=5)
 
        content = ""
        for card in cards:
 
            title = card.find(  # 餐廳名稱
                "a", {"class": "jsx-3292609844 title-text"}).getText()
 
            stars = card.find(  # 餐廳評價
                "div", {"class": "jsx-1207467136 text"}).getText()
 
            address = card.find(  # 餐廳地址
                "div", {"class": "jsx-3292609844 address-row"}).getText()
            
            avgprice = card.find(  # 餐聽均消
                "div", {"class": "jsx-3292609844 avg-price"}).getText()        
 
            #將取得的餐廳名稱、評價及地址連結一起，並且指派給content變數
            content += f"{title} \n{stars}顆星{avgprice}\n地址:{address} \n\n"
 
        return content
# # MENU 美食誌爬蟲
# class Menu(Food):
#     def scrape(self):
#         response = requests.get(
#             "https://menutaiwan.com/tw/restaurants_list/category?city=" + self.area +
#             "&cityId=5d63c42937ca71b646626be5")
        
#         soup = BeautifulSoup(response.content, "html.parser")
        
#          # 爬取前五筆餐廳卡片資料
#         cards = soup.find_all(
#             'div', {'class': "_39ES8ByE42UkRmulkTlRsT"}, limit=5)
 
#         content = ""
#         for card in cards:
 
#             title = card.find(  # 餐廳名稱
#                 "div",  class_="_39ES8ByE42UkRmulkTlRsT", ).getText()
 
#             stars = card.find(  # 餐廳評價
#                 "span", {"class": "recommend__store__card＿ratingScore"}).getText()
 
#             address = card.find(  # 餐廳地址
#                 "p", {"class": "ZFOPgsUsRR03bLNwroL2g"}).getText()
            
#             avgprice = card.find(  # 餐聽均消
#                 "p", {"class": "_1IomHqOntAWyksFvLKHhcf"}, "<::before></::before>").getText()
            
 
 
#             #將取得的餐廳名稱、評價及地址連結一起，並且指派給content變數
#             content += f"{title} \n{stars}顆星\n地址:{address} \n\n"
 
#         return content
