from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import User

# データベース接続
engine = create_engine('mysql+mysqlconnector://example_user:pass@example-rds-mysql-server.cjdy4gezssw8.ap-northeast-1.rds.amazonaws.com/exampledb', echo=True)

# セッションの作成
Session = sessionmaker(bind=engine)
session = Session()

# ユーザーを１件登録
ed_user = User(name='ed', fullname='Ed Jones', password='edspassword')
session.add(ed_user)

# ユーザーを複数登録
session.add_all([
    User(name='wendy', fullname='Wendy Williams', password='foobar'),
    User(name='mary', fullname='Mary Contrary', password='xxg527'),
    User(name='fred', fullname='Fred Flinstone', password='blah')])

# commit() 現在処理されずに残っているデータの変更をすべてデータベースに反映してトランザクションをコミットする
session.commit()
