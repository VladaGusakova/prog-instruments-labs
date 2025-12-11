from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes

class RSAManager:
    def __init__(self, key_size):
        self.key_size = key_size
        self.padding_scheme = padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(),label=None)

    def generate_key_pair(self):
        private_key = rsa.generate_private_key(public_exponent=65537, key_size=self.key_size)
        return private_key, private_key.public_key()

    def encrypt(self, data, public_key):
        try:
            return public_key.encrypt(data, self.padding_scheme)
        except Exception as e:
            raise Exception(f"RSA encryption failed: {e}")

    def decrypt(self, encrypted_data, private_key):
        try:
            return private_key.decrypt(encrypted_data, self.padding_scheme)
        except Exception as e:
            raise Exception(f"RSA decryption failed: {e}")