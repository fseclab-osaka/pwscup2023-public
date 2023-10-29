import pandas as pd
import numpy as np
import random

def hamm_dis(p_record, b_numpy):    
    distances = (b_numpy != p_record).sum(axis=1)
    return distances

# ハミング距離がhのものをリストで返す
def candidates(h,p_record,np_b):
    dis = hamm_dis(p_record, np_b)
    return list(np.where(dis == h)[0])

n = 10**5
df_ano = pd.read_csv(f"b_data/b_14.csv",header=None)
df_p = pd.read_csv(f"p_data/p.csv",header=None)

df_ans = pd.concat([df_p,df_ano],axis=1).iloc[:,:18]

# int型で全部やるためにstarを10にする
df_ano = df_ano.replace("*",10).astype(int)

# 分布チェック
for i in range(11):
    df_bool = (df_ano == i) 
    print(f"{i}, {df_bool.sum(axis=0).to_list()}")


df_ano["p*"] = (df_ano[[0,1,2,3,4,5,6,7]]==10).sum(axis=1)
df_ano["s*"] = (df_ano[[8,9,10,11,12,13,14,15,16,17]]==10).sum(axis=1)

df_p["star"] = (df_p[[1,2,3,4,5,6,7]]==8).sum(axis=1)
df_p["star"] += (df_p[[1,2,3,4,5,6,7]]==9).sum(axis=1)


np_b = df_ano.iloc[:,1:8].values
np_public = df_p.iloc[:,1:8].values
for i in range(n):
    h = df_p.iat[i,8]
    cand_list_tmp = candidates(h,np_public[i],np_b)
    cand_list = random.sample(cand_list_tmp, len(cand_list_tmp))
    for index in cand_list:
        if df_ano.iat[index,18] == h:
            break
    df_ans.iloc[i,8:] = df_ano.iloc[[index]].iloc[:,8:18].values.tolist()[0]
    if i%100 == 0:
        print(i)


df_ans = df_ans.replace(10,8)

df_ans.to_csv("answer/f_14_05.csv",header=False, index=False)



