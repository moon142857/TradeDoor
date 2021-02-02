import tushare as ts
import numpy as np
import matplotlib.pyplot as plt
import random
import math

starttime = '20200101'
endtime = '20210131'
code = '600519'
#code = '000735'
#code = '300696'


realcode = ''
alllist = np.load('stock_basic_list.npy', allow_pickle=True)
for i in range(alllist.shape[0]):
    if alllist[i,:][1] == code:
        realcode = alllist[i, :][0]
        print(alllist[i, :])
        break
print("find ", realcode)

ts.set_token('c8669572f06badef088440c48a9a1449411b2836fb3a9fa02e9acba1')
#pro = ts.pro_api()
data_1day = ts.pro_bar(ts_code=realcode, adj='qfq', start_date=starttime, end_date=endtime)
print(data_1day.shape)
# 15分钟线
data_15min = ts.pro_bar(ts_code=realcode, adj='qfq', start_date=starttime, end_date=endtime, freq='15min')
print(data_15min.shape)
np.savez(realcode+'_'+starttime + '_'+endtime+ '_data', data_1day, data_15min)
exit()

