from aityz import exceptions
import rsa
from Crypto.Cipher import AES
import base64
import hashlib


def pad(pad, length=16):
    """
    Pad a given string `pad` with spaces to a specified `length`.

    :param pad: The string to be padded.
    :param length: The desired length of the padded string. Default is 16.
    :return: The padded string.
    """
    lenPad = len(pad) % length
    return pad + (length - lenPad) * ' '


class RSA:
    """
    Initialize an RSA object.

    :param bits: The number of bits for the RSA key. Default is 2048.
    :param fromFile: If set to True, the constructor expects the priKey and pubKey parameters to be provided and loads the RSA keys from the specified files. Default is False.
    :param priKey: The path to the file containing the private key in PKCS1 format. Required if fromFile is True.
    :param pubKey: The path to the file containing the public key in PKCS1 format. Required if fromFile is True.
    """

    def __init__(self, bits=2048, fromFile=False, priKey=None, pubKey=None):
        """
        :param bits: The number of bits for the RSA key. Default is 2048.
        :param fromFile: If set to True, the constructor expects the priKey and pubKey parameters to be provided and loads the RSA keys from the specified files. Default is False.
        :param priKey: The path to the file containing the private key in PKCS1 format. Required if fromFile is True.
        :param pubKey: The path to the file containing the public key in PKCS1 format. Required if fromFile is True.
        """
        super().__init__()
        if fromFile:
            print('From File is True, Using priKey and pubKey variables!')
            if priKey is None or pubKey is None:
                raise exceptions.InitialisationError
            else:
                with open(pubKey, 'rb') as f:
                    pub_key_data = f.read()
                    self.Pub = rsa.PublicKey.load_pkcs1(pub_key_data)

                with open(priKey, 'rb') as f:
                    pri_key_data = f.read()
                    self.Pri = rsa.PrivateKey.load_pkcs1(pri_key_data)
        else:
            print('Generating RSA Keys...')
            self.Pub, self.Pri = rsa.newkeys(bits)

    def save(self, priKey='priKey.pem', pubKey='pubKey.pem'):
        """
        Save the RSA private and public keys to files.

        :param priKey: The file name to save the private key. Default is 'priKey.pem'.
        :param pubKey: The file name to save the public key. Default is 'pubKey.pem'.
        :return: None
        """
        with open(priKey, 'wb') as f:
            f.write(self.Pri.save_pkcs1())

        with open(pubKey, 'wb') as f:
            f.write(self.Pub.save_pkcs1())

    def encrypt(self, content):
        """
        Encrypts the given content using the RSA encryption algorithm.

        :param content: The content to be encrypted.
        :return: The encrypted content.
        """
        return rsa.encrypt(content.encode(), self.Pub)

    def encryptFile(self, filename, outputFile=None):
        """
        Encrypts the contents of the file with RSA encryption.

        :param filename: The path to the input file.
        :param outputFile: The path to the output file. (optional)
        :return: The encrypted data if `outputFile` is not provided.
        """
        with open(filename, 'rb') as f:
            data = f.read()
            f.close()
        encData = rsa.encrypt(data, self.Pub)
        if outputFile is not None:
            with open(outputFile, 'wb') as f:
                f.write(encData)
        else:
            return encData

    def decrypt(self, content):
        return rsa.decrypt(content, self.Pri)

    def decryptFile(self, filename, outputFile=None):
        with open(filename, 'rb') as f:
            data = f.read()
            f.close()
        Data = rsa.decrypt(data, self.Pri)
        if outputFile is not None:
            with open(outputFile, 'wb') as f:
                f.write(Data)
        else:
            return Data


def loadNonce(loc='nonce.txt'):
    with open(loc, 'rb') as f:
        nonce = f.read()
    return nonce


class AES256:
    def __init__(self, password, nonce=None):
        super().__init__()
        self.key = pad(password)
        if len(password) % 16 != 0:
            password = pad(password)
        if nonce is None:
            self.cipher = AES.new(password.encode('utf8'), AES.MODE_EAX)
        else:
            self.cipher = AES.new(password.encode('utf8'), AES.MODE_EAX, nonce=nonce)

    def encrypt(self, content):
        enc, tag = self.cipher.encrypt_and_digest(content.encode('utf-8'))
        return enc, tag, self.cipher.nonce

    def getNonce(self):
        return self.cipher.nonce

    def decrypt(self, content):
        return self.cipher.decrypt(content)

    def saveNonce(self, save='nonce.txt'):
        with open(save, 'wb') as f:
            f.write(self.cipher.nonce)

    def verify(self, tag):
        try:
            return self.cipher.verify(tag)
        except ValueError:
            return 'Incorrect tag/corrupted message'

    def encryptFile(self, fileName, saveLoc=None):
        with open(fileName, 'r') as f:
            data = f.read()
        if saveLoc is not None:
            with open(saveLoc, 'w') as f:
                f.write(str(self.cipher.encrypt(data.encode('utf-8'))))
        else:
            return str(self.cipher.encrypt(data.encode('utf-8')))

    def decryptFile(self, fileName, saveLoc=None):
        with open(fileName, 'r') as f:
            data = f.read()
        if saveLoc is not None:
            with open(saveLoc, 'w') as f:
                f.write(str(self.cipher.decrypt(data.encode('utf-8'))))
        else:
            return str(self.cipher.decrypt(data.encode('utf-8')))

    def update(self, nonce=None):
        if nonce is None:
            self.cipher = AES.new(self.key, AES.MODE_EAX)
        else:
            self.cipher = AES.new(self.key, AES.MODE_EAX, nonce=nonce)


class SHA3:
    def __init__(self, size):
        super().__init__()
        if size != 224 and size != 256 and size != 384 and size != 512:
            raise exceptions.SizeError()
        if size == 224:
            self.hasher = hashlib.sha3_224()
        elif size == 256:
            self.hasher = hashlib.sha3_256()
        elif size == 384:
            self.hasher = hashlib.sha3_384()
        elif size == 512:
            self.hasher = hashlib.sha3_512()

    def encrypt(self, data: str):
        self.hasher.update(data.encode('utf8'))
        return self.hasher.hexdigest()


class SHA2:
    def __init__(self, size):
        super().__init__()
        if size != 224 and size != 256 and size != 384 and size != 512:
            raise exceptions.SizeError()
        if size == 224:
            self.hasher = hashlib.sha224()
        elif size == 256:
            self.hasher = hashlib.sha256()
        elif size == 384:
            self.hasher = hashlib.sha384()
        elif size == 512:
            self.hasher = hashlib.sha512()

    def encrypt(self, data: str):
        self.hasher.update(data.encode('utf8'))
        return self.hasher.hexdigest()


class SHA1:  # It's no longer secure
    def __init__(self, ignore=False):
        if ignore is not True:
            print('SHA-1 Hashing has been compromised. Use SHA-3 or SHA-2 Instead.')
            print('If you would not like to see this warning pass ignore=True to this class next use.')
        self.hasher = hashlib.sha1()

    def encrypt(self, data: str):
        self.hasher.update(data.encode())
        return self.hasher.hexdigest()


class Whirlpool:
    def __init__(self):
        self.hasher = hashlib.new('whirlpool')

    def encrypt(self, data: str):
        self.hasher.update(data.encode())
        return self.hasher.hexdigest()

