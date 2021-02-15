import tushare as ts
import numpy as np
import matplotlib.pyplot as plt
import random
import math

starttime = '20200101'
endtime = '20210131'
#code = '600000'
#code = '600004'
#code = '600006'
#code = '600007'
#code = '600008'
code = '600009'
#code = '688019'
#code = '600519'
#code = '000735'
#code = '300696'


realcode = ''
alllist = np.load('stock_basic_list.npy', allow_pickle=True)
for i in range(alllist.shape[0]):
    print(i, alllist[i,:])
    if alllist[i,:][1] == code:
        realcode = alllist[i, :][0]
        print(alllist[i, :])
        break
print("find ", realcode)
exit()
ts.set_token('df2e1fcec517cbad6359b3ee4c6c5ba2534ca1e37dc224967acdf509')
#pro = ts.pro_api()
data_1day = ts.pro_bar(ts_code=realcode, adj='qfq', start_date=starttime, end_date=endtime)
print(data_1day)
# 15分钟线
data_15min = ts.pro_bar(ts_code=realcode, adj='qfq', start_date=starttime, end_date=endtime, freq='15min')
print(data_15min)
np.savez(realcode+'_'+starttime + '_'+endtime+ '_data', data_1day, data_15min)
exit()

