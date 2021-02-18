import tushare as ts
import numpy as np
import matplotlib.pyplot as plt
import random
import math

import datetime
import tushare as ts
import pymysql

import baostock as bs
import pandas as pd



#openfile = '600007.SH_20200101_20210131_data.npz'
openfile = '600519.SH_20200101_20210131_data.npz'
#openfile = '000735.SZ_20200101_20210131_data.npz'
#openfile = '601360.SH_20200101_20210131_data.npz'
#openfile = '603256.SH_20200101_20210131_data.npz'
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


# 獲取股票代碼插入數據庫
# pro = ts.pro_api()
# data = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
# db = pymysql.connect(host='127.0.0.1', user='root', passwd='', db='tushare', charset='utf8')

# cursor = db.cursor()
# for i in range(data.shape[0]):
#     try:
#         print(i, data.values[i,:][0])
#         sql_insert = "INSERT INTO `tushare`.`stock_basic` (`ts_code`, `symbol`, `name`, `area`, `industry`, `list_date`) VALUES ('%s', '%s', '%s', '%s', '%s', '%s');"% (str(data.values[i,:][0]),str(data.values[i,:][1]),str(data.values[i,:][2]),str(data.values[i,:][3]),str(data.values[i,:][4]),str(data.values[i,:][5]))
#         cursor.execute(sql_insert)
#         db.commit()
#     except Exception as err:
#         print(err)
# cursor.close()
# db.close()
# exit()



starttime = '2015-01-01'
endtime = '2021-02-15'

ts.set_token('6e5f091fb6ddb814e03f977ccb55d632954119789711c034ec1d0564')

# data_1day = ts.pro_bar(ts_code=realcode, adj='qfq', start_date=starttime, end_date=endtime)
# print(data_1day)
# # 15分钟线
# data_15min = ts.pro_bar(ts_code=realcode, adj='qfq', start_date=starttime, end_date=endtime, freq='15min')
# print(data_15min)
# np.savez(realcode+'_'+starttime + '_'+endtime+ '_data', data_1day, data_15min)
# exit()

pro = ts.pro_api()
data = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')


lg = bs.login()
print('login respond error_code:'+lg.error_code)
print('login respond  error_msg:'+lg.error_msg)

for i in range(data.shape[0]):
    try:
        if int(data.values[i,:][1]) < 600037:
            continue

        realcode = data.values[i,:][0][7]+data.values[i,:][0][8]+'.'+data.values[i,:][1]
        print(i, realcode)
        rs = bs.query_history_k_data_plus(realcode,
            "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,isST",
            start_date=starttime, end_date=endtime,
            frequency="d", adjustflag="2")

        if int(rs.error_code) != 0:
            print('query_history_k_data_plus respond error_code:'+rs.error_code)
            print('query_history_k_data_plus respond  error_msg:'+rs.error_msg)
            exit()

        data_list = []
        while (rs.error_code == '0') & rs.next():
            data_list.append(rs.get_row_data())
        result = pd.DataFrame(data_list, columns=rs.fields)
        
#for i in range(len(result)):
#            print(result.values[i][0], result.values[i][1])
        print(result)

        db = pymysql.connect(host='127.0.0.1', user='root', passwd='', db='tushare', charset='utf8')
        cursor = db.cursor()
        for i in range(len(result)):
            try:
                sql_insert = "INSERT INTO `tushare`.`stock_1day` (`ts_code`, `trade_date`, `open`, `high`, `low`, `close`, `pre_close`, `change`, `pct_chg`, `vol`, `amount`, `status`) VALUES ('%s', '%s', '%.4f', '%.4f', '%.4f', '%.4f', '%.4f', '%.4f', '%.4f', '%.4f', '%.4f','%d');"% (str(result.values[i][1]),str(result.values[i][0]),float(result.values[i][2]),float(result.values[i][3]),float(result.values[i][4]),float(result.values[i][5]),float(result.values[i][6]),float(0),float(result.values[i][12]),float(result.values[i][7]),float(result.values[i][8]),int(result.values[i][11]))
#print(sql_insert)
                cursor.execute(sql_insert)
                db.commit()
            except Exception as err:
                print(err)
        cursor.close()
        db.close()
        

        rs = bs.query_history_k_data_plus(realcode,
                    "date,time,code,open,high,low,close,volume,amount,adjustflag",
                        start_date=starttime, end_date=endtime,
                            frequency="15", adjustflag="2")
        if int(rs.error_code) != 0:
            print('query_history_k_data_plus respond error_code:'+rs.error_code)
            print('query_history_k_data_plus respond  error_msg:'+rs.error_msg)
            exit()

        data_list = []
        while (rs.error_code == '0') & rs.next():
            data_list.append(rs.get_row_data())
        result = pd.DataFrame(data_list, columns=rs.fields)

