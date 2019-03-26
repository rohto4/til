from tinydb import TinyDB, Query
from datetime import datetime

# jsonファイルを指定
db = TinyDB('ongeki.json')

# テーブル名を指定
data_tbl = db.table('data_tbl')

# データ準備
d = datetime.now().strftime("%Y%m%d")

# 書き込み
data_tbl.insert({'name': 'search_ongeki', 'count': '0', 'created_date': d})

# 結果を確認
print(data_tbl.all())