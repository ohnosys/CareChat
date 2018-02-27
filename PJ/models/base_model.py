from sqlalchemy import Column, Integer
from sqlalchemy.ext.declarative import declared_attr, declarative_base

from backend import Backend

Base = declarative_base()

# models.py は モデルをORMで書くところ
# モデルの設定ファイル↓
# Django は models.py
# Trnado は modelsディレクトリ内の各ファイル
# view.py は 長くなりすぎるので分割したりロジックだけ別コードに書き出したりしている

class DjangoLikeModelMixin(object):
    # Base = declarative_base を拡張したい
    # djangolikeなmodel定義にするmixin    

    # dclarative_base()で生成したクラスオブジェクトはモデルを書くときにテーブル名と主キーを書かないとAlchemyさんに怒られる

    # id は全てのクラスで使うので
    id = Column(Integer, primary_key=True)

    # 例えば __tablename__ = "user" と同じ（定義するのが面倒くさいから）
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

