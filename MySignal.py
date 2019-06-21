import talib as ta
import numpy as np
import pandas as pd

"""
将kdj策略需要用到的信号生成器抽离出来
"""

class MySignal():

    def __init__(self, target, paraDict):
        self.author = 'YidaWang'
        self.paraDict = paraDict
        self.close = target.close.values.astype('float')
        self.high = target.high.values.astype('float')
        self.low = target.low.values.astype('float')

    def cmiEnvironment(self):
        cmiPeriod = self.paraDict["cmiPeriod"]
        cmiMaPeriod = self.paraDict["cmiMaPeriod"]
        cmiThreshold = self.paraDict["cmiThreshold"]

        roc = self.close[cmiPeriod:] - self.close[:-cmiPeriod]
        hl = ta.MAX(self.high, cmiPeriod)-ta.MIN(self.low, cmiPeriod)
        cmiMa = ta.MA(np.abs(roc[-(cmiMaPeriod+10):]/(hl[-(cmiMaPeriod+10):] + 0.000001))*100, cmiMaPeriod)
        trendStatus = 1 if cmiMa[-1] > cmiThreshold else 0
        return trendStatus, cmiMa

    def filterLowAtr(self):
        atrPeriod = self.paraDict["atrPeriod"]
        lowVolThreshold = self.paraDict["lowVolThreshold"]

        # 过滤超小波动率
        atr = ta.ATR(self.high, self.low, self.close, atrPeriod)
        filterCanTrade = 1 if atr[-1] > self.close[-1]*lowVolThreshold else 0
        return filterCanTrade

    def breakBandSignal(self):
        smallAtrTime = self.paraDict["smallAtrTime"]
        bigAtrTime = self.paraDict["bigAtrTime"]
        atrPeriod = self.paraDict["atrPeriod"]

        atr = ta.ATR(self.high, self.low, self.close, atrPeriod)

        # 区分趋势与盘整计算上下轨
        hlcMean = ta.MA((self.high+self.low+self.close)/3, 3)[-1]
        priceDirection = 1 if self.close[-1] > hlcMean else -1
        longMultipler = smallAtrTime if priceDirection==1 else bigAtrTime
        shortMultipler = smallAtrTime if priceDirection==-1 else bigAtrTime
        upperBand = self.close[-1]+longMultipler*atr[-1]
        lowerBand = self.close[-1]-shortMultipler*atr[-1]
        breakUpperBand = self.close[-1]>upperBand and self.close[-2]<upperBand
        if breakUpperBand == True:
            print("bug")
        breakLowerBand = self.close[-1]<lowerBand and self.close[-2]>lowerBand
        if breakLowerBand == True:
            print('bug')

        return breakUpperBand, breakLowerBand, upperBand, lowerBand

    def breakTrendBand(self):
        hlMaPeriod = self.paraDict["hlMaPeriod"]

        upperBand = ta.MA(self.high, hlMaPeriod)[-1]
        lowerBand = ta.MA(self.low, hlMaPeriod)[-1]
        breakUpperBand = self.close[-1]>upperBand and self.close[-2]<upperBand
        breakLowerBand = self.close[-1]<lowerBand and self.close[-2]>lowerBand
        return breakUpperBand, breakLowerBand, upperBand, lowerBand

    def maExit(self):
        maPeriod = self.paraDict['maPeriod']

        # 计算均线出场条件
        exitLongTrendSignal = self.low[-1] < ta.MA(self.close, maPeriod)[-1]
        exitShortTrendSignal = self.high[-1] > ta.MA(self.close, maPeriod)[-1]
        return exitLongTrendSignal, exitShortTrendSignal

    def atrStoploss(self):
        atrPeriod = self.paraDict['atrPeriod']
        atr = ta.ATR(self.high, self.low, self.close, atrPeriod)
        return atr