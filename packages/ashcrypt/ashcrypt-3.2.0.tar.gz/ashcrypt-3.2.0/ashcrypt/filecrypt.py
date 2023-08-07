"""This module is used to encrypt and decrypt files of either type str or bytes"""

from dataclasses import dataclass, field
from ashcrypt import crypt
from ashcrypt.utils import exceptions
import os


@dataclass
class CryptFile:
    """Class to encrypt/decrypt a given file. Pass in the filename as well as a 256-bit key """
    filename: str = field()
    key: str = field()

    def __post_init__(self):
        if self.keyverify(self.key) != 1:
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
        if not os.path.exists(self.filename):
            raise exceptions.fixed.FileDoesNotExistError()
        if os.path.splitext(self.filename)[1] == '.crypt':
            raise exceptions.fixed.AlreadyEncryptedError()
        with open(self.filename, 'rb') as f:
            filecontent = f.read()
        try:
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
                elif not filecontent:
                    f.write(filecontent)
                    raise exceptions.fixed.EmptyContentError()
            if go_ahead_rename_crypt == 1:
                os.rename(self.filename, self.filename + '.crypt')
                return 1
        except IOError:
            raise exceptions.fixed.SysError()

    def decrypt(self) -> int:
        if os.path.isdir(self.filename):
            raise exceptions.fixed.GivenDirectoryError()
        if not os.path.exists(self.filename):
            raise exceptions.fixed.FileDoesNotExistError()
        if os.path.splitext(self.filename)[1] != '.crypt':
            raise exceptions.fixed.AlreadyDecryptedError()
        with open(self.filename, 'rb') as f:
            enc_content = f.read()
        try:
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
                elif not enc_content:
                    f.write(enc_content)
                    raise exceptions.fixed.EmptyContentError()
                if go_ahead_remove_crypt == 1:
                    os.rename(
                        self.filename, os.path.splitext(
                            self.filename)[0])
                    return 1
        except IOError:
            raise exceptions.fixed.SysError()
