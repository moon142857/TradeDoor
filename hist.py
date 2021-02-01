import tushare as ts
import numpy as np
import matplotlib.pyplot as plt
import random
import math

openfile = '300696.SZ_20200101_20210131_data.npz'

df = np.load(openfile, allow_pickle=True)
data_1day = df['arr_0'][::-1]
data_15min = df['arr_1'][::-1]
print(data_1day.shape)
print(data_15min.shape)
#d = df.values[:,2]
#y = d[::-1]

y = data_1day[:,2]
x = data_1day[:,1]
#y = data_15min[:,2]
#x = data_15min[:,1]


plt.title("300696") 
plt.xlabel("date") 
plt.ylabel("price") 
plt.plot(x,y) 
plt.show()


