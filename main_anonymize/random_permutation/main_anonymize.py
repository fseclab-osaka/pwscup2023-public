import pandas as pd
import numpy as np
import random
import sys

cat_list = [0,1,2,3,4,5,6,7,8,9]
weights_list = [19,17,15,13,11,9,7,5,3,1]

## 一意に定まる行の特定(ランダム化したデタが＊とした場合) およそ3分
# 一意に定まる行番号
def search_unique(p_data_origin, p_data_, k):
    unique_ind = []
    for i in range(len(p_data_origin)):
        if np.count_nonzero((p_data_origin == p_data_[i]).sum(axis=1) == k) == 1:
            unique_ind.append(i)
    print('num of unique: ',len(unique_ind))
    return unique_ind

def convert_random(record, record_, rand_ind_list, k):
    # rand_ind_list に含まれる列番号からランダムにkこ選び、
    # record の列を加工する
    rand_ind = random.sample(rand_ind_list,k=k)
    rand_cat = random.choices(cat_list, weights=weights_list, k=k)
    while record[rand_ind[0]] == rand_cat[0]:
        rand_cat = random.choices(cat_list, weights=weights_list, k=k)
    record[rand_ind] = rand_cat
    record_[rand_ind] = [-1] * k

def anonymize(filename):
    # データ読み込み
    # o.csv = 公開データと秘密データ結合した未加工データ
    o_file = 'o.csv'
    o_data = pd.read_csv(o_file, header=None)

    n = len(o_data.values)
    p_num = 8
    r_num = 10
    p_data = o_data.iloc[:,0:p_num].values
    r_data = o_data.iloc[:,p_num:].values

    p_data_ = p_data.copy()
    p_data_origin = p_data.copy()

    # Step1
    for i in range(n):
        rand_ind_list = [1,2,3,4,5,6,7]
        convert_random(p_data[i], p_data_[i], rand_ind_list, k=1)

    # Step2
    unique_ind = search_unique(p_data_origin, p_data_, k=7)
    for i in unique_ind:
        rand_ind_list = []
        for j in range(p_num):
            if (p_data_origin[i] == p_data[i])[j] == True:
                rand_ind_list.append(j)
        convert_random(p_data[i], p_data_[i], rand_ind_list, k=1)

    #Step3
    unique_ind = search_unique(p_data_origin, p_data_, k=6)
    for i in unique_ind:
        rand_ind_list = []
        for j in range(p_num):
            if (p_data_origin[i] == p_data[i])[j] == True:
                rand_ind_list.append(j)
        convert_random(p_data[i], p_data_[i], rand_ind_list, k=1)

    usability = 1- sum((p_data_origin!=p_data).sum(axis=1))/((p_num+r_num)*n)
    print('usability is ',usability)

    # 公開データと秘密データ結合
    a_data = np.concatenate([p_data,r_data],axis=1)

    # 出力
    a_file = filename
    np.savetxt(a_file, a_data, delimiter=',', fmt='%d')

if __name__ == '__main__':
    # 複数回実行し、有用性が高いものを選ぶ
    # 引数の文字列を保存するファイル名の最後に加える
    args = sys.argv 
    if len(args) < 2:
        filename_end = ''
    else: filename_end  = args[1]
    # 出力ファイル名
    filename = 'a_A_' + filename_end + '.csv'
    anonymize(filename)