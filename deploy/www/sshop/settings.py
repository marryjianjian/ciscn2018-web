import os, base64

limit = 10
username = '4uuu'
email = 'i@qvq.im'
debug = True

connect_str = 'sqlite:///%s' % os.path.join(os.getcwd(), 'sshop.db3')
flag = open('flag.txt').read().strip()
key = 'SY6dubPQqDP78J/gb9Rq41/QTrqAlfWL'
cookie_secret = base64.b64encode((flag[6:-1].decode('hex')*2)+key[:4])
