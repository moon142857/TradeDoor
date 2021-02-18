import tushare as ts
import numpy as np
import matplotlib.pyplot as plt
import random
import math

openfile = 'all_data.npz'

df = np.load(openfile, allow_pickle=True)
all = df['arr_0']

all = np.array(all)
print(all.shape)
print(all)
v1 = np.sort(all[:,6])
v2 = np.sort(all[:,7])

x = np.arange(all.shape[0])

plt.title("ALL")
plt.xlabel("x")
plt.ylabel("price")
plt.ylim([-100,300])
plt.plot(x,v1,linestyle='--',color='red')
plt.plot(x,v2,linestyle='--',color='green')
plt.show()

