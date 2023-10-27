import pandas as pd
import numpy as np
from tqdm import tqdm
import collections
import matplotlib.pyplot as plt
plt.style.use('ggplot')


def hamm_dis(record, np_records):    
    ''' 
    ハミング距離計算する
    '''
    distances = (np_records != record).sum(axis=1)
    return distances


def candidates(h, record, np_records):
    '''
    ハミング距離がhのもののインデックスをリストで返す
    record(一つのレコード)とnp_records(レコードの集まり)とのハミング距離を計算し,
    np_records 内のハミング距離がh のレコードのインデックスを返す
    '''
    dis = hamm_dis(record, np_records)
    return list(np.where(dis == h)[0])


def main(h_min, team_id):
    # ファイルのパス
    path_p = './p.csv'
    path_b = f'./main-atk-public/b_{team_id}.csv'

    # 公開データ読み込み
    df_ori_p = pd.read_csv(path_p, sep=',', header=None)
    np_ori_p = df_ori_p.values

    # 整列加工データ読み込み
    df_b = pd.read_csv(path_b, header=None).replace('*', 10).astype(int) # "*"は10に置換
    df_b_p = df_b.iloc[:,:np_ori_p.shape[1]] # 整列加工データ公開部
    np_b_p = df_b_p.values

    can_index = [] # ハミング距離最小のインデックスを格納（複数ある場合はランダム）
    ham = [] # ハミング距離を格納
    for i in tqdm(range(np_ori_p.shape[0])):
        h = h_min
        while True:
            can = candidates(h, np_ori_p[i], np_b_p)
            if len(can) != 0:
                idx = np.random.randint(0, len(can)) 
                can_index.append(can[idx])
                ham.append(h)
                break
            h += 1
    
    c = collections.Counter(ham)
    print(c) # ハミング距離の出現回数を出力

    for i in range(np_ori_p.shape[1]+1):
        if i not in c:
            c[i] = 0
    c_sorted = sorted(c.items())
    c_sorted = dict((x, y) for x, y in c_sorted)
    plt.bar(list(c_sorted.keys()), list(c_sorted.values()))
    plt.title(f"Team {team_id}")
    plt.savefig(f'./hamming_distance_{team_id}.png')
    plt.close()

    df_b_r = df_b.iloc[:,np_ori_p.shape[1]:] # 整列加工データ秘密部
    np_b_r = df_b_r.values

    ans = [] # 秘密推定データを格納
    for i in tqdm(range(len(can_index))):
        ans.append(np_b_r[can_index[i]])
    np_ans = np.array(ans)
    df_ans = pd.DataFrame(np_ans)
    df_ans.to_csv(f'./f_{team_id}_05.csv', index=False, header=False) # 秘密推定データを出力


if __name__ == '__main__':
    team_list = ['02', '07', '11', '13', '15']
    h_min_list = [2, 0, 0, 1, 0]
    for i in range(len(team_list)):
        main(h_min_list[i], team_list[i])
        