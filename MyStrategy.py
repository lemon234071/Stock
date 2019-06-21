"""
这里的Demo是一个最简单的双均线策略实现
"""

from __future__ import division
import talib as ta
import numpy as np
from datetime import datetime
from MySignal import MySignal
from atrader import *


class MyStrategy(object):
    className = 'MyStrategy'
    author = 'Yida Wang'

    # 参数列表
    paramList = [
        'symbolList', 'barPeriod', 'lot',
        'timeframeMap',
        'cmiPeriod', 'cmiMaPeriod', 'cmiThreshold',
        'atrPeriod', 'smallAtrTime', 'bigAtrTime',
        'stopAtrTime',
        'lowVolThreshold',
        'hlMaPeriod', 'maPeriod',
    ]

    # ----------------------------------------------------------------------
    def __init__(self, context, target):
        self.context = context
        self.paraDict = context.paraDict
        self.target = target
        self.target_idx = target.target_idx.iloc[0]
        self.long_positions = context.account().positions['volume_long']
        self.short_positions = context.account().positions['volume_short']
        self.close = target.close.values.astype('float')
        self.high = target.high.values.astype('float')
        self.low = target.low.values.astype('float')
        self.update_setting(self.paraDict)
        self.transactionPrice = get_last_order(account_idx=0, target_idx=self.target_idx, position_effect=1)
        self.n_buy = 0

    def update_setting(self, setting: dict):
        """
        Update strategy parameter wtih value in setting dict.
        """
        for name in self.paramList:
            if name in setting:
                setattr(self, name, setting[name])

    def sell(self, price):
        order_target_volume(account_idx=0, target_idx=self.target_idx, target_volume=0, side=1, order_type=2)

    def cover(self, price):
        order_target_volume(account_idx=0, target_idx=self.target_idx, target_volume=0, side=2, order_type=2)

    def cancelAll(self):
        order_cancel_all()

    def buy(self, price):
        order_target_value(account_idx=0, target_idx=self.target_idx, target_value=self.context.initial * 5 / self.context.Tlen,
                           side=1, order_type=1, price=price)

    def short(self, price):
        order_target_value(account_idx=0, target_idx=self.target_idx, target_value=self.context.initial * 5 / self.context.Tlen,
                           side=2, order_type=1, price=price)

    # ----------------------------------------------------------------------
    def onTick(self, tick):
        """收到行情TICK推送"""
        pass

    def on5MinBar(self, bar):
        self.strategy(bar)

    def strategy(self, bar):
        # 根据出场信号出场
        trendStatus, exitLongTrendSignal, exitShortTrendSignal, atr = self.exitSignal()
        exitStatus = self.exitOrder(bar, trendStatus, exitLongTrendSignal, exitShortTrendSignal, atr)

        # 根据进场信号进场
        filterCanTrade, breakUpperBand, breakLowerBand = self.entrySignal()
        if not exitStatus:
            self.entryOrder(bar, filterCanTrade, breakUpperBand, breakLowerBand)

    def exitSignal(self):
        algorithm = MySignal(self.target, self.paraDict)
        trendStatus = 0
        exitLongTrendSignal, exitShortTrendSignal = 0, 0
        trendStatus, cmiMa = algorithm.cmiEnvironment()
        exitLongTrendSignal, exitShortTrendSignal = algorithm.maExit()
        atr = algorithm.atrStoploss()
        return trendStatus, exitLongTrendSignal, exitShortTrendSignal, atr

    def exitOrder(self, bar, trendStatus, exitLongTrendSignal, exitShortTrendSignal, atr):
        exitStatus = 0
        # 执行出场条件
        if trendStatus == 1:
            if exitLongTrendSignal and self.long_positions[self.target_idx] > 0:
                self.sell(bar.close * 0.99)
                exitStatus = 1
            if exitShortTrendSignal and self.short_positions[self.target_idx] > 0:
                self.cover(bar.close * 1.01)
                exitStatus = 1
        else:
            # 止损出场
            print("止损")
            longStop, shortStop = None, None
            if self.transactionPrice is not None:
                self.transactionPrice = self.transactionPrice.price.values.astype('float')
                longStop = self.transactionPrice - self.stopAtrTime * atr[-1]
                shortStop = self.transactionPrice + self.stopAtrTime * atr[-1]
            # 洗价器
            if (self.long_positions[self.target_idx] > 0):
                if (bar.low< longStop):
                    # print('LONG stopLoss')
                    self.cancelAll()
                    self.sell(bar.close * 0.99)
                    exitStatus = 1
            elif (self.short_positions[self.target_idx] > 0):
                if (bar.high > shortStop):
                    # print('SHORT stopLoss')
                    self.cancelAll()
                    self.cover(bar.close * 1.01)
                    exitStatus = 1
        return exitStatus

    def entrySignal(self):
        algorithm = MySignal(self.target, self.paraDict)
        breakUpperBand, breakLowerBand = 0, 0
        trendStatus, cmiMa = algorithm.cmiEnvironment()
        filterCanTrade = algorithm.filterLowAtr()
        if trendStatus == 0:
            breakUpperBand, breakLowerBand, upperBand, lowerBand = algorithm.breakBandSignal()
        elif trendStatus == 1:
            breakUpperBand, breakLowerBand, upperBand, lowerBand = algorithm.breakTrendBand()
        # 画图记录数据
        # self.chartLog['datetime'].append(datetime.strptime(amSignal.datetime[-1], "%Y%m%d %H:%M:%S"))
        # self.chartLog['cmiMa'].append(cmiMa[-1])
        # self.chartLog['upperBand'].append(upperBand)
        # self.chartLog['lowerBand'].append(lowerBand)

        return filterCanTrade, breakUpperBand, breakLowerBand

    def entryOrder(self, bar, filterCanTrade, breakUpperBand, breakLowerBand):
        if filterCanTrade == 1:
            if breakUpperBand and (self.long_positions[self.target_idx] == 0):
                #print(2)
                if self.short_positions[self.target_idx] == 0:
                    self.buy(bar.close * 1.01)  # 成交价*1.01发送高价位的限价单，以最优市价买入进场
                # 如果有空头持仓，则先平空，再做多
                elif self.short_positions[self.target_idx] > 0:
                    self.cancelAll()  # 撤销挂单
                    self.cover(bar.close * 1.01)
                    self.buy(bar.close * 1.01)
            elif breakLowerBand and (self.short_positions[self.target_idx] == 0):
                #print(3)
                if self.long_positions[self.target_idx] == 0:
                    self.short(bar.close * 0.99)  # 成交价*0.99发送低价位的限价单，以最优市价卖出进场
                elif self.long_positions[self.target_idx] > 0:
                    self.cancelAll()  # 撤销挂单
                    self.sell(bar.close * 0.99)
                    self.short(bar.close * 0.99)

    # ----------------------------------------------------------------------
    def onTrade(self, trade):
        """收到成交推送"""
        pass

    # ----------------------------------------------------------------------
    def onStopOrder(self, so):
        """停止单推送"""
        pass