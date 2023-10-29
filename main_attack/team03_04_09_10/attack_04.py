import pandas as pd
import random
import numpy as np

# parameter design
n = 10 ** 5 # number of lines
H = 4 # highest number

# 公開データ読み込み
p_file = 'p.csv'
df_p_origin = pd.read_csv(p_file, header=None)
df_p = df_p_origin.copy()
# 整列データ読み込み
team_num = '04'

b_file = f'main-atk-public/b_{team_num}.csv'
df_b = pd.read_csv(b_file, header=None)

np_p = df_p_origin.values
np_b = df_b.values
np_b_public = df_b.iloc[:,:8].values
#  整列データ公開部分
df_b_public = df_b.iloc[:,:8]
# df_b_public.to_csv(f'b_{team_num}_public.csv',header=None,index=False)
np_b_public = df_b_public.values
# 予備戦 0.8460
b_usability = 0.8445
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

## *(astarisc)　を-1 に変換
def convert_ast(df_b):
    for i in range(n):
        ind_convert = list(np.where(df_b.iloc[i] == '*'))[0]
        if(len(ind_convert) > 0): 
            # 公開データ内で属性値が*を-1に置換
            df_b.iloc[i,ind_convert] = [-1 for j in range(len(ind_convert))]

#＃
def candidates(h, record, np_records):
    '''
    ハミング距離がhのもののインデックスをリストで返す
    record(一つのレコード)とnp_records(レコードの集まり)とのハミング距離を計算し,
    np_records 内のハミング距離がh のレコードのインデックスを返す
    '''
    dis = hamm_dis(record, np_records)
    return list(np.where(dis == h)[0])
# 公開データで属性値がH以上(5~9)を0に置換
num_change_ = 0
num_change_list = [0,0,0,0,0,0,0,0,0]
ind_only = []
ind_one = []
ind_two = []
for i in range(n):
    ind_dup_high = list(np.where(df_p_origin.iloc[i]>H)[0])
    # print(ind_dup_high)
    if(len(ind_dup_high) > 0): 
        df_p.iloc[i,ind_dup_high] = [-1 for j in range(len(ind_dup_high))]
        num_change_ += len(ind_dup_high)
        num_change_list[len(ind_dup_high)] += 1
        if len(ind_dup_high) == 1:
            ind_one.append(i)
        elif len(ind_dup_high) == 2:
            ind_two.append(i)
    else:
        ind_only.append(i)
np_p2b = df_p.values
# 各行の属性数5~9の数
import matplotlib.pyplot as plt

# ヒストグラムを描画する
print(num_change_list)
# plt.xlabel('各行に含まれる5-9の数')
# plt.ylabel('行数')
plt.plot([0,1,2,3,4,5,6,7,8],num_change_list);
## 変換後でユニークな行のインデックス求める

unique_ind = search_unique(np_p2b, np_p2b)
# print(df_p.iloc[0,:])
print(f'num_change:{num_change}, num_cahnge_:{num_change_},:{num_change - num_change_}')
print(f'only 0-4 : {n-sum(num_change_list)}')
print(ind_only)
## 変更数の計算
# 変更数が0のものは3属性置換したとして、変更数1のものはプラス1属性置換したとして
print(f'総変換数:{num_change}, 5-9の数: {num_change_}, 差{num_change-num_change_}')
num_changed = num_change-num_change_ 
print(f'変換0の行に対して2つ変換:{num_changed-len(ind_only)*2}, 3つ変換:{num_changed-len(ind_only)*3}, 5つ変換: {num_changed-len(ind_only)*5}, 6つ変換:{num_changed-len(ind_only)*6}, 7つ変:; {num_changed-len(ind_only)*7}, 8つ変換:{num_changed-len(ind_only)*8}')
print(f'変換1つの行に対して1つ変換:{num_change-num_change_-len(ind_only)*3-num_change_list[1]*1}, 2つ変換:{num_change-num_change_-len(ind_only)*3-num_change_list[1]*2}')
df_only = df_p_origin.iloc[ind_only,:]
weights_list = [19,17,15,13,11]
df_tmp = df_only.copy()
K = 5
for i in range(len(ind_only)):
    rand_ind = random.sample([0,1,2,3,4,5,6,7],k =K)
    # print(rand_ind)
    df_tmp.iloc[i,rand_ind] = random.choices([0,1,2,3,4],weights=weights_list,k=K)
    # print(df_only.iloc[i,:],df_tmp.iloc[i,:])
    # assert()
print(np.count_nonzero(df_only.values != df_tmp.values),len(ind_only)*K)
print(num_changed - np.count_nonzero(df_only.values != df_tmp.values))
num_changed_ = num_changed - np.count_nonzero(df_only.values != df_tmp.values)

df_one = df_p_origin.iloc[ind_one,:]
weights_list = [19,17,15,13,11]
df_tmp = df_one.copy()
K = 2
for i in range(len(ind_one)):
    # j = np.where(np_p2b[ind_one[i]] == -1)[0]
    # print(j)
    rand_list = [0,1,2,3,4,5,6,7]
    # rand_list.pop(j[0])
    rand_ind = random.sample(rand_list, k = K)
    df_tmp.iloc[i,rand_ind] =  random.choices([0,1,2,3,4],weights=weights_list,k=K)
    
print(np.count_nonzero(df_one.values != df_tmp.values),len(ind_one)*K)
print(num_changed_ - np.count_nonzero(df_one.values != df_tmp.values))
ind_ans = np.zeros(n, dtype = int)
df_ans = pd.DataFrame(np.zeros((n,10))).astype('int')
# df_one = df_p.iloc[ind_one,:]
# np_one = df_one.values
l = 0
ll = 0
for i in range(n):
    if i%10000 == 0:print(i)
    num_H = np.count_nonzero(np_p[i] > H)
    if num_H == 0:
        can = candidates(6,np_p[i], np_p2b)
    else:
        h = num_H
        if h == 1: h+=1
        can = candidates(h,np_p[i], np_p2b)
        # print(h,np_p2b[i])
        # print(len(can))
        # assert()
    if len(can) != 0:
        ind_ans[i] = random.choice(can)
    else: 
        # print(f'none candidates!! num_H:{num_H},index[{i}],: {np_p[i]}')
        can = candidates(h+1,np_p[i], np_p2b)
        l+=1
        if len(can) != 0:
            ind_ans[i] = random.choice(can)
        else :
            ll+=1
            print(f'none candidates!! num_H:{num_H},index[{i}],: {np_p[i]}')
print(l,ll)
print(np.where(ind_ans == 0))
print(len(list(np.where(ind_ans == 0)[0])))
for i in range(n):
    df_ans.iloc[i,:] = df_b.iloc[ind_ans[i],8:]
    

# データ書き込み
df_ans.to_csv(f'f_{team_num}_05.csv',header=None,index=False)