import tushare as ts
import numpy as np
import matplotlib.pyplot as plt
import random
import math

openfile = '300696.SZ_20200101_20210131_data.npz'


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

buy = 0
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
            buy = close
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
            if close15 < prelow:
                balance = balance + position * (close15) * 100
                position = 0
                tradable = 0
                cost = 0
                value = balance + close * position * 100
                print("  sell", data_1day[day][1], value, cost, position, open,close, high,close)
    #            exit()
            else:
                print("      rise", data_1day[day][1], value, cost, position, open,close, high,close)
        else:
            #if close15 > prehigh:
            if open15 > prehigh and close15 > prehigh and index >= 1:
                if open15 > close15:
                    restDay = 1
                else:
                    if (close15 - prehigh) / prehigh > 0.03:
                        restDay = 1
                    else:
                        cost = close15+0.01
                        position = math.floor(balance / (cost) / 100 * random.randint(0,100000)/100000)
                        balance = balance - position * (cost) * 100
                        value = balance + close * position * 100
                        print("buy:", data_1day[day][1], value, cost, position, open,close, high,close)
                        tradable = 0
                        restDay = 1
            elif close15 > prehigh:
                cost = close15+0.01
                position = math.floor(balance / (cost) / 100 * random.randint(0,100000)/100000)
                balance = balance - position * (cost) * 100
                value = balance + close * position * 100
                print("buy:", data_1day[day][1], value, cost, position, open,close, high,close)
                tradable = 0
                restDay = 1

        if index == 16:
            preopen = open
            prehigh = high
            preclose = close
            prelow = low


# [rows, cols] = data_1day.shape
# for i in range(rows):
#     open = data_1day[i,:][2]
#     high = data_1day[i,:][3]
#     close = data_1day[i,:][5]
#     low = data_1day[i,:][4]
#     if i<20:
#         preopen = open
#         prehigh = high
#         preclose = close
#         prelow = low
#         buy = close
#         continue
#     tradable = position

#     if position > 0:
#         if low < prelow:
#             balance = balance + position * (low-0.01) * 100
#             position = 0
#             tradable = 0
#             cost = 0
#             value = balance + close * position * 100
#             print("  sell", data_1day[i,:][1], value, cost, position, open,close, high,close)
# #            exit()
#         else:
#             print("      rise", data_1day[i,:][1], value, cost, position, open,close, high,close)
#     else:
#         if high > prehigh:
#             cost = max(prehigh+0.05,open)
#             position = math.floor(balance / (cost) / 100 * random.randint(0,100000)/100000)
#             balance = balance - position * (cost) * 100
#             value = balance + close * position * 100
# #            print(position)
# #            print(balance)
#             print("buy:", data_1day[i,:][1], value, cost, position, open,close, high,close)
#             tradable = 0
#             continue
#         else:
            
#             print("         drop", data_1day[i,:][1], value, cost, position)


        

#     preopen = open
#     prehigh = high
#     preclose = close
#     prelow = low


print("Full position: ",(preclose - buy)*init_amount)


'''
plt.title("603256") 
plt.xlabel("date") 
plt.ylabel("price") 
plt.plot(x,y) 
plt.show()
'''


