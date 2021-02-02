# TradeDoor

交易模型策略请移步知乎链接

`https://zhuanlan.zhihu.com/p/348073931`

根据交易模型

近期会使用Tushare写出交易模型出来

选股100个股 50W模拟盘跑交易结果出来

论证模型是否有效

代码没整理过 极low 但不重要


注册：https://waditu.com/document/1?doc_id=38

导入tushare

`import tushare as ts`

根据股票代码，获取1day和15min数据，服务器不能频繁拉取数据，所以要存下来

`python3 getdata.py`

直方圖

`python3 hist.py`

通过上述交易策略，跑历史数据分析买卖点，，，目前只实现了最最基本一部分
正在更新中...

`python3 ts.py`