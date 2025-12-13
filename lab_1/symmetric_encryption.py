import os
from typing import Tuple
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

BITS_PER_BYTE = 8
CAST5_BLOCK_SIZE = 8
CAST5_BLOCK_SIZE_BITS = 64
IV_SIZE = 8


class CAST5Manager:
    '''
    Manages CAST5 encryption and decryption operations.
    :param key_length: Key length in bits (must be from 40 to 128 bits)
    '''

    def __init__(self, key_length: int) -> None:
        '''
        Initializes CAST5Manager with specified key length.
        :param key_length: Key length in bits
        '''
        self.key_length = key_length // BITS_PER_BYTE
        self.block_size = CAST5_BLOCK_SIZE

    def generate_key(self) -> bytes:
        '''
        Generates a random key of appropriate length.
        :return: Random bytes key
        '''
        return os.urandom(self.key_length)

    def encrypt(self, data: bytes, key: bytes) -> bytes:
        '''
        Encrypts data using CAST5 algorithm with CBC mode and PKCS7 padding.
        :param data: Plaintext data bytes to encrypt
        :param key: Encryption key bytes
        :return: Encrypted data bytes (IV + ciphertext)
        '''
        iv = os.urandom(IV_SIZE)
        cipher = Cipher(algorithms.CAST5(key), modes.CBC(iv))
        encryptor = cipher.encryptor()
        padder = padding.PKCS7(CAST5_BLOCK_SIZE_BITS).padder()
        padded_data = padder.update(data) + padder.finalize()
        encrypted = encryptor.update(padded_data) + encryptor.finalize()
        return iv + encrypted

    def decrypt(self, encrypted_data: bytes, key: bytes) -> bytes:
        '''
        Decrypts data using CAST5 algorithm with CBC mode and PKCS7 padding.
        :param encrypted_data: Encrypted data bytes (IV + ciphertext)
        :param key: Decryption key bytes
        :return: Decrypted plaintext data bytes
        '''
        iv = encrypted_data[:IV_SIZE]
        ciphertext = encrypted_data[IV_SIZE:]
        cipher = Cipher(algorithms.CAST5(key), modes.CBC(iv))
        decryptor = cipher.decryptor()
        padded_data = decryptor.update(ciphertext) + decryptor.finalize()
        unpadder = padding.PKCS7(CAST5_BLOCK_SIZE_BITS).unpadder()
        data = unpadder.update(padded_data) + unpadder.finalize()
        return data