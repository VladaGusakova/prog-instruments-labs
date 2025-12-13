import os
import sys
from typing import Any, Dict
from file_manager import FileManager
from hybrid_crypto import HybridCrypto
from pars import create_parser

MIN_KEY_LENGTH = 40
MAX_KEY_LENGTH = 128
KEY_LENGTH_MULTIPLE = 8


def main() -> None:
    '''
    Using all functions
    :return: None
    '''
    try:
        file_manager = FileManager()
        config = file_manager.load_json_config('settings.json')
        parser = create_parser()
        args = parser.parse_args()

        if os.path.isfile(config.get('key_length')):
            key_length = file_manager.read_key_length_from_file(config.get('key_length'))
            if (key_length < MIN_KEY_LENGTH or key_length > MAX_KEY_LENGTH) or key_length % KEY_LENGTH_MULTIPLE != 0:
                raise ValueError("Incorrect key length.")
            config['cast_key_length'] = key_length
        else:
            key_length = args.cast_key_length
            if (key_length < MIN_KEY_LENGTH or key_length > MAX_KEY_LENGTH) or key_length % KEY_LENGTH_MULTIPLE != 0:
                raise ValueError("Incorrect key length.")
            config['cast_key_length'] = key_length

        crypto = HybridCrypto(config, file_manager)
        if args.generation:
            crypto.generate_keys()
        elif args.encryption:
            crypto.encrypt_file()
        elif args.decryption:
            crypto.decrypt_file()
    except (ValueError, FileNotFoundError, RuntimeError, OSError, PermissionError) as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()