import pandas as pd
import cv2
import matplotlib.pyplot as plt
import argparse
import os
from typing import Tuple
import numpy as np

def create_parse() -> argparse.Namespace:
    '''
    Creates argument parser for command line interface.
    :return: Parsed command line arguments
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument("annotation_path", type=str, help="Path to annotation")
    parser.add_argument("width", type=int, help="Max width")
    parser.add_argument("height", type=int, help="Max height")
    args = parser.parse_args()
    return args

def create_df(annotation_path: str) -> pd.DataFrame:
    '''
    Creates DataFrame from annotation CSV file.
    :param annotation_path: Path to annotation CSV file
    :return: DataFrame with annotation data
    '''
    if os.path.isfile(annotation_path):
        df = pd.read_csv(annotation_path)
        return df
    else:
        raise FileNotFoundError(f"File {annotation_path} not found.")

def add_image_shape(df: pd.DataFrame) -> pd.DataFrame:
    '''
    Adds image dimensions to DataFrame.
    :param df: Input DataFrame with image paths
    :return: DataFrame with added height, width and channels columns
    '''
    height = []
    width = []
    channels = []
    for path in df["relative path"]:
        if os.path.isfile(path):
            img: np.ndarray = cv2.imread(path)
            height.append(img.shape[0])
            width.append(img.shape[1])
            channels.append(img.shape[2])
        else:
            raise FileNotFoundError(f"Image file {path} not found.")
    df["height"] = height
    df["width"] = width
    df["channels"] = channels
    return df

def statistic(df: pd.DataFrame) -> pd.DataFrame:
    '''
    Calculates descriptive statistics for image dimensions.
    :param df: DataFrame with image dimensions
    :return: Statistical summary DataFrame
    '''
    stats = df[["height", "width", "channels"]].describe()
    return stats

def filter_by_width_and_height(df: pd.DataFrame, max_w: int, max_h: int) -> pd.DataFrame:
    '''
    Filters images by maximum width and height.
    :param df: DataFrame with image dimensions
    :param max_w: Maximum allowed width
    :param max_h: Maximum allowed height
    :return: Filtered DataFrame
    '''
    filtered_df = df[(df['width'] <= max_w) & (df['height'] <= max_h)]
    return filtered_df

def add_area(df: pd.DataFrame) -> pd.DataFrame:
    '''
    Calculates and adds image area column.
    :param df: DataFrame with image dimensions
    :return: DataFrame with added area column
    '''
    if 'width' in df.columns:
        df['area'] = df['width'] * df['height']
        return df
    else:
        raise RuntimeError(f"Failed to add area column")

def filter_by_area(df: pd.DataFrame) -> pd.DataFrame:
    '''
    Sorts DataFrame by image area in ascending order.
    :param df: DataFrame with image area
    :return: Sorted DataFrame by area
    '''
    if 'area' in df.columns:
        df_sorted = df.sort_values(by='area')
        return df_sorted
    else:
        raise RuntimeError(f"Failed to filter by area")

def create_histogram(df: pd.DataFrame) -> None:
    '''
    Creates histogram of image areas distribution.
    :param df: DataFrame with image areas
    '''
    plt.hist(df['area'], bins=df.shape[0], color='black')
    plt.title('image area distribution')
    plt.xlabel('area(px)')
    plt.ylabel('frequency')
    plt.show()

def main() -> None:
    '''
    Main function to execute image analysis pipeline.
    '''
    try:
        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)
        args = create_parse()
        df = create_df(args.annotation_path)
        print(df.head())
        add_image_shape(df)
        print(df, "\n")
        print(statistic(df))
        print(filter_by_width_and_height(df, args.width, args.height))
        print(filter_by_area(add_area(df)))
        create_histogram(df)
    except Exception as exc:
        print(exc)

if __name__ == '__main__':
    main()



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