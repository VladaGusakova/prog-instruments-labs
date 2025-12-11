import os
import json
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import (
    load_pem_public_key,
    load_pem_private_key,
)


class FileManager:
    def read_key_length_from_file(self, filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                key_length = int(content)
                return key_length
        except Exception as e:
            raise IOError(f"Error reading key length from file '{filepath}': {e}")

    def read_file(self, filepath):
        try:
            with open(filepath, 'rb') as f:
                data = f.read()
            print(f"File read: {filepath} ({len(data)} bytes)")
            return data
        except Exception as e:
            raise IOError(f"Error reading file {filepath}: {e}")

    def write_file(self, data, filepath):
        try:
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            with open(filepath, 'wb') as f:
                f.write(data)
            print(f"File written: {filepath} ({len(data)} bytes)")
        except Exception as e:
            raise IOError(f"Error writing file {filepath}: {e}")

    def save_private_key_pem(self, private_key, filepath):
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

    def save_public_key_pem(self, public_key, filepath):
        try:
            pem = public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo,
            )
            self.write_file(pem, filepath)
            print(f"Public key saved: {filepath}")
        except Exception as e:
            raise IOError(f"Error saving public key: {e}")

    def load_private_key_pem(self, filepath):
        try:
            data = self.read_file(filepath)
            private_key = load_pem_private_key(data, password=None)
            return private_key
        except Exception as e:
            raise IOError(f"Error loading private key: {e}")

    def load_public_key_pem(self, filepath):
        try:
            data = self.read_file(filepath)
            public_key = load_pem_public_key(data)
            return public_key
        except Exception as e:
            raise IOError(f"Error loading public key: {e}")

    def load_json_config(self, filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                config = json.load(f)
            print(f"Configuration loaded: {filepath}")
            return config
        except Exception as e:
            raise IOError(f"Error loading config {filepath}: {e}")