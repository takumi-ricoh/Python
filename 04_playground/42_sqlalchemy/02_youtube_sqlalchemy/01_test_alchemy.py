#%%
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session,sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,Integer,Float

import pandas as pd
import os

#%% セッション作成

#データベース名
database_file = os.path.join(os.path.abspath(os.getcwd()), 'data.db')

#接続の設定
engine = create_engine('sqlite:///' + database_file, convert_unicode=True, echo=False)

#セッション作成
db_session = scoped_session(
    sessionmaker(
        autocommit = False,
        autoflush = False,
        bind = engine,
    )
)

# %%データベースとのやり取りをするクラス

#ベースクラス
Base = declarative_base()

class Wine(Base): #ベースクラスの継承
    #ベースクラス自体を上書きしている。
    #こういうものなのかも。
    __tablename__ = 'wine_class'
    #Columnのidは整数型
    id = Column(Integer,primary_key=True)
    wine_class = Column(Integer,unique=False)
    alcohol = Column(Float, unique=False)
    ash = Column(Float, unique=False)
    hue = Column(Float, unique=False)
    proline = Column(Integer, unique=False)

    #idは勝手に作ってくれる
    #wine_class～prolineまでは設定して上げる必要がある
    def __init__(self, wine_class=None, alcohol=None, ash=None, hue=None, proline=None):
        self.wine_class = wine_class
        self.alcohol = alcohol
        self.ash = ash
        self.hue = hue
        self.proline = proline


#データベース初期化
#これをやらないとテーブルが作られない
#metadata：データベースの色々な情報を保持しているもの
#これはWineクラス宣言の後にやる必要がある
#Wineでなく、Baseとしても同じように動く (Base自体を上書きしているため)
Wine.metadata.create_all(bind=engine)
Wine.query = db_session.query_property()  #おまじない的な。無くても動く


#%% csvを書き込む

def set_data_csv2db():
    wine_df = pd.read_csv('wine_class.csv')

    #1行ずつデータベースに格納する
    for index,_df in wine_df.iterrows():
        #1行分をインスタンス化
        row = Wine(wine_class = _df['Class'], alcohol=_df['Alcohol'], ash=_df['Ash'], hue=_df['Hue'], proline=_df['Proline'])
        #セッションにaddする
        db_session.add(row)

    #DBへの追加を保存
    db_session.commit()

set_data_csv2db()


#%% CRUD操作：read

session = db_session

#全部抽出の場合
queries = session.query(Wine) #Wineクラスにできるクエリ候補(クラス)
db = queries.all() #すべてのデータをリストとして返す
for row in db[0:20]:
    print("read_all :::","id:",row.id,"data:",row.alcohol)


#カラム部分抽出の場合
queries = session.query(Wine.hue, Wine.proline) #Wineクラスにできるクエリ候補(クラス)
db = queries.all() #すべてのデータをリストとして返す
for row in db[0:20]:
    print("read_column:::","data:",row.hue)


#条件抽出：filter
queries = session.query(Wine) #Wineクラスにできるクエリ候補(クラス)
db = queries.filter(Wine.hue > 1.0).all() #hueが1.0より大きいものを取る
for row in db[0:20]:
    print("read_where:::","id:",row.id,"data:",row.hue)


#取得レコード数の制限：limit
queries = session.query(Wine) #Wineクラスにできるクエリ候補(クラス)
db = queries.limit(20).all()  #20個に制限
for row in db:
    print("read_limit:::","id:",row.id,"data:",row.alcohol)


#ソート：order_by
from sqlalchemy import desc #降順
queries = session.query(Wine) #Wineクラスにできるクエリ候補(クラス)
db = queries.order_by(desc(Wine.hue)).limit(20).all()
for row in db:
    print("read_orderby:::","id:",row.id,"data:",row.hue)


# %% CRUD操作：create

#1行分のデータをインスタンス化
wine = Wine(wine_class=1, alcohol=1, ash=1, proline=1)

db_session.add(wine)
db_session.commit()


#proline=1のものを抽出してみる
db = db_session.query(Wine).filter(Wine.proline==1).all()
for row in db:
    print("read_proline=1:::","id:",row.id,"data:",row.wine_class,)


#%% CRUD操作：update

db = db_session.query(Wine).filter(Wine.proline==1).first()
db.wine_class = 10
db_session.commit()


#%% CRUD操作：delete

db_session.query(Wine).filter(Wine.proline == 1).delete()

