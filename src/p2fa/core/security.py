# Encryption / KDF / Hashing
import os
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt

def derive_key(
        password: str,
        salt: bytes
) -> bytes:
    """
    password to base64 key
    """

    kdf = Scrypt(
        salt = salt,
        length = 32,
        n = 2**16, # 2^16 - memory cost
        r = 8,     # block size
        p = 1      # parallelisation value
    )

    # encode turns the password into binary so Scrypt can understand it
    raw_key: bytes = kdf.derive(
        password.encode()
    )

    return base64.urlsafe_b64encode(
        raw_key
    )

def encrypt_password(
        data: str,
        password: str,
        salt: bytes
) -> bytes:
    """
    encrypt the password
    """
    # get the key
    key: bytes = derive_key(
        password,
        salt
    )

    f: Fernet = Fernet(
        key
    )

    # encrypt the data
    secret_bytes: bytes = data.encode()

    return f.encrypt(
        secret_bytes
    )

def decrypt_password(
        password: str,
        salt: bytes,
        token: bytes
) -> bytes:
    ...