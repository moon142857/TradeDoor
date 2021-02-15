import tushare as ts
import numpy as np
import matplotlib.pyplot as plt
import random
import math

import datetime
import tushare as ts
import pymysql


starttime = '20180102'
endtime = '20210205'



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


x = []
y = []



db = pymysql.connect(host='127.0.0.1', user='root', passwd='', db='tushare', charset='utf8')
cursor = db.cursor()
try:
    sql = "select * from stock_basic order by ts_code;"
    cursor.execute(sql)
    stockbasic = np.array(cursor.fetchall())
    

    for i in range(stockbasic.shape[0]):
        print(stockbasic[i,:][0])
        sql = "select * from stock_1day where ts_code='%s' and trade_date >= '%s' and trade_date < '%s'  order by trade_date asc;" %(stockbasic[i,:][0], starttime,endtime)
        cursor.execute(sql)
        data_1day = np.array(cursor.fetchall())
        #print(data_1day[0])
        #print(data_1day[-1])

        beginclose = float(data_1day[0][6])
        endclose = float(data_1day[-1][6])
        
        buyPosition = math.floor(init_amount / beginclose / 100)
        buyPrice = beginclose
        buyBalance = init_amount - buyPrice*buyPosition * 100
        buyDate = data_1day[0][2]

        totle = (buyBalance + buyPosition* endclose* 100 - init_amount)/init_amount*100
        print(totle)
        print(stockbasic[i,:][1])
        x.append(int(stockbasic[i,:][1]))
        y.append(float(totle))

        open = float(data_1day[-1][3])
        high = float(data_1day[-1][4])
        close = float(data_1day[-1][6])
        low = float(data_1day[-1][5])
        
        print(i)
        if i > 50:
            break
except Exception as err:
    print(err)

cursor.close()
db.close()

out_list = np.array([list(item) for item in zip(x,y)])

print(out_list)
out_list = out_list[np.lexsort(out_list.T)]
print(out_list)

np.savez('all_data', out_list)

plt.title("ALL") 
plt.xlabel("x") 
plt.ylabel("price") 
plt.plot(out_list[:,1]) 
plt.show()
