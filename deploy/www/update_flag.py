import os
from hashlib import sha256

with open('flag.txt', 'w') as f:
    flag = 'CISCN{' + sha256(os.urandom(16)).hexdigest()[32:] + '}'
    f.write(flag)
