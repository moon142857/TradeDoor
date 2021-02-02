import tushare as ts
import numpy as np
import matplotlib.pyplot as plt
import random
import math
#openfile = '600519.SH_20200101_20210131_data.npz'
#openfile = '000735.SZ_20200101_20210131_data.npz'
#openfile = '601360.SH_20200101_20210131_data.npz'
openfile = '603256.SH_20200101_20210131_data.npz'
#openfile = '688019.SH_20200101_20210131_data.npz'
#openfile = '601857.SH_20200101_20210131_data.npz'

#ts.set_token('cefe71af0b7f229153b085142bf33e0cca0d5427f291fc488eff9252')
#pro = ts.pro_api()
#df = ts.pro_bar(ts_code='300696.SZ', adj='qfq', start_date='20200101', end_date='20210131')
#df = ts.pro_bar(ts_code='300696.SZ', adj='qfq', start_date='20200101', end_date='20210131')

# 15分钟线
#df = ts.pro_bar(ts_code='300696.SZ', adj='qfq', start_date='20200101', end_date='20210131',freq='15min')

#df = pro.trade_cal(exchange='', start_date='20180901', end_date='20181001', fields='exchange,cal_date,is_open,pretrade_date', is_open='0')
#print(df)

#df = ts.pro_bar(ts_code='600000.SH',
#    freq='1min', 
#    start_date='2020-01-07 09:00:00', 
#    end_date='2020-01-08 17:00:00')
#print(df)

df = np.load(openfile, allow_pickle=True)
data_1day = df['arr_0'][::-1]
data_15min = df['arr_1'][::-1]
print(data_1day.shape)
print(data_15min.shape)
[rows, cols] = data_1day.shape
[rows15, cols15] = data_15min.shape


init_amount = 500000
balance = init_amount #现金余额
value = 0 #市值（现金余额+收盘价格*持仓手数*100）
position = 0 #持仓手数
tradable = 0 #可卖手数
cost = 0 #成本

preopen = 0
prehigh = 0
preclose = 0
prelow = 0
predata = ''

buyPosition = 0
buyBalance = 0.0
buyPrice = 0.0
buyDate = ''
restDay = 0 #=1今天休息

for i in range(rows15):
    day = int(i / 17)
    #print(data_15min[i][1][:10].replace('-', ''))
    #print(data_1day[day][1])
    if data_15min[i][1][:10].replace('-', '') != data_1day[day][1]:
        print("ERR")
        exit()
    else:
        
        open = float(data_1day[day][2])
        high = float(data_1day[day][3])
        close = float(data_1day[day][5])
        low = float(data_1day[day][4])
        #if i<260*17:
        if i<20*17:
            preopen = open
            prehigh = high
            preclose = close
            prelow = low
            buyPosition = math.floor(init_amount / close / 100)
            buyPrice = close
            buyBalance = init_amount - buyPrice*buyPosition * 100
            buyDate = data_1day[day][1]
            continue
        tradable = position
        
        open15 = float(data_15min[i][2])
        close15 = float(data_15min[i][3])
        high15 = float(data_15min[i][4])
        low15 = float(data_15min[i][5])

        index = int(i % 17)
        if index == 0:
            restDay = 0
            continue
        if restDay == 1:
            preopen = open
            prehigh = high
            preclose = close
            prelow = low
            continue

        if position > 0:
            if close15 < cost - (cost * 0.005) or  close15 < prelow - (prelow * 0.005):
            #if close15 < prelow - (prelow * 0.001):
                balance = balance + position * (close15) * 100
                value = balance# + close15 * position * 100
                print("   卖出时间：", data_1day[day][1], "市值：", value, "买入价格：", cost, 
                            "成交手数：",position,  "昨天开盘：", preopen, "昨天收盘：",preclose, prehigh,preclose)
                cost = 0
                position = 0
                tradable = 0
    #            exit()
            #else:
                #print("      rise", data_1day[day][1], value, cost, position, open,close, high,close)
        else:
            #if close15 > prehigh:
            if open15 > prehigh and close15 > prehigh and index >= 1:
                if open15 > close15:
                    restDay = 1
                else:
                    if (close15 - prehigh) / prehigh > 0.03:
                        restDay = 1
                    else:
                        cost = prehigh+min(prehigh*0.005, 0.01)
                        #position = math.floor(balance / (cost) / 100 * random.randint(0,100000)/100000)
                        position = math.floor(balance / (cost) / 100)
                        balance = balance - position * (cost) * 100
                        value = balance + close * position * 100
                        print("买入时间:", data_1day[day][1], "市值：", value, "买入价格：", cost, 
                            "成交手数：",position,  "昨天开盘：", preopen, "昨天收盘：",preclose, prehigh,preclose)
                        tradable = 0
                        restDay = 1
            elif close15 > prehigh:
                cost = prehigh+min(prehigh*0.005, 0.01)
                #position = math.floor(balance / (cost) / 100 * random.randint(0,100000)/100000)
                position = math.floor(balance / (cost) / 100)
                balance = balance - position * (cost) * 100
                value = balance + close * position * 100
                print("买入时间:", data_1day[day][1], "市值：", value, "买入价格：", cost, 
                            "成交手数：",position,  "昨天开盘：", preopen, "昨天收盘：",preclose, prehigh,preclose)
                tradable = 0
                restDay = 1

        if index == 16:
            preopen = open
            prehigh = high
            preclose = close
            prelow = low
            predate = data_1day[day][1]
print("标的             ： ", openfile[:9])
print("无脑+算法购买日期 :  ", buyDate)
print("无脑满仓购买价格  :  ", buyPrice)
print("无脑满仓购买手数  :  ", buyPosition)
print("无脑+算法截止日期 :  ", predate)
print("截止日期的收盘价格:   ", preclose)
print("无脑满仓市值     :   ", (buyBalance + buyPosition* preclose* 100 - init_amount)/init_amount*100, "%")
print("短线算法市值     :   ", (balance + position* preclose*100 -init_amount)/init_amount*100,"%")

