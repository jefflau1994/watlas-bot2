import requests
from bs4 import BeautifulSoup
import re
import time
import os
from os import environ
import timeit

USERNAME = environ['USERNAME']
PASSWORD = environ['PASSWORD']

url = "http://watlas.fantasyarea.com/watlas/index.cgi"
sess = requests.session()
response = sess.get(url)

#行動function
def action(dataIn):
    url = "http://watlas.fantasyarea.com/watlas/action.cgi"
    sess.post(url=url, data=dataIn)

def watlasBot():

    start = timeit.default_timer()
    
    #登入
    data = {
        'nm': USERNAME,
        'pw': PASSWORD,
        }

    headers = {
        "Host": "watlas.fantasyarea.com",
        "Origin": "http://watlas.fantasyarea.com",
        "Referer": "http://watlas.fantasyarea.com/watlas/index.cgi",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36"
        }

    url = "http://watlas.fantasyarea.com/watlas/action.cgi"
    response = sess.post(url, data = data, headers = headers)
    soup = BeautifulSoup(response.text, 'lxml')

    #讀取 main 陳列架庫存&體力時間
    mainTable = soup.find_all("table")[4].find_all('tr')[1:]
    stockList = []
    for cell in mainTable:
        stockList.append(cell.contents[5].text[:-1])

    breadCount = stockList[0]
    wineCount = stockList[1]
    eggCount = stockList[2]
    ship1Count = stockList[3]
    ship2Count = stockList[4]
    stamina = soup.find(string="體力時間").parent.parent.contents[1].text

    if len(re.findall(r"\d+", stamina)) == 2:
        hour = int(re.findall(r"\d+", stamina)[0])
        minute = float(re.findall(r"\d+", stamina)[1])/60
    
    if len(re.findall(r"\d+", stamina)) == 1:
        if "小時" in stamina:
            hour = int(re.findall(r"\d+", stamina)[0])
            minute = 0.0
        if "分" in stamina:
            hour = 0
            minute = float(re.findall(r"\d+", stamina)[0])/60

    gameTime = hour + minute


    #讀取 market 市場價格
    response = sess.get("http://watlas.fantasyarea.com/watlas/action.cgi?key=shop-m")
    soup = BeautifulSoup(response.text, 'lxml')
    marketTable = soup.find_all("table")[2].find_all('tr')
    priceList = []
    for cell in marketTable:
        priceList.append(int(cell.contents[1].text[2:].replace(',','')))

 
    #action data
    breadPrice = str(priceList[0])
    winePrice = str(priceList[1])
    woodPrice = str(priceList[3]) #e.g."3160"
    sailPrice = str(priceList[4])
    eggPrice = str(priceList[9])


    #check stock
    response = sess.get("http://watlas.fantasyarea.com/watlas/action.cgi?key=stock")
    soup = BeautifulSoup(response.text, 'lxml')
    
    if soup.find(string = "木材"):
        if soup.find(string = "木材").parent.get('href'):
            woodStock = int(soup.find(string = "木材").parent.parent.parent.contents[3].text[:-4])
        else:
            woodStock = 0
    else:
        woodStock = 0
    if soup.find(string = "帆布"):
        if (soup.find(string = "帆布").parent.get('href')):
            sailStock = int(soup.find(string = "帆布").parent.parent.parent.contents[3].text[:-4])
        else:
            sailStock = 0
    else:
        sailStock = 0
    point = soup.find_all("table")[1].find_all('td')[5].text
    
    def shopM(item,num):
        return    

    buyBread = {'key':'buy-s', 'bk':'m!', 'id':'0','pr': breadPrice, 'sc':'0', 'it':'18', 'num1': '1', 'num2':str(1000-int(breadCount))}
    buyWine = {'key':'buy-s', 'bk':'m!', 'id':'0','pr': winePrice, 'sc':'1', 'it':'19', 'num1': '1', 'num2':str(500-int(wineCount))}
    buyWood25 = {'key':'buy-s', 'bk':'m!', 'id':'0','pr': woodPrice, 'sc':'3', 'it':'15', 'num1': '1', 'num2':str(50-woodStock)}
    buySail25 = {'key':'buy-s', 'bk':'m!', 'id':'0','pr': sailPrice, 'sc':'4', 'it':'16', 'num1': '1', 'num2':str(50-sailStock)}
    buyWood50 = {'key':'buy-s', 'bk':'m!', 'id':'0','pr': woodPrice, 'sc':'3', 'it':'15', 'num1': '1', 'num2':str(50-woodStock)}
    buySail50 = {'key':'buy-s', 'bk':'m!', 'id':'0','pr': sailPrice, 'sc':'4', 'it':'16', 'num1': '1', 'num2':str(50-sailStock)}
    buyWood100 = {'key':'buy-s', 'bk':'m!', 'id':'0','pr': woodPrice, 'sc':'3', 'it':'15', 'num1': '1', 'num2':str(100-woodStock)}
    buySail100 = {'key':'buy-s', 'bk':'m!', 'id':'0','pr': sailPrice, 'sc':'4', 'it':'16', 'num1': '1', 'num2':str(100-sailStock)}
    buyEgg = {'key':'buy-s', 'bk':'m!', 'id':'0','pr': eggPrice, 'sc':'9', 'it':'90', 'num1': '1', 'num2':'1600'}

    makeShip1 = {'key':'item-s', 'bk':'s', 'item':'1', 'no':'0', 'cnt1':'1', 'cnt2':'50'}
    makeShip2 = {'key':'item-s', 'bk':'s', 'item':'1', 'no':'1', 'cnt1':'1', 'cnt2':'25'}

    sellSeed = {'key': 'manor-r', 'bk': 'manor'}
    buySeed1 = {'key': 'manor-s','bk': 'manor','it': '0','num1': '1','num2': '20'}
    buySeed2 = {'key': 'manor-s','bk': 'manor','it': '1','num1': '1','num2': '20'}
    buySeed3 = {'key': 'manor-s','bk': 'manor','it': '2','num1': '1','num2': '20'}

    sweep = {'key':'sweep-s', 'cnt1':'1', 'cnt2': '1'}
    palace = {'key':'palace-s'}
    
    
    #action(sweep)
    response = sess.get("http://watlas.fantasyarea.com/watlas/action.cgi?key=sweep")
    soup = BeautifulSoup(response.text, 'lxml')
    rubbishText = soup.find_all("table")[2].tr.find_all('td')[1].text
    if (re.findall(r"\d+", rubbishText) == []):
        rubbishNum = "0"
    else:
        rubbishNum = re.findall(r"\d+", rubbishText)[0]
    
    if (int(rubbishNum)>30 and gameTime>1):
        action(sweep)
        print("已打掃")
    
    localtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    #Print to console
    print(localtime + '\t包:' + breadCount+'\t酒:'+wineCount+'\t蛋:'+eggCount+'\t船1:'+ship1Count+'\t船2:'+ship2Count+'\t時間:'+stamina+'\tPT:'+point)

    #check 宮殿任務
    response = sess.get("http://watlas.fantasyarea.com/watlas/action.cgi?key=palace")
    soup = BeautifulSoup(response.text, 'lxml')

    if int(point) > 22000:
        need = soup.find(alt = "國王").parent.text
        if "包" in need:
            action(buyBread)
            action(palace)
            print("包任")
        if "酒" in need:
            action(buyWine)
            action(palace)
            print("酒任")
        if "木" in need:
            action(buyWood100)
            action(palace)
            print("木任")
        if "帆" in need:
            action(buySail100)
            action(palace)
            print("帆任")
        if "狗" in need:
            0



    #行動 補充庫存 (包 & 酒 & 蛋 & 船)
    if breadCount == "0" and gameTime>0.22:
        action(buyBread)
        print("已買包")
        gameTime -= 0.22

    if wineCount == "0" and gameTime>0.22:
        action(buyWine)
        print("已買酒")
        gameTime -= 0.22

    if eggCount == "0" and gameTime>0.22:
        action(buyEgg)
        print("已買蛋")
        gameTime -= 0.22

    if (ship1Count == "0" and gameTime > 11.3):
        action(buyWood50)
        action(buySail50)
        action(makeShip1)
        print("已造船1")
        gameTime -= 11.3

    if (ship2Count == "0" and gameTime >8.77):
        action(buyWood25)
        action(buySail25)
        action(makeShip2)
        print("已造船2")
        gameTime -= 8.77


    #行動 買賣種子
    response = sess.get("http://watlas.fantasyarea.com/watlas/action.cgi?key=manor")
    soup = BeautifulSoup(response.text, 'lxml')
    seedTable = soup.find_all("table")[2].find_all('tr')
    seed1count = seedTable[1].contents[3].text[:-2]
    seed2count = seedTable[2].contents[3].text[:-2]
    seed3count = seedTable[3].contents[3].text[:-2]
    if seed1count == "0" and gameTime>0.22:
        #action(sellSeed)
        action(buySeed1)
        #print("已賣種子")
        print("已買種子1")
        gameTime -= 0.22
    if seed2count == "0" and gameTime>0.22:
        #action(sellSeed)
        action(buySeed2)
        #print("已賣種子")
        print("已買種子2")
        gameTime -= 0.22
    if seed3count == "0" and gameTime>0.22:
        #action(sellSeed)
        action(buySeed3)
        #print("已賣種子")
        print("已買種子3")
        gameTime -= 0.22
    
    run_time = timeit.default_timer() - start
    


while(True):
    watlasBot()
    time.sleep(600)
#watlasBot()
