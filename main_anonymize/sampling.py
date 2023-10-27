import pandas as pd
import random


def eval_utility():
    # 整列前加工データ読み込み
    df_a = pd.read_csv('a.csv', header=None)
    
    # 加工前データ
    df_o = pd.read_csv('o.csv', header=None)

    wrong_elements = (df_a != df_o).sum().sum()
    utility_eval = 1 - wrong_elements / (df_o.shape[0] * df_o.shape[1])
    print(f"utility_eval: {utility_eval:.5f}") # 有用性評価値を出力


def main(num_A):
    df_a_A = pd.read_csv('a_A.csv', sep=',', header=None)
    df_a_B = pd.read_csv('a_B.csv', sep=',', header=None)

    index_A = sorted(random.sample(range(df_a_A.shape[0]), num_A))
    index_B = list(set(range(df_a_A.shape[0])) - set(index_A))

    df_a_A_sampling = df_a_A.iloc[index_A,:]
    df_a_B_sampling = df_a_B.iloc[index_B,:]

    df_a = pd.concat([df_a_A_sampling, df_a_B_sampling], axis=0).sort_index(axis='index')

    df_a.to_csv('a.csv', header=False, index=False)

    eval_utility()


if __name__ == '__main__':
    '''
    mode = 0: sampling from a_A.csv and a_B.csv and eval_utility
    mode = 1: eval_utility only
    '''
    mode = 0

    if mode == 0:
        num_A = 50000 # Aのサンプリング数
        main(num_A)
    elif mode == 1:
        eval_utility()
    else:
        print("mode is not 0 or 1")