import pandas as pd
import random
import sys

args = sys.argv
if len(args) < 2:
    filename_end = ''
else: filename_end = args[1]

n = 10 **5
# 読み込み
# 公開データ
p_file = 'p.csv'
p_data_origin = pd.read_csv(p_file, header=None)

# 秘密データ
s_file = 'r.csv'
s_data = pd.read_csv(s_file, header=None)

## 公開データの頻度調査 
# freq_p = [0 for i in range(10)]
# for i in range(6):
#     for j in range(10):
#         freq_p[j] += p_data[i].value_counts().iloc[j]
# print(freq_p/sum(freq_p))
# [0.190785   0.16952667 0.15006    0.13005333 0.10964167 0.089795
# 0.07025    0.04971333 0.02988833 0.01028667]
# -> weights_list
##

# カテゴリ候補数（各属性10通りなので共通）
cat_list = [0,1,2,3,4,5,6,7,8,9]
weights_list = [19,17,15,13,11,9,7,5,3,1]
# 書き換え数
K = 1

p_data = p_data_origin.copy()

# 一意に決まるか探索用（データを＊に変換した場合）
p_data_ = p_data_origin.copy()

## およそ 15秒
for i in range(len(p_data)):
    # 先頭列を同じ頻度で変更
    rand_cat_head = random.choices(cat_list, weights=weights_list, k=1)
    while p_data.iloc[i,0] == rand_cat_head[0]: # 確実に置換
        rand_cat_head = random.choices(cat_list, weights=weights_list, k=1)
    p_data.iloc[i,0] = rand_cat_head[0]
    p_data_.iloc[i,0] = -1

    # 先頭以外からランダムに1つを置き換える
    rand_ind = random.sample([1,2,3,4,5],k=K)
    rand_cat = random.choices(cat_list, weights=weights_list, k=K)
    while p_data.iloc[i,rand_ind[0]] == rand_cat[0] :
        rand_cat = random.choices(cat_list, weights=weights_list, k=K)
    p_data.iloc[i,rand_ind] = rand_cat
    p_data_.iloc[i,rand_ind] = [-1]
    # ペース確認用
    # print(i)

## 一意に定まる行の特定(ランダム化したデタが＊とした場合) およそ3分
# 一意に定まる行番号
unique_ind = []
for i in range(n):
    # ペース確認用
    if (i % 10000 == 0): print('uni ',i)
     # 乱数化したデータとオリジナルをひき、ランダム化していない列3ヶ所がすべて一致する行データの数が1つ
    if (p_data_origin == p_data_.iloc[i]).sum(axis=1).value_counts()[4] == 1:
        unique_ind.append(i)
print('num of unique: ',len(unique_ind))

##

# 一意に定まった行データに乱数追加
for i in unique_ind:
    rand_ind_list = []
    for j in range(6):
        if (p_data_origin.iloc[i] == p_data.iloc[i])[j] == True:
            rand_ind_list.append(j)

    rand_ind = random.sample(rand_ind_list,k= 1)
    rand_cat = random.choices(cat_list, weights=weights_list, k=1)
    while p_data.iloc[i,rand_ind[0]] == rand_cat[0]:
        rand_cat = random.choices(cat_list, weights=weights_list, k=1)
    p_data.iloc[i,rand_ind] = rand_cat
    p_data_.iloc[i,rand_ind] = [-1]

unique_ind = []
for i in range(n):
    # ペース確認用
    if (i % 10000 == 0): print('uni ',i)
     # 乱数化したデータとオリジナルをひき、ランダム化していない列3ヶ所がすべて一致する行データの数が1つ
    if (p_data_origin == p_data_.iloc[i]).sum(axis=1).value_counts()[3] == 1:
        unique_ind.append(i)
print('num of unique: ',len(unique_ind))

# 一意に定まった行データに乱数追加
for i in unique_ind:
    rand_ind_list = []
    for j in range(6):
        if (p_data_origin.iloc[i] == p_data.iloc[i])[j] == True:
            rand_ind_list.append(j)

    rand_ind = random.sample(rand_ind_list,k= 1)
    rand_cat = random.choices(cat_list, weights=weights_list, k=1)
    while p_data.iloc[i,rand_ind[0]] == rand_cat[0]:
        rand_cat = random.choices(cat_list, weights=weights_list, k=1)
    p_data.iloc[i,rand_ind] = rand_cat
    p_data_.iloc[i,rand_ind] = [-1]


print('usability is ',1- sum((p_data_origin!=p_data).sum(axis=1))/(16*n))
# 公開データと秘密データ結合
a_data = pd.concat([p_data,s_data],axis=1)

# 出力
a_file = 'out_a_uni_'+ filename_end +'.csv'
a_data.to_csv(a_file,header=None,index=False)