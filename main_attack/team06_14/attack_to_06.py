import pandas as pd
import numpy as np

# 読み込み
df_ano = pd.read_csv(f"b_data/b_06.csv",header=None)
df_p = pd.read_csv(f"p_data/p.csv",header=None)

# (7,5,3)属性の組み合わせで1000通りのindexを作成
df_ano["t"] = 100*df_ano[7] + 10*df_ano[5] + df_ano[3]

final_list = []

# 1000通りのindexごとに秘密データの頻度を集計
for i in range(1000):
    df_ans = df_ano[df_ano["t"]==i]
    max_list = []
    for j in range(10):
        ans_list = [0]*11
        for k in range(len(df_ans)):
            if df_ans.iat[k,j+8] == "*":
                ans_list[10] += 1
            else:
                ans_list[int(df_ans.iat[k,j+8])] += 1
        max_list.append(np.argmax(np.array(ans_list)))

    for j in range(len(max_list)):
        if max_list[j] == 10:
            max_list[j] = "*"

    final_list.append(max_list)
    if i % 100 == 0:
        print(i)

col = [8,9,10,11,12,13,14,15,16,17]
df_max = pd.DataFrame(np.zeros((10**5,10)),columns=col)
print(df_max)

for i in range(len(df_p)):
    df_max.iloc[i,:] = final_list[100*df_p.iat[i,7] + 10*df_p.iat[i,5] + df_p.iat[i,3]]
    if i % 100 == 0:
        # 進行確認
        print(i)

df_merged = pd.concat([df_p, df_max],axis=1).astype('int')

print(df_merged)

# 書き出し
df_merged.to_csv(f"answer/f_06_05.csv", header=False, index=False)

