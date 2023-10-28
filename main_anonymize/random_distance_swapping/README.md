# Random Distance Swapping Method

## Algorithm

```
def anonymize(p.csv)->anonymized_p.csv
    p.csvの各行をハミング距離空間上の点とみなす
    chosen_list = [] # すでにswapされた点のリスト
    swap_map_table = [] # swapの対応表
    各点sについて, s \notin chosen_list なら
        1. distance = randInt(9) # [0, 9) から1つrandomにえらぶ
        2. もしBall(s, distance) != \phi なら, randomに1つ点tを選ぶ
        3. Ball(s, distance) == \phi なら, distanceをのぞいて1.に戻る
        4. chosen_list.append(s,t)
        5. swap_map_table.append((s,t)), swap_map_table.append((s,t))
    swap_map_tableに基づいてp.csvをswap
    return p.csv
```

## Usefulness Analysis
- swapのコスト$c = distance * 2$
(e.g. swapされる点が[1 1 1] と [1 2 1] ならdistance=1でcost = 2 * distance = 2)
- 上記のアルゴリズムのforループ内の2. において常に$Ball(s, distnace)!=\empty$なら, $E[distance] = (1/9) * (1/2) * 8 * 9 = 4$

すなわち, 平均的に各行4列修正するため,
理想的には(3.が起きなければ) (18-4)/18 = 0.7777..

しかし, 実験的には2.で常に$Ball(s, distnace)!=\empty$とならず, 以下のようにswap時のcostの分布が偏る.
```
usedDistanceHist:  [28 1128 5923 7053 7262 7208 7069 7170 7159]
usefullness:  0.7232255555555556
```
そのため, distance = randInt(6)にするなど調整を行っている.







## anonymize.go
p.csv, r.csvからanonymized_p.csv, anonymized_r.csv を生成

## merge_p_r.go
anonymized_p.csv, r.csvを結合して提出用のファイルanonymized.csvを生成

```
$ go run anonymize.go
$ go run merge_p_r.go
```

# term
useddistancesum: 全体を通して選ばれた距離の合計。これの2倍が総コスト
usedDistanceHist: 選ばれたdistanceの分布。左からdistance=0の個数, 1の個数,..
maxignore: n  n以下のハミング距離マッチングを無視