import pandas as pd
import random
import numpy as np

# parameter design
n = 10 ** 5 # number of lines
H = 2 # highest number

# 公開データ読み込み
p_file = 'p.csv'
df_p_origin = pd.read_csv(p_file, header=None)
df_p = df_p_origin.copy()
# 整列データ読み込み
team_num = '09'

b_file = f'main-atk-public/b_{team_num}.csv'
df_b = pd.read_csv(b_file, header=None)

np_p = df_p_origin.values
np_b = df_b.values
np_b_public = df_b.iloc[:,:8].values

b_usability = 0.7109
num_change = 18*n*(1-b_usability)
num_change_ = 0
print(f'usability:{b_usability}, average_change/row :',18*(1-b_usability), f'num_change:{num_change}')
#  整列データ公開部分
df_b_public = df_b.iloc[:,:8]
df_b_public.to_csv(f'b_{team_num}_public.csv',header=None,index=False)
np_b_public = df_b_public.values
## ハミング距離計算 レコード対レコード群
def hamm_dis(b_record, p_numpy):
    distances = (p_numpy != b_record).sum(axis=1)
    return distances

## 一意に定まる行の特定(ランダム化したデタが＊とした場合) およそ3分
# 一意に定まる行番号
def search_unique(np_data_, np_data):
    k = len(np_data[0])
    unique_ind = []
    for i in range(n):
        # print(np.count_nonzero((p_data == p_data_[i]).sum(axis=1) == k))
        # if i ==10: assert()
        if np.count_nonzero((np_data == np_data_[i]).sum(axis=1) == k) == 1:
            unique_ind.append(i)
        # if np.count_nonzero((p_data == p_data_[i]).sum(axis=1) == 1):
    print('num of unique: ',len(unique_ind))
    return unique_ind


def convert_ast(df_b):
    for i in range(n):
        ind_convert = list(np.where(df_b.iloc[i] == '*'))[0]
        if(len(ind_convert) > 0): 
            # 公開データ内で属性値が*を-1に置換
            df_b.iloc[i,ind_convert] = [-1 for j in range(len(ind_convert))]

def candidates(h, record, np_records):
    '''
    ハミング距離がhのもののインデックスをリストで返す
    record(一つのレコード)とnp_records(レコードの集まり)とのハミング距離を計算し,
    np_records 内のハミング距離がh のレコードのインデックスを返す
    '''
    dis = hamm_dis(record, np_records)
    return list(np.where(dis == h)[0])
ind_ans = np.zeros(n, dtype = int)
df_ans = pd.DataFrame(np.zeros((n,10))).astype('int')
l = 0
for i in range(n):
    h = 2
    while True:
        can = candidates(h,np_p[i],np_b_public)
        if len(can) != 0:
            print(i,h,len(can))
            ind_ans[i] = random.choice(can)
            l+=h
            break
        h+=1
    

for i in range(n):
    df_ans.iloc[i,:] = df_b.iloc[ind_ans[i],8:]

print(l,num_change)

# データ書き込み
df_ans.to_csv(f'f_{team_num}_05.csv',header=None,index=False)
ind_b_first = []
bf_bool = df_b_public.duplicated()
for i in range(n):
    if not bf_bool[i]:
        # print(df_b_public.iloc[i,:])
        ind_b_first.append(i)
ind_same = []
num_same = []
ind_diff = []
num_diff = []

for i in range(len(ind_b_first)):
    ind = ind_b_first[i]
    if i < len(ind_b_first)-1:
        num_dup = ind_b_first[i+1] - ind_b_first[i]
    else: num_dup = n - ind_b_first[i]
    if num_dup%4 == 0:
        ind_same.append(ind)
        num_same.append(num_dup)
    else:
        ind_diff.append(ind)
        num_diff.append(num_dup)

print(f'num of same: {len(ind_same)},({sum(num_same)})')
print(f'num of diff: {len(ind_diff)},({sum(num_diff)})')