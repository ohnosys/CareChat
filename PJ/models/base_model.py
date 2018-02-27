from sqlalchemy import Column, Integer
from sqlalchemy.ext.declarative import declared_attr, declarative_base

from backend import Backend

Base = declarative_base()

# 本来SQLAlchemyではテーブル定義とPythonクラス（自作）を別々に作ってマッピングだけど、
# きっちり分けないで済むようにdeclarative_baseを利用してBaseクラスを作って継承させる

# Base = declarative_base を拡張したい
# djangolikeなmodel定義にするmixin    
# DjangoLike DBを直接扱わなくていいように、Djangoのようにmodels.pyを作成して、そこに記述するクラスを操作することでDB操作する

class DjangoLikeModelMixin(object):

    # dclarative_base()で生成したクラスオブジェクトはモデルを書くときにテーブル名と主キーを書かないとAlchemyさんに怒られる

    # id は全てのクラスで使うので
    id = Column(Integer, primary_key=True)

    # __tablename__ = "user" と同じ（定義するのが面倒くさいからdeclarative_base）
    # __tablename__ == user.py の class User を入れて小文字にしてる 
    
    @declared_attri # Foreign KeyなどをMixinで定義するときに付ける必要があるデコレータ
    def __tablename__(cls):
        return cls.__name__.lower()

    @classmethod # クラス変数にアクセス / 動作が変わるべきとき
    def get(cls, id):
        return cls.session().query(cls).get(id)

    @classmethod
    def search_name(cls, name):
        return cls.session().query(cls).filter(cls.name.ilike('%{0}%'.format(name))).order_by(cls.name).all()

    def save(self):
        self.session().add(self)
        self.session().commit()

    def delete(self):
        self.session().delete(self)
        self.session().commit()

    @staticmethod # 継承クラスでも動作変わらない
    def session():
        return Backend.instance().get_session()

