from typing import Dict, Any
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey, RSAPublicKey
from asymmetric_encryption import RSAManager
from symmetric_encryption import CAST5Manager
from file_manager import FileManager

DEFAULT_RSA_KEY_SIZE = 2048
DEFAULT_CAST_KEY_LENGTH = 128


class HybridCrypto:
    def __init__(self, config: Dict[str, Any], file_manager: FileManager) -> None:
        '''
        Initializes HybridCrypto with configuration and file manager.
        :param config: Configuration dictionary
        :param file_manager: File manager instance
        '''
        self.config = config
        self.file_manager = file_manager
        self.rsa_manager = RSAManager(config.get('rsa_key_size', DEFAULT_RSA_KEY_SIZE))
        self.cast_manager = CAST5Manager(config.get('cast_key_length', DEFAULT_CAST_KEY_LENGTH))

    def generate_keys(self) -> None:
        '''
        Generates RSA key pair and CAST5 symmetric key.
        Saves keys to files defined in configuration.
        '''
        cast_key = self.cast_manager.generate_key()
        private_key, public_key = self.rsa_manager.generate_key_pair()

        self.file_manager.save_private_key_pem(private_key, self.config['private_key'])
        self.file_manager.save_public_key_pem(public_key, self.config['public_key'])

        encrypted_cast_key = self.rsa_manager.encrypt(cast_key, public_key)
        self.file_manager.write_file(encrypted_cast_key, self.config['symmetric_key'])

        print("Key generation completed.")

    def encrypt_file(self) -> None:
        '''
        Encrypts target file using CAST5 symmetric encryption.
        Uses RSA to decrypt the symmetric key first.
        '''
        private_key = self.file_manager.load_private_key_pem(self.config['private_key'])
        encrypted_cast_key = self.file_manager.read_file(self.config['symmetric_key'])
        cast_key = self.rsa_manager.decrypt(encrypted_cast_key, private_key)

        data = self.file_manager.read_file(self.config['text_file'])
        encrypted_data = self.cast_manager.encrypt(data, cast_key)
        self.file_manager.write_file(encrypted_data, self.config['encrypted_file'])

        print("Encryption complete.")

    def decrypt_file(self) -> None:
        '''
        Decrypts file using CAST5 symmetric encryption.
        Uses RSA to decrypt the symmetric key first.
        '''
        private_key = self.file_manager.load_private_key_pem(self.config['private_key'])
        encrypted_cast_key = self.file_manager.read_file(self.config['symmetric_key'])
        cast_key = self.rsa_manager.decrypt(encrypted_cast_key, private_key)

        encrypted_data = self.file_manager.read_file(self.config['encrypted_file'])
        decrypted_data = self.cast_manager.decrypt(encrypted_data, cast_key)
        self.file_manager.write_file(decrypted_data, self.config['decrypted_file'])

        print("Decryption complete.")