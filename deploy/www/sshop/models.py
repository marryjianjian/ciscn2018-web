import os
import string
import bcrypt
import random
from datetime import date

from sqlalchemy import Column
from sqlalchemy.dialects.sqlite import FLOAT, VARCHAR, INTEGER
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from settings import connect_str, cookie_secret

BaseModel = declarative_base()
engine = create_engine(connect_str, echo=True, pool_recycle=3600)
db = scoped_session(sessionmaker(bind=engine))


class Commodity(BaseModel):
    __tablename__ = 'commoditys'

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    name = Column(VARCHAR(200), unique=True, nullable=False)
    desc = Column(VARCHAR(500), default='no description')
    amount = Column(INTEGER, default=10)
    price = Column(FLOAT, nullable=False)

    def __repr__(self):
        return '<Commodity: %s>' % self.name

    def __price__(self):
        return self.price

    def sell(self, num):
        if type(num) is int and self.amount >= num:
            res = self.amount - num
            return res
        else: return None


class User(BaseModel):
    __tablename__ = 'user'

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    username = Column(VARCHAR(130))
    mail = Column(VARCHAR(50))
    password = Column(VARCHAR(130))
    integral = Column(FLOAT, default=2333)
    seckill = Column(INTEGER, default=1)

    def check(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf8'))

    def __repr__(self):
        return '<User: %s>' % self.username

    def pay(self, num):
        res = (self.integral - num) if (self.integral - num) else False
        if res >= 0:
            return res
        else:
            return None

    def __integral__(self):
        return self.integral

    def is_vip(self):
        if 'vip' in self.username.lower():
            return True
        else: return False


class Shopcar(BaseModel):
    __tablename__ ='shopcar'

    id = Column(INTEGER, primary_key=True, autoincrement=True)



if __name__ == "__main__":
    BaseModel.metadata.create_all(engine)
    # for i in xrange(49):
        # name = ''.join(random.sample(string.ascii_letters, 16))
        # desc = ''.join(random.sample(string.ascii_letters * 5, 100))
        # price = random.randint(10, 200)
    for i in range(1,11):
        name = 'iphone%s' % i
        desc = 'this is iphone%s you must be wanna it! just buy it!' %i
        price = i*100
        if i == 10:
            name = 'iphoneX'
            desc = 'this is iphoneX you must be wanna it! just buy it!'
        if i == 9:
            name = 'iphone8plus'
            desc = 'this is iphone8plus you must be wanna it !just buy it!'
        db.add(Commodity(name=name, desc=desc, price=price))
    db.add(User(username='vip', mail='i@vip.me', password=bcrypt.hashpw(cookie_secret, bcrypt.gensalt())))
    db.commit()
