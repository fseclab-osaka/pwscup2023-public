import pandas as pd
import random
import numpy as np

# parameter design
n = 10 ** 5 # number of lines
# H = 4 # highest numbr

# 公開データ読み込み
p_file = 'p.csv'
df_p_origin = pd.read_csv(p_file, header=None)
df_p = df_p_origin.copy()
# 整列データ読み込み
team_num = '10'

b_file = f'main-atk-public/b_{team_num}.csv'
df_b = pd.read_csv(b_file, header=None)

np_p = df_p_origin.values
np_b = df_b.values
np_b_public = df_b.iloc[:,:8].values

# 予備戦 0.9974	
b_usability = 0.8768
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
unique_ind_p = search_unique(np_p,np_p)
# unique_ind_b = search_unique(np_b,np_b)
unique_ind_b = search_unique(np_b_public,np_b_public)
len(unique_ind_p)-len(unique_ind_b)
rest_ind_b = []
rest_ind_p = []
pair_ind_b = []
pair_ind_p = []
same_ind_p = []
same_ind_b = []
same_num_b =[]
diff_ind_p = []
diff_ind_b = []
diff_num_b = []
one_ind_p = []
one_ind_b = []
dis_ind_p = []
np_b_ = np_b.copy()
for i in range(n):
    ind_p = list(np.where((np_p == np_p[i]).sum(axis=1) == 8)[0])
    n_p = len(ind_p)
    # print(np_p[i])
    # n_b = np.count_nonzero(np_b_public == np_p[i])
    ind_b = list(np.where((np_b_public == np_p[i]).sum(axis=1) == 8)[0])
    n_b = len(ind_b)
    # print(ind_b)
    # assert()
    n_b = len(ind_b)
    print(n_p,n_b)
    if n_b == 0:
        print('disappear')
        if n_p == 1:
            dis_ind_p.append(i)
        else:
            diff_ind_p.append(i)
            
    elif n_p == 1 and n_b == 1:
        one_ind_p.append(i)
        one_ind_b.append(ind_b[0])
    elif n_p == n_b:
        same_ind_p.append(i)
        same_ind_b.append(ind_b[0])
        same_num_b.append(len(ind_b))
    else:
        diff_ind_p.append(i)
        diff_ind_b.append(ind_b[0])
        diff_num_b.append(len(ind_b))

        
    # can = candidates(0,np_p[i],np_b_)
    # if len(can) != 0:
    #     pair_ind_p.append(i)
    #     pair_ind_p.append(can[0])
    # np_b_ = np.delete(np_b_,can[0])
print('one:',len(one_ind_p),len(same_ind_p),'diff:', len(diff_ind_p),len(diff_ind_b),'dis:',len(dis_ind_p),len(one_ind_p)+len(same_ind_p)+ len(diff_ind_p)+len(dis_ind_p))
print(same_ind_p[0],one_ind_p[0])
ind_ans = np.zeros(n, dtype = int)
df_ans = pd.DataFrame(np.zeros((n,10))).astype('int')
l = 0
for i in range(n):
    h = 2
    while True:
        can = candidates(h,np_p[i],np_b_public)
        if len(can) != 0:
            # print(i,h)
            ind_ans[i] = random.choice(can)
            l+=h
            break
        h+=1
    

for i in range(n):
    df_ans.iloc[i,:] = df_b.iloc[ind_ans[i],8:]

print(l,num_change)
    

# データ書き込み
df_ans.to_csv(f'f_{team_num}_05.csv',header=None,index=False)