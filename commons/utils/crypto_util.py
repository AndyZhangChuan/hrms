# -*- encoding: utf8 -*-
# requirements: cryptography==1.4
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend
from cryptography.exceptions import InvalidSignature

MAX_ENCRYPT_SIZE = 117
MAX_DECRYPT_SIZE = 128


class PrivateKey(object):
    @classmethod
    def init_from_file(cls, key_path, password=None):
        key_file = open(key_path, "rb")
        return cls(key_file.read(), password=password)

    def __init__(self, key_block, password=None):
        self.priv = serialization.load_pem_private_key(
            key_block, password=password, backend=default_backend())
        self.pub = self.priv.public_key()

    def sign(self, msg):
        sign = self.priv.sign(
            msg,
            padding.PKCS1v15(),
            hashes.SHA1()
        )
        return sign

    def _verify(self, signature, msg):
        verify = self.pub.verify(
            signature,
            msg,
            padding.PKCS1v15(),
            hashes.SHA1()
        )
        return verify

    def verify(self, signature, msg):
        try:
            self._verify(signature, msg)
            return True
        except InvalidSignature as e:
            print str(e)
            return False

    def encrypt(self, msg):
        cipher = ''
        if len(msg) <= MAX_ENCRYPT_SIZE:
            cipher = self.pub.encrypt(
                msg,
                padding.PKCS1v15()
            )
        else:
            offset = 0
            while offset < len(msg):
                end = offset + MAX_ENCRYPT_SIZE
                cipher += self.encrypt(msg[offset: end])
                offset = end
        return cipher

    def decrypt(self, cipher):
        plain = ''
        if len(cipher) <= MAX_DECRYPT_SIZE:
            plain = self.priv.decrypt(
                cipher,
                padding.PKCS1v15()
            )
        else:
            offset = 0
            while offset < len(cipher):
                end = offset + MAX_DECRYPT_SIZE
                plain += self.decrypt(cipher[offset: end])
                offset = end
        return plain


class PublicKey(object):
    def __init__(self, key_block):
        self.pub = serialization.load_pem_public_key(
            key_block,
            backend=default_backend()
        )

    def verify(self, sign, msg):
        try:
            self.pub.verify(sign, msg, padding.PKCS1v15(), hashes.SHA1())
            return True
        except InvalidSignature as e:
            print str(e)
            return False


def rc4(data, key):
    """RC4 encryption and decryption method."""
    S, j, out = list(range(256)), 0, []

    for i in range(256):
        j = (j + S[i] + ord(key[i % len(key)])) % 256
        S[i], S[j] = S[j], S[i]

    i = j = 0
    for ch in data:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        out.append(chr(ord(ch) ^ S[(S[i] + S[j]) % 256]))

    return "".join(out)

