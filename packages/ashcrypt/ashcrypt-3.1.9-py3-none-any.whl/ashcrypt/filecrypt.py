"""This module is used to encrypt and decrypt files of either type str or bytes"""


from ashcrypt import crypt
from ashcrypt.utils import exceptions
import os


class CryptFile:
    """Class to encrypt/decrypt a given file. Pass in the filename
                as well as a 256-bit key """

    def __init__(self, filename: str, key: str):
        self.filename = filename
        self.bad_key = 0
        if self.keyverify(key) == 1:
            self.key = key
        else:
            raise exceptions.dynamic.KeyLengthError()

    @staticmethod
    def genkey() -> str:
        return crypt.Enc.genkey()

    @staticmethod
    def keyverify(key: str) -> int:
        try:
            a = bytes.fromhex(key.strip())
            if len(a) == 32:
                return 1
        except ValueError:
            return 0

    def encrypt(self) -> int:
        if os.path.isdir(self.filename):
            raise exceptions.fixed.GivenDirectoryError()
        if self.bad_key == 1:
            raise exceptions.dynamic.KeyLengthError()
        try:
            if not os.path.exists(self.filename):
                raise exceptions.fixed.FileDoesNotExistError()
            else:
                if os.path.splitext(self.filename)[1] == '.crypt':
                    raise exceptions.fixed.AlreadyEncryptedError()
                else:
                    with open(self.filename, 'rb') as f:
                        filecontent = f.read()
                    with open(self.filename, 'wb') as f:
                        if filecontent:
                            try:
                                ins = crypt.Enc(
                                    message=filecontent, mainkey=self.key)
                                new_content = ins.encrypt(get_bytes=True)
                                f.write(new_content)
                                go_ahead_rename_crypt = 1
                            except BaseException:
                                f.write(filecontent)
                                raise exceptions.fixed.FileCryptError()
                        else:
                            f.write(filecontent)
                            raise exceptions.fixed.EmptyContentError()
                    if go_ahead_rename_crypt == 1:
                        os.rename(self.filename, self.filename + '.crypt')
                        return 1
        except Exception:
            raise exceptions.fixed.SysError()

    def decrypt(self) -> int:
        if os.path.isdir(self.filename):
            raise exceptions.fixed.GivenDirectoryError()
        if self.bad_key == 1:
            raise exceptions.dynamic.KeyLengthError()
        try:
            if not os.path.exists(self.filename):
                raise exceptions.fixed.FileDoesNotExistError()
            else:
                if os.path.splitext(self.filename)[1] != '.crypt':
                    raise exceptions.fixed.AlreadyDecryptedError()
                else:
                    with open(self.filename, 'rb') as f:
                        enc_content = f.read()
                    with open(self.filename, 'wb') as f:
                        if enc_content:
                            try:
                                ins = crypt.Dec(
                                    message=enc_content, mainkey=self.key)
                                a = ins.decrypt(get_bytes=True)
                                f.write(a)
                                go_ahead_remove_crypt = 1
                            except Exception:
                                f.write(enc_content)
                                raise exceptions.fixed.FileCryptError()
                        else:
                            f.write(enc_content)
                            raise exceptions.fixed.EmptyContentError()
                    if go_ahead_remove_crypt == 1:
                        os.rename(
                            self.filename, os.path.splitext(
                                self.filename)[0])
                        return 1
        except Exception:
            raise exceptions.fixed.SysError()

    def __str__(self):
        return f'Encrypting/Decrypting File {self.filename} With {self.key} Key '

    def __repr__(self):
        return f'{self.__class__.__name__}({self.filename},{self.key})'
