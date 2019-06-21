# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     Channe5
   Description :
   Author :       yidawang
   date：          2019/06/20
-------------------------------------------------
   Change Activity:
                   2019/06/30:
-------------------------------------------------
"""
__author__ = 'yidawang'

'''
大作业
'''
from atrader import *
import numpy as np
import pandas as pd
import sys
import os
import json

from MyStrategy2 import MyStrategy

try:
    import talib
except:
    print('请安装TA-Lib库')
    sys.exit(-1)


def init(context):
    set_backtest(initial_cash=1e7, margin_rate=2)
    reg_kdata('day', 1)
    context.Tlen = len(context.target_list)
    context.initial = 1e7
    context.N = 120
    context.count = 0

    context.reg_ratio = 1
    context.p = 0.5
    context.q = 0.5
    context.state = 'empty'
    context.n_pairs = 1

def on_data(context):
    data = get_reg_kdata(reg_idx=context.reg_kdata[0], length=context.N, fill_up=True, df=True)
    if data['close'].isna().any():
        return
    datalist = [data[data['target_idx'] == x] for x in pd.unique(data.target_idx)]
    bar = get_current_bar()
    for i in range(0, len(datalist)-1, 2):
        strategy = MyStrategy(context, [datalist[i], datalist[i+1]])
        context.count += 1
        # if context.count==471:
        #     print("bug")
        # print(context.count)
        strategy.on5MinBar(bar.ix[i])


if __name__ == '__main__':
    target = ['cffex.if0000', 'shfe.rb0000']# ['CZCE.FG000', 'SHFE.rb0000']# ['cffex.if0000']
    # tarlist = get_code_list('hs300')
    # df = tarlist[tarlist.name == "招商银行"]
    # df2 = tarlist[tarlist.name == "伊利股份"]
    run_backtest('MyStrategy', 'Run2.py', target_list=target, frequency='day', fre_num=1,
                 begin_date='2016-01-01', end_date='2019-03-01', fq=1)
