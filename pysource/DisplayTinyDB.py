from tinydb import TinyDB
import xlsxwriter

'''
指定のTinyDB(.json)の中身をxlsxに出力します。
※同名Excelファイルには上書きする点に注意
'''

##### 初期化部 #####
# ファイル名を指定 (TinyDBをオープン)
# db = TinyDB('xxxxxxxxxx.json')
db = TinyDB('ongeki.json')
# テーブル名を指定
tbl = db.table('data_tbl')

# "ファイル名_テーブル名"の形式で指定 (同名のExcelファイルを作成)
# data_book = xlsxwriter.Workbook(r"D:\10_dev_doc\xxxxx_yyyyy.xlsx")
data_book = xlsxwriter.Workbook(r"D:\10_dev_doc\ongeki_data_tbl.xlsx")
data_sheet = data_book.add_worksheet('data_tbl')

# print('---- 中身を確認')
# for item in tbl:
#     for key in item:
#         print(key + ' : ' + item[key])

##### データ挿入部 #####
# 列名リストを作成 : 一行目のデータの保持する列名に依存
column_list = []
for item in tbl:
    for key in item:
       column_list.append(key)

# 列名をExcelファイルに書き込み
ew_row = 0
for ci in range(len(column_list)):
    data_sheet.write(ew_row, ci, column_list[ci])

'''
ここまでOK
'''

# データリストを作成
data_list = []
cnt = 0

# テーブル内の行数ループ
for item in tbl:
    # データ格納領域を追加
    # //TODO この辺りのデータ単位の配列生成方法が不明
    data_list.append([])

    # データのカラム数ループ
    for key in item:
        data_list[cnt].append(item[key])
    cnt += 1

# //TODO データ2行以上の検証必要
print(data_list)

# データリストをExcelファイルに書き込み
ew_row += 1
# 存在するデータの行数ループ
for di in range(len(data_list)):

    # データのカラム数ループ
    for d_column_i in range(len(data_list[ew_row - 1])):
        data_sheet.write(ew_row, di, data_list[ew_row - 1][di - 1])
        ew_row += 1

data_book.close()



