"""This module is used to encrypt and decrypt text data"""

from ashcrypt.utils import exceptions
from ashcrypt import crypt as ac
from typing import Union


class Crypt:
    def __init__(self, text: Union[str, bytes], key: str):
        self.text = text
        if self.keyverify(key) == 1:
            self.key = key
        else:
            raise exceptions.dynamic.KeyLengthError()

    @staticmethod
    def genkey() -> str:
        return ac.Enc.genkey()

    @staticmethod
    def keyverify(key: str) -> int:
        try:
            a = bytes.fromhex(key.strip())
            if len(a) == 32:
                return 1
        except ValueError:
            return 0

    def encrypt(self) -> tuple:
        if self.text:
            try:
                ins = ac.Enc(self.text, self.key)
                new_content = ins.encrypt()
                return 1, new_content
            except BaseException:
                raise exceptions.fixed.CryptError()
        else:
            raise exceptions.fixed.EmptyContentError()

    def decrypt(self) -> tuple:
        if self.text:
            try:
                dec_instance = ac.Dec(message=self.text, mainkey=self.key)
                a = dec_instance.decrypt()
                output = a
                return 1, output
            except BaseException:
                raise exceptions.fixed.CryptError()
        else:
            raise exceptions.fixed.EmptyContentError()

    def __str__(self):
        return f'Encrypting/Decrypting Text {self.text[:8]}.. With {self.key} Key '

    def __repr__(self):
        return f'{self.__class__.__name__}({self.text[:8]},{self.key})'
