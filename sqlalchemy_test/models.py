from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
 
Base = declarative_base()
 
 
class User(Base):
    # テーブル定義
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(15))
    fullname = Column(String(30))
    password = Column(String(100))
 
if __name__ == "__main__":
    # データベース接続

    engine = create_engine('mysql+mysqlconnector://example_user:pass@example-rds-mysql-server.cjdy4gezssw8.ap-northeast-1.rds.amazonaws.com/exampledb', echo=True)

    Base.metadata.create_all(engine)  # テーブル作成


