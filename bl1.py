import pandas as pd
import lightgbm as lgb
from sklearn.preprocessing import LabelEncoder
import numpy as np
import os


def GetData(path):
    # type = {'Closing Price':np.float32, '': np.int32}
    # df_train = pd.read_csv(path, dtype=type)
    df_train = pd.read_csv(path+'/train.csv')
    df_test = pd.read_csv(path+'/test.csv')
    df_train.pop('ID')
    df_test.pop('ID')
    li_valid = df_train.loc[df_train['Date'].str.startswith('2009-11', na=False)].index.tolist()
    df_valid = df_train.loc[df_train['Date'].str.startswith('2009-11', na=False)]
    df_train = df_train.drop(li_valid)
    df_train['label'] = 1
    df_valid['label'] = 0
    df_test['label'] = -1
    data = pd.concat([df_train, df_valid, df_test])
    data = label_encoding(data)
    df_train = data[data.label == 1]
    df_train_y = df_train.pop('Closing Price')
    df_valid = data[data.label == 0]
    df_valid_y = df_valid.pop('Closing Price')
    df_test=data[data.label==-1]
    del df_train['label'], df_valid['label'], df_test['label']
    # l_code = df_train['Stock Code'].unique()
    return df_train, df_train_y, df_valid, df_valid_y ,df_test

def label_encoding(data):
    for feature in ['Date', 'Time']:
        try:
            data[feature] = LabelEncoder().fit_transform(data[feature].apply(int))
        except:
            data[feature] = LabelEncoder().fit_transform(data[feature])
    return data


if __name__ == '__main__':
    # Make sure the current directory is the parent directory of "data" !!!
    train, train_y, valid, valid_y, test = GetData('./data')
    train.to_csv('./data/train_v1.csv', index=False)
    valid.to_csv('./data/valid_v1.csv', index=False)

    lgb_train = lgb.Dataset(train, train_y)
    lgb_valid = lgb.Dataset(valid, valid_y)

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
    # LightGBM
    lgb_model = lgb.train(lgb_params, lgb_train, num_boost_round=10000, verbose_eval=10,
                          valid_sets=lgb_valid, early_stopping_rounds=100)

    test['Closing Price'] = lgb_model.predict(test.iloc[:, 1:])
    test['Closing Price'] = test['Closing Price'].apply(lambda x: float('%.6f' % x))
    test.to_csv('./data/submission.csv', index=False)
    print 'finished'
