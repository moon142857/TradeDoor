import tushare as ts
import numpy as np
import matplotlib.pyplot as plt
import random
import math

import datetime
import tushare as ts
import pymysql
import stock_one



# p = stock_one.oneday('sh.600123', '20150102', '20210218')
# print(p)
# exit()

starttime = '20170102'
endtime = '20210218'

all = []

a = ['SH.600206', datetime.date(2017, 1, 3), 10.0739, 496, datetime.date(2021, 2, 10), 11.33, 12.460511999999987, 236.9613760000003]
b = ['SH.600206', datetime.date(2017, 1, 3), 10.0739, 496, datetime.date(2021, 2, 10), 11.33, 12.460511999999987, 236.9613760000003]
all.append(a)
all.append(b)



x = []
y = []




db = pymysql.connect(host='127.0.0.1', user='root', passwd='', db='tushare', charset='utf8')
cursor = db.cursor()
try:
    sql = "select * from stock_basic order by ts_code;"
    cursor.execute(sql)
    stockbasic = np.array(cursor.fetchall())
    
    for i in range(stockbasic.shape[0]):
        isgo = 0
        #print(stockbasic[i,:][0], stockbasic[i,:][1])
        if int(stockbasic[i,:][1]) >= 600000 and int(stockbasic[i,:][1]) < 600589: #600589:
            isgo = 1
        if int(stockbasic[i,:][1]) >= 1 and int(stockbasic[i,:][1]) < 898:
            isgo = 1
        # if int(stockbasic[i,:][1]) == 600160:
        #     isgo = 1
        if isgo == 0:
            continue

        realcode = stockbasic[i,:][0][7]+stockbasic[i,:][0][8]+'.'+stockbasic[i,:][1]
        print(i, realcode)
        
        p = stock_one.oneday(realcode, starttime, endtime)
        print(p)
        all.append(p)
        
except Exception as err:
    print(err)

cursor.close()
db.close()

all = np.array(all)
v1 = np.sort(all[:,6])
v2 = np.sort(all[:,7])

x = np.arange(all.shape[0])


# out_list = np.array([list(item) for item in zip(x,y)])

# print(out_list)
# out_list = out_list[np.lexsort(out_list.T)]
# print(out_list)

np.savez('all_data', all)

plt.title("ALL") 
plt.xlabel("x") 
plt.ylabel("price") 
plt.ylim([-100,300])
plt.plot(x,v1,linestyle='--',color='red') 
plt.plot(x,v2,linestyle='--',color='green') 
plt.show()
