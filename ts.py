import tushare as ts
import numpy as np
import matplotlib.pyplot as plt
import random
import math

ts.set_token('cefe71af0b7f229153b085142bf33e0cca0d5427f291fc488eff9252')
#pro = ts.pro_api()
#df = ts.pro_bar(ts_code='300696.SZ', adj='qfq', start_date='20200101', end_date='20210131')
#df = ts.pro_bar(ts_code='300696.SZ', adj='qfq', start_date='20200101', end_date='20210131')


#df = pro.trade_cal(exchange='', start_date='20180901', end_date='20181001', fields='exchange,cal_date,is_open,pretrade_date', is_open='0')
#print(df)

#df = ts.pro_bar(ts_code='600000.SH',
#    freq='1min', 
#    start_date='2020-01-07 09:00:00', 
#    end_date='2020-01-08 17:00:00')
#print(df)

#ts.get_hist_data('600848')

#df = ts.get_hist_data('603256',start='2020-01-01',end='2021-01-30')
#df = ts.get_hist_data('688019',start='2020-01-01',end='2021-01-30')
#df = ts.get_hist_data('300696',start='2020-01-01',end='2021-01-30')

#df = np.load('./603256.SZ_20200101_20210131.npy', allow_pickle=True)
df = np.load('./300696.SZ_20200101_20210131.npy', allow_pickle=True)
df = df[::-1]
print(df)
#d = df.values[:,2]
#y = d[::-1]


pro = ts.pro_api()

data = pro.trade_cal(exchange='SSE', is_open='1', start_date='20200101', end_date='20210130', fields='cal_date')
x = data.values[:,0]
#print(x)

balance = 500000 #现金余额
value = 0 #市值（现金余额+收盘价格*持仓手数*100）
position = 0 #持仓手数
tradable = 0 #可卖手数
cost = 0 #成本

preopen = 0
prehigh = 0
preclose = 0
prelow = 0

[rows, cols] = df.shape
for i in range(rows):
    open = df[i,:][2]
    high = df[i,:][3]
    close = df[i,:][5]
    low = df[i,:][4]
    if i==0:
        preopen = open
        prehigh = high
        preclose = close
        prelow = low
        continue
    tradable = position

    if position > 0:
        if low < prelow:
            balance = balance + position * (low-0.01) * 100
            position = 0
            tradable = 0
            cost = 0
            value = balance + close * position * 100
            print("  sell", x[i], value, cost, position, open,close, high,close)
#            exit()
        else:
            print("      rise", x[i], value, cost, position, open,close, high,close)
    else:
        if high > prehigh:
            cost = max(prehigh+0.01,open)
            position = math.floor(balance / (cost) / 100 * random.randint(0,100000)/100000)
            balance = balance - position * (cost) * 100
            value = balance + close * position * 100
#            print(position)
#            print(balance)
            print("buy:", x[i], value, cost, position, open,close, high,close)
            tradable = 0
            continue
        else:
            
            print("         drop", x[i], value, cost, position)


        

    preopen = open
    prehigh = high
    preclose = close
    prelow = low






'''
plt.title("603256") 
plt.xlabel("date") 
plt.ylabel("price") 
plt.plot(x,y) 
plt.show()
'''


