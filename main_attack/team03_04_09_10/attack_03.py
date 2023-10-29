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
b_num = '03'

b_file = f'main-atk-public/b_{b_num}.csv'
df_b = pd.read_csv(b_file, header=None)

np_p = df_p_origin.values
np_b = df_b.values
np_b_public = df_b.iloc[:,:8].values

#  整列データ公開部分
df_b_public = df_b.iloc[:,:8]
# df_b_public.to_csv(f'b_{b_num}_public.csv',header=None,index=False)

# 予備戦　0.9053
b_usability = 0.7802
num_change = 18*n*(1-b_usability)
num_change_ = 0
print(f'usability:{b_usability}, average_change/row :',18*(1-b_usability), f'num_change:{num_change}')
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
# 公開データで属性値がH以上(3~9)を0に置換
for i in range(n):
    ind_dup_high = list(np.where(df_p_origin.iloc[i]>H))[0]
    if(len(ind_dup_high) > 0): 
        df_p.iloc[i,ind_dup_high] = [0 for j in range(len(ind_dup_high))]
        num_change_ += len(ind_dup_high)
## ユニークな行のインデックス求める
np_p2b = df_p.values
unique_ind = search_unique(np_p2b, np_p2b)
# 残り加工数
print(f'num of rest change:{num_change-num_change_}')
## 公開データの属性値3-9 を0に加工してできるデータと整列データを比べて、個数が5個以上一致する列は最短距離0でハミングマッチ
# 0置換して個数が一致するものはとりあえず確定
# ただし、1行のみ場合は罠とみなす。

ind_b_first = []
bf_bool = df_b_public.duplicated()
for i in range(n):
    if not bf_bool[i]:
        # print(df_b_public.iloc[i,:])
        ind_b_first.append(i)
np_p2b_unique = df_p.iloc[unique_ind,:].values
ind_same = []
num_same = []
ind_diff = []
num_diff = []
ind_one = []
for i in range(len(ind_b_first)):
    ind = ind_b_first[i]
    if i < len(ind_b_first)-1:
        num_dup = ind_b_first[i+1] - ind_b_first[i]
    else: num_dup = n - ind_b_first[i]
    if num_dup == 1:
        ind_one.append(ind)
    elif num_dup > 4 and np.count_nonzero((np_p2b == np_b_public[ind]).sum(axis=1) == 8) == num_dup:
        if np.count_nonzero((np_p2b_unique == np_b_public[ind]).sum(axis=1) == 8) > 0 :
            print('unique!!!')
            ind_diff.append(ind)
            ind_diff.append(num_dup)
        else:
            ind_same.append(ind)
            num_same.append(num_dup)
    else:
        ind_diff.append(ind)
        num_diff.append(num_dup)

print(f'num of same: {len(ind_same)},({sum(num_same)})')
print(f'num of diff: {len(ind_diff)},({sum(num_diff)})')
print(f'num of one: {len(ind_one)}')

# same 
np_ans = np.zeros((n,10))
df_ans = pd.DataFrame(np_ans).astype('int')
for i in range(len(ind_same)):
    ind = ind_same[i]
    num = num_same[i]
    ind_list = list(np.where((np_b_public[ind] == np_p2b).sum(axis=1) == 8)[0])
    rand_list = random.sample(range(ind,ind+num),num)
    assert(len(ind_list) == len(rand_list))
    for j in range(len(ind_list)):
        df_ans.iloc[ind_list[j], 0:] = df_b.iloc[rand_list[j],8:]
## 残りの行は最短距離1以上でハミングマッチ
rest_list_p_ = list(np.where(df_ans.values.sum(axis=1) == 0))[0]
import copy
# rest_list_b_ = ind_diff + ind_one
print(len(ind_one))
rest_list_b_ = copy.deepcopy(ind_one)
for i in range(len(ind_diff)):
    # print([ind_diff[i]]*num_diff[i])
    for j in range(num_diff[i]):
        rest_list_b_ += [ind_diff[i]+j]
print(len(rest_list_b_))

rest_list_p_ = list(np.where(df_ans.values.sum(axis=1) == 0))[0]
rest_df_b = df_b.iloc[rest_list_b_,:]
rest_np_b = rest_df_b.values
rest_df_p = df_p.iloc[rest_list_p_,:]
rest_np_p = rest_df_p.values
rest_df_b = df_b.iloc[rest_list_b_,:]
rest_np_b = rest_df_b.values
rest_df_p = df_p.iloc[rest_list_p_,:]
rest_np_p = rest_df_p.values
# print(rest_np_b[0,:8])
rest_list_p_copy = copy.deepcopy(rest_list_p_)
k = 0
rest_np_p = rest_df_p.values
for i in range(len(rest_np_p)):
    h = 1
    if rest_list_p_copy[i] in unique_ind:
        h = 1
        # print('unique!')

    while True:
        can = candidates(h, rest_np_p[i],rest_np_b[:,:8])
        if len(can) != 0:
            print(i, h)
            k+= h
            break
        h+=1
    i_ = random.choice(can)
    df_ans.iloc[rest_list_p_[i],:] = df_b.iloc[rest_list_b_[i_],8:]
    # rest_np_b = np.delete(rest_np_b, i_,0)
    # rest_list_b_ = np.delete(rest_list_b_, i_)

# print(k,len(rest_np_b),len(rest_np_p))
print(k,len(rest_np_b))
print(rest_np_p)
# print(rest_np_b)
print(list(np.where(df_ans.values.sum(axis=1) == 0))[0])


# データ書き込み
df_ans.to_csv(f'f_03_05.csv',header=None,index=False)