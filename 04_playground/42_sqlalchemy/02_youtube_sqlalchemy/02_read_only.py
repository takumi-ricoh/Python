from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session,sessionmaker
from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declarative_base
import os

#%% セッション作成

#データベース名
database_file = os.path.join(os.path.abspath(os.getcwd()), 'data.db')

#接続の設定
engine = create_engine('sqlite:///' + database_file, convert_unicode=True, echo=False)


#%% クラス
Base = declarative_base(bind = engine)


