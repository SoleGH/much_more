# 操作说明
## 连接数据库
### 初始化链接信息
    create_engine(connection_info)
`connection_info`: '数据库类型+数据库驱动名称://用户名:口令@机器地址:端口号/数据库名'
### 各数据库连接样例,[官网说明](http://docs.sqlalchemy.org/en/latest/core/engines.html)

* MySQL
    ```python
    # default
    engine = create_engine('mysql://scott:tiger@localhost/foo')
    # mysql-python
    engine = create_engine('mysql+mysqldb://scott:tiger@localhost/foo')
    # MySQL-connector-python
    engine = create_engine('mysql+mysqlconnector://scott:tiger@localhost/foo')
    # OurSQL
    engine = create_engine('mysql+oursql://scott:tiger@localhost/foo')
    ```
### 创建连接
```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class MysqlOp(object):
    
    def __init__(self):
        engine_params = {
        'name_or_url':'mysql://scott:tiger@localhost/foo',
        'max_overflow': 256,
        'encoding': 'utf-8',
        'pool_recycle': 3600,
        'pool_size': 2,
        'echo': False,
        }
        self.engine = create_engine(**engine_params)
        self.session = sessionmaker(bind=engine)
        # 此session类似于一个connection ,可直接用于查询
        #session.execute(sql_str)
    
    def get_session():
        session = self.session
        session.connection()
        try:
            yield session
            session.commit()
        else:
            session.rollback()

    def init_db(self, base):
        base.metadata.create_all(self.engine)  # 创建所有表

    def drop_db(self, base):
        base.metadata.drop_all(self.engine)
    
```
### 定义models
```python
from sqlalchemy import Column
from sqlalchemy.types import CHAR, Integer, String
from sqlalchemy.ext.declarative import declarative_base


base_model = declarative_base()

class User(base_model):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(CHAR(30))  # or Column(String(30))

import MysqlOp
mysql_op = MysqlOp()
mysql_op.init_db(base_model)
```
### 获取session
```python
mysql_op = MysqlOp()
with mysql_op.get_session as session:
    session.query()
```
### CRUD
* 增
```python
user = User(name='jack')
session.add(user)
```
* 查
```python
session.query(User).all()

# 分页
session.query(User).filter(User.id == id).all().offset(index).limit(page)
# in
session.query(User).filter(User.id.in_(id_tuple)).all()
# order by
session.query(User).order_by(desc(User.id)).all()
# like and count
session.query(User).filter(Usre.name.like("%ed")).count()
```

