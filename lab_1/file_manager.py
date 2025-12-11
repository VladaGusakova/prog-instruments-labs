import os
import json
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import (
    load_pem_public_key,
    load_pem_private_key,
)
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey, RSAPublicKey
from typing import Dict, Any


class FileManager:
    """
    A utility class for handling file operations related to keys and configuration.
    """

    def read_key_length_from_file(self, filepath: str) -> int:
        """
        Reads the key length (as integer) from a text file.
        :param filepath: Path to the text file containing the key length.
        :return: Key length as integer.
        :raises IOError: If the file cannot be read or content is not an integer.
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                key_length = int(content)
                return key_length
        except Exception as e:
            raise IOError(f"Error reading key length from file '{filepath}': {e}")

    def read_file(self, filepath: str) -> bytes:
        """
        Reads binary data from a file.
        :param filepath: Path to the file to read.
        :return: Data bytes read from the file.
        :raises IOError: If the file cannot be read.
        """
        try:
            with open(filepath, 'rb') as f:
                data = f.read()
            print(f"File read: {filepath} ({len(data)} bytes)")
            return data
        except Exception as e:
            raise IOError(f"Error reading file {filepath}: {e}")

    def write_file(self, data: bytes, filepath: str) -> None:
        """
        Writes binary data to a file, creating directories if needed.
        :param data: Data bytes to write.
        :param filepath: Path to the target file.
        :raises IOError: If the file cannot be written.
        """
        try:
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            with open(filepath, 'wb') as f:
                f.write(data)
            print(f"File written: {filepath} ({len(data)} bytes)")
        except Exception as e:
            raise IOError(f"Error writing file {filepath}: {e}")

    def save_private_key_pem(self, private_key: RSAPrivateKey, filepath: str) -> None:
        """
        Saves an RSA private key to a file in PEM format without encryption.
        :param private_key: RSA private key object.
        :param filepath: Path to save the private key.
        :raises IOError: If the key cannot be serialized or saved.
        """
        try:
            pem = private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption(),
            )
            self.write_file(pem, filepath)
            print(f"Private key saved: {filepath}")
        except Exception as e:
            raise IOError(f"Error saving private key: {e}")

    def save_public_key_pem(self, public_key: RSAPublicKey, filepath: str) -> None:
        """
        Saves an RSA public key to a file in PEM format.
        :param public_key: RSA public key object.
        :param filepath: Path to save the public key.
        :raises IOError: If the key cannot be serialized or saved.
        """
        try:
            pem = public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo,
            )
            self.write_file(pem, filepath)
            print(f"Public key saved: {filepath}")
        except Exception as e:
            raise IOError(f"Error saving public key: {e}")

    def load_private_key_pem(self, filepath: str) -> RSAPrivateKey:
        """
        Loads an RSA private key from a PEM file.
        :param filepath: Path to the PEM file containing the private key.
        :return: RSA private key object.
        :raises IOError: If the file cannot be read or the key is invalid.
        """
        try:
            data = self.read_file(filepath)
            private_key = load_pem_private_key(data, password=None)
            return private_key
        except Exception as e:
            raise IOError(f"Error loading private key: {e}")

    def load_public_key_pem(self, filepath: str) -> RSAPublicKey:
        """
        Loads an RSA public key from a PEM file.
        :param filepath: Path to the PEM file containing the public key.
        :return: RSA public key object.
        :raises IOError: If the file cannot be read or the key is invalid.
        """
        try:
            data = self.read_file(filepath)
            public_key = load_pem_public_key(data)
            return public_key
        except Exception as e:
            raise IOError(f"Error loading public key: {e}")

    def load_json_config(self, filepath: str) -> Dict[str, Any]:
        """
        Loads a JSON configuration file.
        :param filepath: Path to the JSON configuration file.
        :return: Parsed configuration dictionary.
        :raises IOError: If the file cannot be read or JSON is invalid.
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                config = json.load(f)
            print(f"Configuration loaded: {filepath}")
            return config
        except Exception as e:
            raise IOError(f"Error loading config {filepath}: {e}")