#        for i in range(len(result)):
#            print(result.values[i][1])
        print(result)

        db = pymysql.connect(host='127.0.0.1', user='root', passwd='', db='tushare', charset='utf8')
        cursor = db.cursor()
        for i in range(len(result)):
            try:
                sql_insert = "INSERT INTO `tushare`.`stock_15min` (`ts_code`, `trade_time`, `open`, `close`, `high`, `low`, `vol`, `amount`) VALUES ('%s', '%s', '%.4f', '%.4f', '%.4f', '%.4f', '%.4f', '%.4f');"% (str(result.values[i][2]),str(result.values[i][0]+" "+result.values[i][1][8]+result.values[i][1][9]+":"+result.values[i][1][10]+result.values[i][1][11]+":00" ),float(result.values[i][3]),float(result.values[i][6]),float(result.values[i][4]),float(result.values[i][5]),float(result.values[i][7]),float(result.values[i][8]))
                #print(sql_insert)
                cursor.execute(sql_insert)
                db.commit()
            except Exception as err:
                print(err)
        cursor.close()
        db.close()

        
#        data_1day = ts.pro_bar(ts_code=realcode, adj='qfq', start_date=starttime, end_date=endtime)
#        print(data_1day.shape)
#        [rows, cols] = data_1day.shape
#        data_1day = data_1day.values
#        db = pymysql.connect(host='127.0.0.1', user='root', passwd='', db='tushare', charset='utf8')
#        cursor = db.cursor()
#        for i in range(rows):
#            try:
#                sql_insert = "INSERT INTO `tushare`.`stock_1day` (`ts_code`, `trade_date`, `open`, `high`, `low`, `close`, `pre_close`, `change`, `pct_chg`, `vol`, `amount`) VALUES ('%s', '%s', '%.4f', '%.4f', '%.4f', '%.4f', '%.4f', '%.4f', '%.4f', '%.4f', '%.4f');"% (str(data_1day[i,:][0]),str(data_1day[i,:][1]),float(data_1day[i,:][2]),float(data_1day[i,:][3]),float(data_1day[i,:][4]),float(data_1day[i,:][5]),float(data_1day[i,:][6]),float(data_1day[i,:][7]),float(data_1day[i,:][8]),float(data_1day[i,:][9]),float(data_1day[i,:][10]))
#                cursor.execute(sql_insert)
#                db.commit()
#            except Exception as err:
#                print(err)
#        cursor.close()
#        db.close()


        #if i > 1:
        #    break

#        data_15min = ts.pro_bar(ts_code=realcode, adj='qfq', start_date=starttime, end_date=endtime, freq='15min')
#        [rows15, cols15] = data_15min.shape
#        print(data_15min.shape)
#        data_15min = data_15min.values

#        db = pymysql.connect(host='127.0.0.1', user='root', passwd='', db='tushare', charset='utf8')
#        cursor = db.cursor()
#        for i in range(rows15):
#            try:
#                sql_insert = "INSERT INTO `tushare`.`stock_15min` (`ts_code`, `trade_time`, `open`, `close`, `high`, `low`, `vol`, `amount`) VALUES ('%s', '%s', '%.4f', '%.4f', '%.4f', '%.4f', '%.4f', '%.4f');"% (str(data_15min[i,:][0]),str(data_15min[i,:][1]),float(data_15min[i,:][2]),float(data_15min[i,:][3]),float(data_15min[i,:][4]),float(data_15min[i,:][5]),float(data_15min[i,:][6]),float(data_15min[i,:][7]))
#               cursor.execute(sql_insert)
#                db.commit()
#            except Exception as err:
#                print(err)
#        cursor.close()
#        db.close()
        
    except Exception as err:
        print(err)
bs.logout()

exit()


db = pymysql.connect(host='127.0.0.1', user='root', passwd='', db='tushare', charset='utf8')
cursor = db.cursor()
for i in range(rows):
    try:
        sql_insert = "INSERT INTO `tushare`.`stock_1day` (`ts_code`, `trade_date`, `open`, `high`, `low`, `close`, `pre_close`, `change`, `pct_chg`, `vol`, `amount`) VALUES ('%s', '%s', '%.4f', '%.4f', '%.4f', '%.4f', '%.4f', '%.4f', '%.4f', '%.4f', '%.4f');"% (str(data_1day[i,:][0]),str(data_1day[i,:][1]),float(data_1day[i,:][2]),float(data_1day[i,:][3]),float(data_1day[i,:][4]),float(data_1day[i,:][5]),float(data_1day[i,:][6]),float(data_1day[i,:][7]),float(data_1day[i,:][8]),float(data_1day[i,:][9]),float(data_1day[i,:][10]))
        cursor.execute(sql_insert)
        db.commit()
    except Exception as err:
        print(err)
cursor.close()
db.close()


db = pymysql.connect(host='127.0.0.1', user='root', passwd='', db='tushare', charset='utf8')
cursor = db.cursor()
for i in range(rows15):
    try:
        sql_insert = "INSERT INTO `tushare`.`stock_15min` (`ts_code`, `trade_time`, `open`, `close`, `high`, `low`, `vol`, `amount`) VALUES ('%s', '%s', '%.4f', '%.4f', '%.4f', '%.4f', '%.4f', '%.4f');"% (str(data_15min[i,:][0]),str(data_15min[i,:][1]),float(data_15min[i,:][2]),float(data_15min[i,:][3]),float(data_15min[i,:][4]),float(data_15min[i,:][5]),float(data_15min[i,:][6]),float(data_15min[i,:][7]))
        cursor.execute(sql_insert)
        db.commit()
    except Exception as err:
        print(err)
cursor.close()
db.close()

exit()
