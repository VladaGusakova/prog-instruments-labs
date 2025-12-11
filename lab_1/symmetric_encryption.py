from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
import os

class CAST5Manager:
    def __init__(self, key_length):
        self.key_length = key_length // 8
        self.block_size = 8

    def generate_key(self):
        return os.urandom(self.key_length)

    def encrypt(self, data, key):
        iv = os.urandom(8)
        cipher = Cipher(algorithms.CAST5(key), modes.CBC(iv))
        encryptor = cipher.encryptor()
        padder = padding.PKCS7(64).padder()
        padded_data = padder.update(data) + padder.finalize()
        encrypted = encryptor.update(padded_data) + encryptor.finalize()
        return iv + encrypted

    def decrypt(self, encrypted_data, key):
        iv = encrypted_data[:8]
        ciphertext = encrypted_data[8:]
        cipher = Cipher(algorithms.CAST5(key), modes.CBC(iv))
        decryptor = cipher.decryptor()
        padded_data = decryptor.update(ciphertext) + decryptor.finalize()
        unpadder = padding.PKCS7(64).unpadder()
        data = unpadder.update(padded_data) + unpadder.finalize()
        return data
