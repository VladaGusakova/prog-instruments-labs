from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
import os


class CAST5Manager:
    '''
    Manages CAST5 encryption and decryption operations.
    :param key_length: Key length in bits (must be from 40 to 128 bits)
    '''

    def __init__(self, key_length):
        '''
        Initializes CAST5Manager with specified key length.
        :param key_length: Key length in bits
        '''
        self.key_length = key_length // 8
        self.block_size = 8

    def generate_key(self):
        '''
        Generates a random key of appropriate length.
        :return: Random bytes key
        '''
        return os.urandom(self.key_length)

    def encrypt(self, data, key):
        '''
        Encrypts data using CAST5 algorithm with CBC mode and PKCS7 padding.
        :param data: Plaintext data bytes to encrypt
        :param key: Encryption key bytes
        :return: Encrypted data bytes (IV + ciphertext)
        '''
        iv = os.urandom(8)
        cipher = Cipher(algorithms.CAST5(key), modes.CBC(iv))
        encryptor = cipher.encryptor()
        padder = padding.PKCS7(64).padder()
        padded_data = padder.update(data) + padder.finalize()
        encrypted = encryptor.update(padded_data) + encryptor.finalize()
        return iv + encrypted

    def decrypt(self, encrypted_data, key):
        '''
        Decrypts data using CAST5 algorithm with CBC mode and PKCS7 padding.
        :param encrypted_data: Encrypted data bytes (IV + ciphertext)
        :param key: Decryption key bytes
        :return: Decrypted plaintext data bytes
        '''
        iv = encrypted_data[:8]
        ciphertext = encrypted_data[8:]
        cipher = Cipher(algorithms.CAST5(key), modes.CBC(iv))
        decryptor = cipher.decryptor()
        padded_data = decryptor.update(ciphertext) + decryptor.finalize()
        unpadder = padding.PKCS7(64).unpadder()
        data = unpadder.update(padded_data) + unpadder.finalize()
        return data