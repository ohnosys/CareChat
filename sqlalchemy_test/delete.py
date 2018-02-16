from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import User

engine = create_engine('mysql+mysqlconnector://example_user:pass@example-rds-mysql-server.cjdy4gezssw8.ap-northeast-1.rds.amazonaws.com/exampledb', echo=True)

Session = sessionmaker(bind=engine)
session = Session()
 
# 削除処理
row = session.query(User).filter_by(id=1).one()
session.delete(row)
session.commit()

