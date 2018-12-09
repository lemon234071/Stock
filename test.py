import pandas as pd

filename = './data/train.csv'
#count = len(open(filename).readlines())
# 55500855
#df = pd.read_csv(filename, skiprows=range(0, 55500855-200000), header=0)
#train = pd.read_csv('./data/train.csv', tail=1000)
# train = pd.read_csv('./data/train.csv', nrows=100000)
# test = pd.read_csv('./data/test.csv', nrows=10000)
# df_train = pd.read_csv('./data/train.csv', header=0, iterator=True)
# tail = df_train.get_chunk(1000)
# df_train = pd.read_csv(filename, nrows=6000)
# df_train.pop('ID')
# # l_code = df_train['Stock Code'].unique()
# # df_valid = df_train.loc[df_train['Date'].str.startswith('2009-11', na=False)]
# li_valid = df_train.loc[df_train['Date'].str.startswith('2008-02', na=False)].index.tolist()
# # li_valid = df_train[(df_train.Date.str.startwith('2009-11', na=False))].index.tolist()
# df_valid = df_train.drop(li_valid)
test = pd.read_csv('./data/train.csv', nrows=120000)
print("ok")