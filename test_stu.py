from unittest import TestCase

import pandas as pd
import numpy as np
from task2 import model
import copy

class TestModel(TestCase):

    money = 100000
    test_data_pre = pd.DataFrame(
        columns=['ID', 'Stock Code', 'Time', 'Opening Price','Highest Price', 'Lowest Price'])
    investment_data = pd.DataFrame(
        columns=['Time', 'Stocks you buy', 'Corresponding number of stocks you buy', 'Stocks you sell',
                 'Corresponding number of stocks you sell'])

    s = pd.Timestamp('2009-12-01 09:30:00')
    test_data_pre = test_data_pre.append({'ID': 1, 'Stock Code': 600000, 'Time': s,
                                          'Opening Price': 15.8, 'Highest Price': 15.9, 'Lowest Price': 15},
                                         ignore_index=True)
    test_data_pre = test_data_pre.append({'ID': 1, 'Stock Code': 600004, 'Time': s,
                                          'Opening Price': 25.8, 'Highest Price': 25.9, 'Lowest Price': 25},
                                         ignore_index=True)
    test_data_pre = test_data_pre.append({'ID': 1, 'Stock Code': 600005, 'Time': s,
                                          'Opening Price': 35.8, 'Highest Price': 35.9, 'Lowest Price': 35},
                                         ignore_index=True)
    b = copy.deepcopy(money)
    add_data = model(s, b, test_data_pre[test_data_pre['Time'] <= s], investment_data)
    investment_data = investment_data.append(add_data)


    s = s + pd.Timedelta(minutes=1)
    test_data_pre = test_data_pre.append({'ID': 1, 'Stock Code': 600000, 'Time': s,
                                          'Opening Price': 26.8, 'Highest Price': 26.8, 'Lowest Price': 26.8},
                                         ignore_index=True)
    test_data_pre = test_data_pre.append({'ID': 1, 'Stock Code': 600004, 'Time': s,
                                          'Opening Price': 16.2, 'Highest Price': 17, 'Lowest Price': 16.1},
                                         ignore_index=True)
    test_data_pre = test_data_pre.append({'ID': 1, 'Stock Code': 600005, 'Time': s,
                                          'Opening Price': 36.8, 'Highest Price': 36.9, 'Lowest Price': 36},
                                         ignore_index=True)
    b = copy.deepcopy(money)
    add_data = model(s, b, test_data_pre[test_data_pre['Time'] <= s], investment_data)
    investment_data = investment_data.append(add_data)


    info = investment_data[investment_data.Time == s]
    his = test_data_pre[test_data_pre.Time == s]
    bug_code = info['Stocks you buy'].values[0]
    if type(bug_code) == str:
        bug_price = his[his['Stock Code'] == int(bug_code)]['Opening Price'].values
        money -= bug_price * int(info['Corresponding number of stocks you buy'].values)

    sell_code = info['Stocks you sell'].values[0]
    if type(sell_code) == str:
        sell_price = his[his['Stock Code'] == int(sell_code)]['Opening Price'].values
        money += sell_price * int(info['Corresponding number of stocks you sell'].values)


    # TODO
    s = s + pd.Timedelta(minutes=1)
    test_data_pre = test_data_pre.append({'ID': 1, 'Stock Code': 600000, 'Time': s,
                                          'Opening Price': 21.8, 'Highest Price': 21.9, 'Lowest Price': 21},
                                         ignore_index=True)
    test_data_pre = test_data_pre.append({'ID': 1, 'Stock Code': 600004, 'Time': s,
                                          'Opening Price': 23.8, 'Highest Price': 23.9, 'Lowest Price': 23},
                                         ignore_index=True)
    test_data_pre = test_data_pre.append({'ID': 1, 'Stock Code': 600005, 'Time': s,
                                          'Opening Price': 22.8, 'Highest Price': 22.9, 'Lowest Price': 22},
                                         ignore_index=True)
    b = copy.deepcopy(money)
    add_data = model(s, b, test_data_pre[test_data_pre['Time'] <= s], investment_data)
    investment_data = investment_data.append(add_data)

    info = investment_data[investment_data.Time == s]
    his = test_data_pre[test_data_pre.Time == s]
    bug_code = info['Stocks you buy'].values[0]
    if type(bug_code) == str:
        bug_price = his[his['Stock Code'] == int(bug_code)]['Opening Price'].values
        money -= bug_price * int(info['Corresponding number of stocks you buy'].values)

    sell_code = info['Stocks you sell'].values[0]
    if type(sell_code) == str:
        sell_price = his[his['Stock Code'] == int(sell_code)]['Opening Price'].values
        money += sell_price * int(info['Corresponding number of stocks you sell'].values)
    # TODO
    s = s + pd.Timedelta(minutes=1)
    test_data_pre = test_data_pre.append({'ID': 1, 'Stock Code': 600000, 'Time': s,
                                          'Opening Price': 25.8, 'Highest Price': 25.9, 'Lowest Price': 25},
                                         ignore_index=True)
    test_data_pre = test_data_pre.append({'ID': 1, 'Stock Code': 600004, 'Time': s,
                                          'Opening Price': 25.8, 'Highest Price': 25.9, 'Lowest Price': 25},
                                         ignore_index=True)
    test_data_pre = test_data_pre.append({'ID': 1, 'Stock Code': 600005, 'Time': s,
                                          'Opening Price': 25.8, 'Highest Price': 25.9, 'Lowest Price': 25},
                                         ignore_index=True)
    b = copy.deepcopy(money)
    add_data = model(s, b, test_data_pre[test_data_pre['Time'] <= s], investment_data)
    investment_data = investment_data.append(add_data)


    info = investment_data[investment_data.Time == s]
    his = test_data_pre[test_data_pre.Time == s]
    bug_code = info['Stocks you buy'].values[0]
    if type(bug_code) == str:
        bug_price = his[his['Stock Code'] == int(bug_code)]['Opening Price'].values
        money -= bug_price * int(info['Corresponding number of stocks you buy'].values)

    sell_code = info['Stocks you sell'].values[0]
    if type(sell_code) == str:
        sell_price = his[his['Stock Code'] == int(sell_code)]['Opening Price'].values
        money += sell_price * int(info['Corresponding number of stocks you sell'].values)

    # TODO
    s = s + pd.Timedelta(minutes=1)
    test_data_pre = test_data_pre.append({'ID': 1, 'Stock Code': 600000, 'Time': s,
                                          'Opening Price': 25.1, 'Highest Price': 25.2, 'Lowest Price': 25},
                                         ignore_index=True)
    b = copy.deepcopy(money)
    add_data = model(s, b, test_data_pre[test_data_pre['Time'] <= s], investment_data)
    investment_data = investment_data.append(add_data)

    info = investment_data[investment_data.Time == s]
    his = test_data_pre[test_data_pre.Time == s]
    bug_code = info['Stocks you buy'].values[0]
    if type(bug_code) == str:
        bug_price = his[his['Stock Code'] == int(bug_code)]['Opening Price'].values
        money -= bug_price * int(info['Corresponding number of stocks you buy'].values)

    sell_code = info['Stocks you sell'].values[0]
    if type(sell_code) == str:
        sell_price = his[his['Stock Code'] == int(sell_code)]['Opening Price'].values
        money += sell_price * int(info['Corresponding number of stocks you sell'].values)
    # TODO
    s = s + pd.Timedelta(minutes=1)
    test_data_pre = test_data_pre.append({'ID': 1, 'Stock Code': 600000, 'Time': s,
                                          'Opening Price': 25.8, 'Highest Price': 25.9, 'Lowest Price': 25},
                                         ignore_index=True)
    test_data_pre = test_data_pre.append({'ID': 1, 'Stock Code': 600004, 'Time': s,
                                          'Opening Price': 25.8, 'Highest Price': 25.9, 'Lowest Price': 25},
                                         ignore_index=True)
    test_data_pre = test_data_pre.append({'ID': 1, 'Stock Code': 600005, 'Time': s,
                                          'Opening Price': 25.8, 'Highest Price': 25.9, 'Lowest Price': 25},
                                         ignore_index=True)
    b = copy.deepcopy(money)
    add_data = model(s, b, test_data_pre[test_data_pre['Time'] <= s], investment_data)
    investment_data = investment_data.append(add_data)

    info = investment_data[investment_data.Time == s]
    his = test_data_pre[test_data_pre.Time == s]
    bug_code = info['Stocks you buy'].values[0]
    if type(bug_code) == str:
        bug_price = his[his['Stock Code'] == int(bug_code)]['Opening Price'].values
        money -= bug_price * int(info['Corresponding number of stocks you buy'].values)

    sell_code = info['Stocks you sell'].values[0]
    if type(sell_code) == str:
        sell_price = his[his['Stock Code'] == int(sell_code)]['Opening Price'].values
        money += sell_price * int(info['Corresponding number of stocks you sell'].values)
    # TODO
    s = s + pd.Timedelta(minutes=1)
    test_data_pre = test_data_pre.append({'ID': 1, 'Stock Code': 600000, 'Time': s,
                                          'Opening Price': 26.1, 'Highest Price': 26.2, 'Lowest Price': 26},
                                         ignore_index=True)
    test_data_pre = test_data_pre.append({'ID': 1, 'Stock Code': 600004, 'Time': s,
                                          'Opening Price': 26.1, 'Highest Price': 26.2, 'Lowest Price': 26},
                                         ignore_index=True)
    test_data_pre = test_data_pre.append({'ID': 1, 'Stock Code': 600005, 'Time': s,
                                          'Opening Price': 26.1, 'Highest Price': 26.2, 'Lowest Price': 26},
                                         ignore_index=True)
    b = copy.deepcopy(money)
    add_data = model(s, b, test_data_pre[test_data_pre['Time'] <= s], investment_data)
    investment_data = investment_data.append(add_data)

    info = investment_data[investment_data.Time == s]
    his = test_data_pre[test_data_pre.Time == s]
    bug_code = info['Stocks you buy'].values[0]
    if type(bug_code) == str:
        bug_price = his[his['Stock Code'] == int(bug_code)]['Opening Price'].values
        money -= bug_price * int(info['Corresponding number of stocks you buy'].values)

    sell_code = info['Stocks you sell'].values[0]
    if type(sell_code) == str:
        sell_price = his[his['Stock Code'] == int(sell_code)]['Opening Price'].values
        money += sell_price * int(info['Corresponding number of stocks you sell'].values)
    # TODO
    s = s + pd.Timedelta(minutes=1)
    test_data_pre = test_data_pre.append({'ID': 1, 'Stock Code': 600000, 'Time': s,
                                          'Opening Price': 26.1, 'Highest Price': 26.2, 'Lowest Price': 26},
                                         ignore_index=True)
    test_data_pre = test_data_pre.append({'ID': 1, 'Stock Code': 600004, 'Time': s,
                                          'Opening Price': 26.1, 'Highest Price': 26.2, 'Lowest Price': 26},
                                         ignore_index=True)
    test_data_pre = test_data_pre.append({'ID': 1, 'Stock Code': 600005, 'Time': s,
                                          'Opening Price': 26.1, 'Highest Price': 26.2, 'Lowest Price': 26},
                                         ignore_index=True)
    b = copy.deepcopy(money)
    add_data = model(s, b, test_data_pre[test_data_pre['Time'] <= s], investment_data)
    investment_data = investment_data.append(add_data)

    info = investment_data[investment_data.Time == s]
    his = test_data_pre[test_data_pre.Time == s]
    bug_code = info['Stocks you buy'].values[0]
    if type(bug_code) == str:
        bug_price = his[his['Stock Code'] == int(bug_code)]['Opening Price'].values
        money -= bug_price * int(info['Corresponding number of stocks you buy'].values)

    sell_code = info['Stocks you sell'].values[0]
    if type(sell_code) == str:
        sell_price = his[his['Stock Code'] == int(sell_code)]['Opening Price'].values
        money += sell_price * int(info['Corresponding number of stocks you sell'].values)
    # TODO
    s = s + pd.Timedelta(minutes=1)
    test_data_pre = test_data_pre.append({'ID': 1, 'Stock Code': 600005, 'Time': s,
                                          'Opening Price': 27.1, 'Highest Price': 27.2, 'Lowest Price': 27},
                                         ignore_index=True)
    b = copy.deepcopy(money)
    add_data = model(s, b, test_data_pre[test_data_pre['Time'] <= s], investment_data)
    investment_data = investment_data.append(add_data)

    s = s + pd.Timedelta(minutes=1)
    test_data_pre = test_data_pre.append({'ID': 1, 'Stock Code': 600000, 'Time': s,
                                          'Opening Price': 26.1, 'Highest Price': 26.2, 'Lowest Price': 26},
                                         ignore_index=True)
    test_data_pre = test_data_pre.append({'ID': 1, 'Stock Code': 600004, 'Time': s,
                                          'Opening Price': 26.1, 'Highest Price': 26.2, 'Lowest Price': 26},
                                         ignore_index=True)
    test_data_pre = test_data_pre.append({'ID': 1, 'Stock Code': 600005, 'Time': s,
                                          'Opening Price': 26.1, 'Highest Price': 26.2, 'Lowest Price': 26},
                                         ignore_index=True)
    b = copy.deepcopy(money)
    add_data = model(s, b, test_data_pre[test_data_pre['Time'] <= s], investment_data)
    investment_data = investment_data.append(add_data)
    print(add_data)
