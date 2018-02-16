from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import User



engine = create_engine('mysql+mysqlconnector://example_user:pass@example-rds-mysql-server.cjdy4gezssw8.ap-northeast-1.rds.amazonaws.com/exampledb', echo=False)
Session = sessionmaker(bind=engine)
session = Session()
 
for row in session.query(User).all():
    print(row.id, row.name, row.fullname, row.password)
