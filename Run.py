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

from MyStrategy import MyStrategy

try:
    import talib
except:
    print('请安装TA-Lib库')
    sys.exit(-1)


def init(context):
    set_backtest(initial_cash=1e7)
    reg_kdata('min', 1)
    context.Tlen = len(context.target_list)
    # 获取当前绝对路径
    path = os.path.split(os.path.realpath(__file__))[0]
    with open(path+"//CTA_setting.json") as f:
        context.paraDict = json.load(f)[0]
    context.N = 101

def on_data(context):
    data = get_reg_kdata(reg_idx=context.reg_kdata[0], length=context.N + 1, fill_up=True, df=True)
    if data['close'].isna().any():
        return
    datalist = [data[data['target_idx'] == x] for x in pd.unique(data.target_idx)]
    bar = get_current_bar()
    for i, target in enumerate(datalist):
        strategy = MyStrategy(context, target)
        strategy.on5MinBar(bar.ix[i])


if __name__ == '__main__':
    target = ['cffex.if0000']
    run_backtest('MyStrategy', 'Run.py', target_list=target, frequency='min', fre_num=5,
                 begin_date='2016-01-01', end_date='2019-03-31', fq=1)
