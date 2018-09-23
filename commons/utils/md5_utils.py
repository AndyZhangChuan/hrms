# -*- encoding: utf8 -*-

import random
import hashlib


def generate_random_md5_str():
    seed = "1234567890abcdefghijklmnopqrstuvwxyz"
    sa = []
    for i in range(8):
        sa.append(random.choice(seed))
    salt = ''.join(sa)
    hash_str = hashlib.md5()
    hash_str.update(salt.encode())
    return hash_str.hexdigest()