import talib as ta
import numpy as np
import pandas as pd

"""
将kdj策略需要用到的信号生成器抽离出来
"""

class MySignal():

    def __init__(self, context, target):
        self.author = 'YidaWang'
        self.target = target
        self.context = context

    def z_test(self):
        # 获取历史价格
        close1 = self.target[0].close.values.astype('float')
        close2 = self.target[1].close.values.astype('float')

        reg_ratio = self.context.reg_ratio

        # 计算平稳序列
        stable_series = close2 - reg_ratio * close1
        series_mean = np.mean(stable_series)
        sigma = np.std(stable_series)
        # 平稳序列现值与均值相差多少
        diff = stable_series[-1] - series_mean
        # 返回z值
        return (diff / sigma)