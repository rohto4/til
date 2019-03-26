from tinydb import TinyDB, Query

# DBエンティティの作成
db = TinyDB('ongeki.json')
data_tbl = db.table('data_tbl')
py_tbl = db.table('py_tbl')

que = Query()

# 初期化
index_cnt = 0
cnt_res = data_tbl.search(que.last_insert_flg == '1')
if cnt_res.last_insert_flg == '1':
    index_cnt = cnt_res.index

cnt = py_tbl.search(que.index)

list_name = ['a', 'b', 'c']
for insert_name in list_name:
    cnt += 1
    py_tbl.insert({'index': cnt, 'name': insert_name})

# 全データ取得
print('---- 中身を確認')
for item in py_tbl:
    print(item)


