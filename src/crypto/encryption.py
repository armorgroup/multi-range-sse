from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import unpad

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding

import confuse
from base64 import b64encode, b64decode
import os

class AES_crypto():
    def __init__(self):
        
        config = confuse.Configuration('App')
        config.set_file('conf.yaml')
        key = config['crypto']['AES_key'].get()
        iv = config['crypto']['iv'].get()
        if key==None:
            key = get_random_bytes(16)
            print(f'b64encode key:', b64encode(key).decode('utf-8'))
            self.key = key
        else:
            self.key = b64decode(key)
        if iv==None:
            self.cipher = AES.new(self.key, AES.MODE_CBC)
            print(f'b64encode iv:', b64encode(self.cipher.iv).decode('utf-8'))
            self.iv = self.cipher.iv
        else:
            self.iv = b64decode(iv)
            self.cipher = AES.new(self.key, AES.MODE_CBC, iv=self.iv)

    def AES_encrypt(self, data):
        data = bytes(str(data), encoding='utf-8')
        ct_bytes = self.cipher.encrypt(pad(data, AES.block_size))
        return b64encode(ct_bytes).decode('utf-8')

    def AES_decrypt(self, cypherTxt):
        cypherTxt = b64decode(cypherTxt)
        try:
            cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
            plainTxt = unpad(cipher.decrypt(cypherTxt), AES.block_size)
            return float(plainTxt)
        except (ValueError, KeyError):
            print("Incorrect decryption")
            return None    
        


class AES_XTS_crypto():
    def __init__(self):
        
        config = confuse.Configuration('App')
        config.set_file('conf.yaml')
        key = config['crypto']['AES_XTS_key'].get()
        # iv = config['crypto']['iv'].get()
        if key==None:
            key = os.urandom(int(256/8))
            print(f'b64encode key:', self.__dec_utf(b64encode(key)))
            self.key = key
        else:
            self.key = b64decode(key)
    def AES_XTS_encrypt(self, data, index):
        data = self.__enc_utf(str(data))
        iv = self.__generate_iv_16(index)
        data = self.__pad(data)#pad the data (needs to be at least 16 bytes)
        enc = Cipher(algorithms.AES(self.key), modes.XTS(iv)).encryptor()#create AES-XTS cipher object given key and iv, and get the encryptor
        ciphertext = enc.update(data) + enc.finalize()#encrypt the data to get ciphertext
        return self.__dec_utf(b64encode(ciphertext))#return tuple of IV and ciphertext

    def AES_XTS_decrypt(self, cypherTxt, index):
        try:
            cypherTxt = b64decode(self.__enc_utf(cypherTxt))
            iv = self.__generate_iv_16(index)
            dec = Cipher(algorithms.AES(self.key), modes.XTS(iv)).decryptor()#create AES-XTS cipher object given key and iv, and get the decryptor
            return float(self.__dec_utf(self.__unpad(dec.update(cypherTxt) + dec.finalize()))) #decrypt the ciphertext and remove the original padding
        except:
            print("Incorrect decryption")
            return None 

    def __generate_iv_16(self, index):
        index = str(index)
        len_index = len(index)
        pad_index = " "*(16-len_index) if len_index<16 else ' '
        return self.__enc_utf((index+pad_index)[:16])

    def __enc_utf(self, data):#str to bytes
        return data.encode('utf-8')

    def __dec_utf(self, data):#bytes to str
        return data.decode('utf-8')

    def __pad(self, data):#pad 16 bytes to data
        padder = padding.PKCS7(128).padder()
        return padder.update(data) + padder.finalize()

    def __unpad(self, data):#unpad 16 bytes to data
        unpadder = padding.PKCS7(128).unpadder()
        return unpadder.update(data) + unpadder.finalize()