import tornado.web
from sqlalchemy.orm.exc import NoResultFound
from sshop.base import BaseHandler
from sshop.models import Commodity, User
from sshop.settings import limit, flag
from random import randint


class ShopIndexHandler(BaseHandler):
    def get(self, *args, **kwargs):
        return self.redirect('/shop')


class ShopListHandler(BaseHandler):
    def get(self):
        page = self.get_argument('page', 1)
        page = int(page) if int(page) else 1
        commoditys = self.orm.query(Commodity) \
            .filter(Commodity.amount > 0) \
            .order_by(Commodity.price.desc()) \
            .limit(limit).offset((page - 1) * limit).all()
        return self.render('index.html', commoditys=commoditys, preview=page - 1, next=page + 1, limit=limit)


class ShopDetailHandler(BaseHandler):
    def get(self, id=1):
        try:
            commodity = self.orm.query(Commodity) \
                .filter(Commodity.id == int(id)).one()
        except NoResultFound:
            return self.redirect('/')
        return self.render('info.html', commodity=commodity)


class ShopPayHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self):
        try:
            price = self.get_argument('price')
            user = self.orm.query(User).filter(User.username == self.current_user).one()
            cid = self.get_argument('id')
            commodity = self.orm.query(Commodity).filter(Commodity.id==cid).one()
            remc = commodity.sell(1)
            if remc is not None:
                commodity.amount = remc
            else:
                return self.render('pay.html', danger=1, message='good not enough buddy')
            remc = user.pay(float(price))
            if remc is not None:
                user.integral = remc
            else:
                return self.render('pay.html', danger=1, message='money not enough buddy')
            self.orm.commit()
            return self.render('pay.html', success=1)
        except:
            return self.render('pay.html', danger=1, message='you mao bing')


class ShopCarHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        id = self.get_secure_cookie('commodity_id')
        if id:
            commodity = self.orm.query(Commodity).filter(Commodity.id == id).one()
            return self.render('shopcar.html', commodity=commodity)
        return self.render('shopcar.html')

    @tornado.web.authenticated
    def post(self, *args, **kwargs):
        try:
            price = self.get_argument('price')
            user = self.orm.query(User).filter(User.username == self.current_user).one()
            res = user.pay(float(price))
            cid = self.get_secure_cookie('commodity_id')
            commodity = self.orm.query(Commodity).filter(Commodity.id==cid).one()
            ans = commodity.sell(1)
            if res is not None and ans is not None:
                user.integral = res
                commodity.amount = ans
                self.orm.commit()
                self.clear_cookie('commodity_id')
                return self.render('shopcar.html', success=1)
        except Exception as ex:
            print str(ex)
        return self.redirect('/shopcar')


class ShopCarAddHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self, *args, **kwargs):
        id = self.get_argument('id')
        self.set_secure_cookie('commodity_id', id)
        return self.redirect('/shopcar')


class SecKillHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        cid = randint(1, 10)
        return self.render('seckill.html', cid=cid, vip=False)

    @tornado.web.authenticated
    def post(self, *args, **kwargs):
        cid = randint(1, 10)
        user = self.orm.query(User).filter(User.username == self.current_user).one()
        try:
            id = self.get_argument('id')
            user = self.orm.query(User).filter(User.username == self.current_user).one()
            commodity = self.orm.query(Commodity).filter(Commodity.id == id).one()
            ans = commodity.sell(1)
            res = user.pay(float(commodity.price))
            if res is not None and ans is not None:
                user.integral = res
                commodity.amount = ans
            else:
                return self.render('seckill.html', danger=1, cid=cid, vip=False, message='good not enough buddy')
            if user.seckill == 1:
                user.seckill -= 1
                self.orm.commit()
                return self.render('seckill.html', success=1, cid=cid, vip=False, message='Impossible!')
            else:
                if user.is_vip():
                    return self.render('seckill.html', success=1, cid=cid, vip=True, message=flag)
                else:
                    return self.render('seckill.html', danger=1, cid=cid, vip=True, message='you need to be vip to get flag')
        except:
            return self.render('seckill.html', danger=1, cid=cid, vip=False, message='you mao bing')
