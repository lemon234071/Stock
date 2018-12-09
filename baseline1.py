import pandas as pd
import lightgbm as lgb
from sklearn.preprocessing import LabelEncoder
import numpy as np
import os


def GetTrainData(path):
    # type = {'Closing Price':np.float32, '': np.int32}
    # df_train = pd.read_csv(path, dtype=type)
    df_train = pd.read_csv(path, nrows=200000)
    df_train.pop('ID')
    # l_code = df_train['Stock Code'].unique()
    df_valid = df_train.loc[df_train['Date'].str.startswith('2009-11', na=False)]
    li_valid = df_train.loc[df_train['Date'].str.startswith('2009-11', na=False)].index.tolist()
    df_train = df_train.drop(li_valid)
    return df_train, df_valid

def GetTestData(path):
    df_test = pd.read_csv(path)
    return df_test

def label_encoding(data):
    for feature in ['Date', 'Time']:
        try:
            data[feature] = LabelEncoder().fit_transform(data[feature].apply(int))
        except:
            data[feature] = LabelEncoder().fit_transform(data[feature])
    return data


if __name__ == '__main__':
    # Make sure the current directory is the parent directory of "data" !!!
    train, valid = GetTrainData('./data/train.csv')
    test = GetTestData('./data/test.csv')

    train = label_encoding(train)
    valid = label_encoding(valid)
    test = label_encoding(test)

    train.to_csv('./data/train_v1.csv', index=False)
    valid.to_csv('./data/valid_v1.csv', index=False)

    lgb_train = lgb.Dataset(train, train['Closing Price'])
    lgb_valid = lgb.Dataset(valid, valid['Closing Price'])

    lgb_params = {
        'boosting_type': 'gbdt',
        'application': 'regression',
        'metric': 'rmse',
        'num_leaves': 61,
        'max_depth': -1,
        'learning_rate': 0.01,
        'verbose': 1,
        'seed': 2018,
    }
    # LightGBM建模
    lgb_model = lgb.train(lgb_params, lgb_train, num_boost_round=100, verbose_eval=10,
                          valid_sets=lgb_valid, early_stopping_rounds=100)

    test['Closing Price'] = lgb_model.predict(test.iloc[:, 1:])
    test['Closing Price'] = test['Closing Price'].apply(lambda x: float('%.6f' % x))
    test.to_csv('./data/submission.csv', index=False)
    print("finished")
