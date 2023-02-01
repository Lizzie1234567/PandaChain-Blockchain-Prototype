import binascii

from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.PublicKey.RSA import RsaKey

from .AMessage import EMessageType
from .PlainTextMessage import PlainTextMessage


class EncryptedTextMessage(PlainTextMessage):

    def __init__(self, message: str):
        super().__init__(message)

    def soft_encrypt(self, address: str) -> str:
        from bc import rsa_long_encrypt
        enc = rsa_long_encrypt(binascii.unhexlify(address), self.message.encode('utf-8'))
        return binascii.hexlify(enc).decode('ascii')

    def encrypt(self, address: str):
        self.message = self.soft_encrypt(address=address)

    def soft_decrypt(self, key: RsaKey) -> str:
        from bc import rsa_long_decrypt
        dec = rsa_long_decrypt(key, binascii.unhexlify(self.message)).decode('utf-8')

        return dec

    def decrypt(self, key: RsaKey):
        self.message = self.soft_decrypt(key)

    @property
    def message_type(self) -> int:
        return EMessageType.ENCRYPTED_TEXT
