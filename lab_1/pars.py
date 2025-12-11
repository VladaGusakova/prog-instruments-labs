import argparse


def create_parser() -> argparse.ArgumentParser:
    '''
    Creates an argument parser for the hybrid crypto system.
    Defines command line arguments for key generation, encryption,
    and decryption operations.
    :return: Configured argument parser object
    :rtype: argparse.ArgumentParser
    '''
    parser = argparse.ArgumentParser(
        description='Hybrid RSA + CAST5 Cryptosystem'
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        '-gen',
        '--generation',
        action='store_true',
        help='Key Generation'
    )
    group.add_argument(
        '-enc',
        '--encryption',
        action='store_true',
        help='File Encryption'
    )
    group.add_argument(
        '-dec',
        '--decryption',
        action='store_true',
        help='Decrypting a file'
    )
    parser.add_argument(
        '-len',
        '--cast-key-length',
        type=int,
        default=128,
        help='Key Length CAST5'
    )
    return parser