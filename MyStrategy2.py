"""
这里的Demo是一个最简单的双均线策略实现
"""

from __future__ import division
from MySignal2 import MySignal
from atrader import *


class MyStrategy(object):
    className = 'MyStrategy'
    author = 'Yida Wang'
    # ----------------------------------------------------------------------
    def __init__(self, context, target):
        self.signal = MySignal(context, target)
        self.context = context
        self.target = target

    # ----------------------------------------------------------------------
    def onTick(self, tick):
        """收到行情TICK推送"""
        pass

    def on5MinBar(self, bar):
        self.strategy(bar)

    def strategy(self, bar):
        # 需要止损
        # 移动计算相关性
        new_state = self.entrySignal()
        self.entryOrder1(new_state)

    def exitSignal(self):
        pass

    def exitOrder(self, bar):
        pass

    def entrySignal(self):
        z_score = self.signal.z_test()
        if z_score > 1:
            # buy x
            return ('buy1')
        elif z_score < -1:
            return ('buy2')
        elif -1 <= z_score <= 1:
            # 如果差大于0
            if z_score >= 0:
                # 在均值上面
                return ('side1')
            # 反之
            else:
                # 在均值下面
                return ('side2')

    def entryOrder(self, new_state):
        total_value = self.context.account().cash.total_asset.values.astype('float') * 0.95 / self.context.n_pairs
        #total_value = self.context.initial / self.context.n_pairs
        # 如果新状态是全仓股票1
        if (new_state == 'buy1'):
            if self.context.state == 'buy2':
                order_close_all(account_idx=0)
            # 做空股票2
            order_target_value(account_idx=0, target_idx=self.target[1].target_idx.iloc[0],
                               target_value=total_value/2, side=2,
                               order_type=2, price=0)
            # 做多股票1
            order_target_value(account_idx=0, target_idx=self.target[0].target_idx.iloc[0],
                               target_value=total_value/2, side=1,
                               order_type=2, price=0)
            # 旧状态更改
            self.context.state = 'buy1'
        # 如果新状态是全仓股票2
        if (new_state == 'buy2'):
            if self.context.state == 'buy1':
                order_close_all(account_idx=0)
            # 做空股票1
            order_target_value(account_idx=0, target_idx=self.target[0].target_idx.iloc[0],
                               target_value=total_value/2, side=2,
                               order_type=2, price=0)
            # 做多股票2
            order_target_value(account_idx=0, target_idx=self.target[1].target_idx.iloc[0],
                               target_value=total_value/2, side=1,
                               order_type=2, price=0)
            # 旧状态更改
            self.context.state = 'buy2'
        # 如果处于全仓一股票状态，但是z-score交叉0点
        if (self.context.state == 'buy1' and new_state == 'side2') or (self.context.state == 'buy2' and new_state == 'side1'):
            order_close_all(account_idx=0)
            # 状态改为‘平’
            self.context.state = 'empty'

    def entryOrder1(self, new_state):
        total_value = self.context.account().cash.total_asset.values.astype('float') * 0.95 / self.context.n_pairs
        # print(total_value)
        # print(self.context.state)
        #total_value = self.context.initial / self.context.n_pairs
        # 如果新状态是全仓股票1
        if new_state == 'buy1':
            # 全卖股票2
            order_target_volume(account_idx=0, target_idx=self.target[1].target_idx.iloc[0],
                                target_volume=0, side=1, order_type=2)
            # 全买股票1
            order_target_value(account_idx=0, target_idx=self.target[0].target_idx.iloc[0],
                               target_value=total_value, side=1,
                               order_type=2, price=0)
            # 旧状态更改
            self.context.state = 'buy1'
        # 如果新状态是全仓股票2
        if new_state == 'buy2':
            # 全卖股票1
            order_target_volume(account_idx=0, target_idx=self.target[0].target_idx.iloc[0],
                                target_volume=0, side=1, order_type=2)
            # 全买股票2
            order_target_value(account_idx=0, target_idx=self.target[1].target_idx.iloc[0],
                               target_value=total_value, side=1,
                               order_type=2, price=0)
            # 旧状态更改
            self.context.state = 'buy2'
        # 如果处于全仓一股票状态，但是z-score交叉0点
        if (self.context.state == 'buy1' and new_state == 'side2') or (self.context.state == 'buy2' and new_state == 'side1'):
            # 按照p,q值将股票仓位调整为默认值
            order_target_value(account_idx=0, target_idx=self.target[0].target_idx.iloc[0],
                               target_value=total_value * self.context.p, side=1,
                               order_type=2, price=0)
            order_target_value(account_idx=0, target_idx=self.target[1].target_idx.iloc[0],
                               target_value=total_value * self.context.q, side=1,
                               order_type=2, price=0)
            # 代码里重复两遍因为要先卖后买，而我们没有特地确定哪个先哪个后
            order_target_value(account_idx=0, target_idx=self.target[0].target_idx.iloc[0],
                               target_value=total_value * self.context.p, side=1,
                               order_type=2, price=0)
            order_target_value(account_idx=0, target_idx=self.target[1].target_idx.iloc[0],
                               target_value=total_value * self.context.q, side=1,
                               order_type=2, price=0)
            # 状态改为‘平’
            self.context.state = 'even'

















