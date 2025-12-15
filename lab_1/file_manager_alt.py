import os
import json
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import (
    load_pem_public_key,
    load_pem_private_key,
)
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey, RSAPublicKey
from cryptography.exceptions import InvalidKey, UnsupportedAlgorithm
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
        :raises FileNotFoundError: If the file does not exist.
        :raises PermissionError: If the file cannot be read due to permissions.
        :raises ValueError: If the content cannot be converted to integer.
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                key_length = int(content)
                return key_length
        except FileNotFoundError as e:
            raise FileNotFoundError(f"File '{filepath}' not found: {e}") from e
        except PermissionError as e:
            raise PermissionError(f"Permission denied for file '{filepath}': {e}") from e
        except ValueError as e:
            raise ValueError(f"Invalid key length value in file '{filepath}': {e}") from e
        except OSError as e:
            raise OSError(f"OS error reading file '{filepath}': {e}") from e

    def read_file(self, filepath: str) -> bytes:
        """
        Reads binary data from a file.
        :param filepath: Path to the file to read.
        :return: Data bytes read from the file.
        :raises FileNotFoundError: If the file does not exist.
        :raises PermissionError: If the file cannot be read due to permissions.
        :raises OSError: For other OS-related errors.
        """
        try:
            with open(filepath, 'rb') as f:
                data = f.read()
            print(f"File read: {filepath} ({len(data)} bytes)")
            return data
        except FileNotFoundError as e:
            raise FileNotFoundError(f"File {filepath} not found: {e}") from e
        except PermissionError as e:
            raise PermissionError(f"Permission denied for file {filepath}: {e}") from e
        except OSError as e:
            raise OSError(f"OS error reading file {filepath}: {e}") from e

    def write_file(self, data: bytes, filepath: str) -> None:
        """
        Writes binary data to a file, creating directories if needed.
        :param data: Data bytes to write.
        :param filepath: Path to the target file.
        :raises PermissionError: If the file cannot be written due to permissions.
        :raises OSError: For other OS-related errors.
        """
        try:
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            with open(filepath, 'wb') as f:
                f.write(data)
            print(f"File written: {filepath} ({len(data)} bytes)")
        except PermissionError as e:
            raise PermissionError(f"Permission denied for file {filepath}: {e}") from e
        except OSError as e:
            raise OSError(f"OS error writing file {filepath}: {e}") from e

    def save_private_key_pem(self, private_key: RSAPrivateKey, filepath: str) -> None:
        """
        Saves an RSA private key to a file in PEM format without encryption.
        :param private_key: RSA private key object.
        :param filepath: Path to save the private key.
        :raises ValueError: If the key cannot be serialized.
        :raises OSError: If the file cannot be saved.
        """
        try:
            pem = private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption(),
            )
            self.write_file(pem, filepath)
            print(f"Private key saved: {filepath}")
        except (ValueError, TypeError) as e:
            raise ValueError(f"Failed to serialize private key: {e}") from e
        except OSError as e:
            raise OSError(f"Failed to save private key to {filepath}: {e}") from e

    def save_public_key_pem(self, public_key: RSAPublicKey, filepath: str) -> None:
        """
        Saves an RSA public key to a file in PEM format.
        :param public_key: RSA public key object.
        :param filepath: Path to save the public key.
        :raises ValueError: If the key cannot be serialized.
        :raises OSError: If the file cannot be saved.
        """
        try:
            pem = public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo,
            )
            self.write_file(pem, filepath)
            print(f"Public key saved: {filepath}")
        except (ValueError, TypeError) as e:
            raise ValueError(f"Failed to serialize public key: {e}") from e
        except OSError as e:
            raise OSError(f"Failed to save public key to {filepath}: {e}") from e

    def load_private_key_pem(self, filepath: str) -> RSAPrivateKey:
        """
        Loads an RSA private key from a PEM file.
        :param filepath: Path to the PEM file containing the private key.
        :return: RSA private key object.
        :raises FileNotFoundError: If the file does not exist.
        :raises ValueError: If the key is invalid.
        :raises UnsupportedAlgorithm: If the key format is not supported.
        """
        try:
            data = self.read_file(filepath)
            private_key = load_pem_private_key(data, password=None)
            return private_key
        except (ValueError, InvalidKey, UnsupportedAlgorithm) as e:
            raise ValueError(f"Invalid private key in file {filepath}: {e}") from e
        except Exception as e:
            raise RuntimeError(f"Failed to load private key from {filepath}: {e}") from e

    def load_public_key_pem(self, filepath: str) -> RSAPublicKey:
        """
        Loads an RSA public key from a PEM file.
        :param filepath: Path to the PEM file containing the public key.
        :return: RSA public key object.
        :raises FileNotFoundError: If the file does not exist.
        :raises ValueError: If the key is invalid.
        :raises UnsupportedAlgorithm: If the key format is not supported.
        """
        try:
            data = self.read_file(filepath)
            public_key = load_pem_public_key(data)
            return public_key
        except (ValueError, InvalidKey, UnsupportedAlgorithm) as e:
            raise ValueError(f"Invalid public key in file {filepath}: {e}") from e
        except Exception as e:
            raise RuntimeError(f"Failed to load public key from {filepath}: {e}") from e

    def load_json_config(self, filepath: str) -> Dict[str, Any]:
        """
        Loads a JSON configuration file.
        :param filepath: Path to the JSON configuration file.
        :return: Parsed configuration dictionary.
        :raises FileNotFoundError: If the file does not exist.
        :raises json.JSONDecodeError: If the JSON is invalid.
        :raises PermissionError: If the file cannot be read.
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                config = json.load(f)
            print(f"Configuration loaded: {filepath}")
            return config
        except FileNotFoundError as e:
            raise FileNotFoundError(f"Config file {filepath} not found: {e}") from e
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in config file {filepath}: {e}") from e
        except PermissionError as e:
            raise PermissionError(f"Permission denied for config file {filepath}: {e}") from e
        except OSError as e:
            raise OSError(f"OS error reading config file {filepath}: {e}") from e