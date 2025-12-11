from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes

PUBLIC_EXPONENT = 65537


class RSAManager:
    '''
    Manages RSA key generation, encryption and decryption operations.
    '''

    def __init__(self, key_size):
        '''
        Initializes RSAManager with specified key size.
        :param key_size: Size of RSA key in bits
        '''
        self.key_size = key_size
        self.padding_scheme = padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )

    def generate_key_pair(self):
        '''
        Generates RSA private and public key pair.
        :return: Tuple containing private key and public key
        '''
        private_key = rsa.generate_private_key(
            public_exponent=PUBLIC_EXPONENT,
            key_size=self.key_size
        )
        return private_key, private_key.public_key()

    def encrypt(self, data, public_key):
        '''
        Encrypts data using RSA public key with OAEP padding.
        :param data: Data bytes to encrypt
        :param public_key: RSA public key object
        :return: Encrypted data bytes
        '''
        try:
            return public_key.encrypt(data, self.padding_scheme)
        except Exception as e:
            raise Exception(f"RSA encryption failed: {e}")

    def decrypt(self, encrypted_data, private_key):
        '''
        Decrypts data using RSA private key with OAEP padding.
        :param encrypted_data: Encrypted data bytes to decrypt
        :param private_key: RSA private key object
        :return: Decrypted data bytes
        '''
        try:
            return private_key.decrypt(encrypted_data, self.padding_scheme)
        except Exception as e:
            raise Exception(f"RSA decryption failed: {e}")