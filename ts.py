import tushare as ts
import numpy as np
import matplotlib.pyplot as plt

#ts.set_token('cefe71af0b7f229153b085142bf33e0cca0d5427f291fc488eff9252')
#pro = ts.pro_api()
#df = pro.trade_cal(exchange='', start_date='20180901', end_date='20181001', fields='exchange,cal_date,is_open,pretrade_date', is_open='0')
#print(df)

#df = ts.pro_bar(ts_code='600000.SH',
#    freq='1min', 
#    start_date='2020-01-07 09:00:00', 
#    end_date='2020-01-08 17:00:00')
#print(df)

#ts.get_hist_data('600848')



import tushare as ts
from matplotlib import pyplot as plt 


df = ts.get_hist_data('603256',start='2020-01-01',end='2021-01-30')
print(df)
d = df.values[:,2]
print(d[::-1])
y = d[::-1]


pro = ts.pro_api()

data = pro.trade_cal(exchange='SSE', is_open='1', start_date='20200101', end_date='20210130', fields='cal_date')
x = data.values[:,0]
print(x)




plt.title("603256") 
plt.xlabel("date") 
plt.ylabel("price") 
plt.plot(x,y) 
plt.show()



