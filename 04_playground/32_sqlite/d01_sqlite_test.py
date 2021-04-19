import sqlite3
import pandas as pd

#%% データベースの作成：■データベース1
dbname = "TEST.db"

#存在しない場合は新規に作られる
conn = sqlite3.connect(dbname)

#操作用のカーソルオブジェクト
cur = conn.cursor()

#personsというテーブルを作る
#大文字がSQL文
# cur.execute(
#     'CREATE TABLE persons ( id INTEGER PRIMARY KEY AUTOINCREMENT,\
#     name STRING)' )


#%% データの挿入
#"name"に"Taro"を入れる
cur.execute('INSERT INTO persons(name) values("Taro")')
#どうように、HanakoとHirokiも入れる
cur.execute('INSERT INTO persons(name) values("Hanako")')
cur.execute('INSERT INTO persons(name) values("Hiroki")')

#%% テーブルの内容確認
#terminalと同様にSQL文と同じようにexecuteに書く
cur.execute('SELECT * FROM persons')


print("############################################")
print("データベース1：persons")
#中身を全て取得するfetchall()を使って、printする
print(cur.fetchall())


#%% Pandasから作る：■データベース2
data = {"year":[2012,2014,2016],\
        "month":[11,10,6],\
        "day":[15,18,22]}
df = pd.DataFrame(data)

df.to_sql("sample_df", conn, if_exists='replace')

print("############################################")
print("データベース2：sample_df")

select_sql = "SELECT * FROM sample_df"
for row in cur.execute(select_sql):
    print(row)


#%% DBをPandasで開く
df2 = pd.read_sql("SELECT * FROM sample_df",conn)

print("############################################")
print("データベース2(SQLite)をpandasで開く")
print(df2)


#%% 保存&終了
#データベースにコミット。変更が反映される。
conn.commit()

#閉じる
conn.close()

